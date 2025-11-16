"""
Voice endpoints for audio transcription
"""
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from app.services.voice import VoiceService
from app.services.vision import VisionService
from app.services.database import DatabaseService
from app.core.config import get_settings

router = APIRouter(prefix="/voice", tags=["voice"])


@router.websocket("/transcribe")
async def transcribe_audio(websocket: WebSocket, user_id: str) -> None:
    """
    WebSocket endpoint for real-time audio transcription

    Args:
        websocket: WebSocket connection
        user_id: User ID for session management
    """
    await websocket.accept()
    settings = get_settings()
    voice_service = VoiceService()

    # Lazy-load services only when needed (after wake word detection)
    vision_service = None
    db_service = None

    try:
        # Buffer for wake word detection
        transcription_buffer: list[str] = []
        wake_word_detected = False

        async def handle_transcript(text: str) -> None:
            """Handle transcribed text"""
            nonlocal wake_word_detected, vision_service, db_service

            # Add to buffer
            transcription_buffer.append(text)

            # Keep only last 5 transcripts
            if len(transcription_buffer) > 5:
                transcription_buffer.pop(0)

            # Check for wake word
            full_text = " ".join(transcription_buffer)
            if voice_service.detect_wake_word(full_text, settings.wake_word):
                wake_word_detected = True
                await websocket.send_json(
                    {"type": "wake_word", "message": "Wake word detected!"}
                )

            # Send transcription to client
            await websocket.send_json(
                {
                    "type": "transcription",
                    "text": text,
                    "wake_word_active": wake_word_detected,
                }
            )

            # If wake word is active, process the command
            if wake_word_detected:
                # Lazy-load services when wake word is first detected
                if vision_service is None:
                    try:
                        vision_service = VisionService()
                    except Exception as e:
                        print(f"⚠️  Vision service not available: {e}")
                        await websocket.send_json({"type": "error", "message": f"Vision unavailable: {e}"})
                        return

                if db_service is None:
                    try:
                        db_service = DatabaseService()
                    except Exception as e:
                        print(f"⚠️  Database service not available: {e}")
                        # Continue without database

                # Classify intent
                intent_result = await vision_service.classify_intent(
                    text, context={"user_id": user_id}
                )

                await websocket.send_json(
                    {
                        "type": "intent",
                        "intent": intent_result["intent"],
                        "confidence": intent_result["confidence"],
                        "entities": intent_result["entities"],
                    }
                )

                # Log to database (if available)
                if db_service:
                    try:
                        await db_service.log_action(
                            {
                                "user_id": user_id,
                                "action_type": "voice_command",
                                "intent": intent_result["intent"],
                                "text": text,
                            }
                        )
                    except Exception as e:
                        print(f"⚠️  Could not log to database: {e}")

        # Start transcription
        await voice_service.start_transcription(
            on_transcript=handle_transcript,
            language="en",
        )

        # Receive and process audio data
        while True:
            audio_data = await websocket.receive_bytes()
            await voice_service.send_audio(audio_data)

    except WebSocketDisconnect:
        print(f"WebSocket disconnected for user {user_id}")
    except Exception as e:
        print(f"Error in transcription: {e}")
        await websocket.send_json({"type": "error", "message": str(e)})
    finally:
        await voice_service.stop_transcription()
        await websocket.close()


@router.get("/wake-word-test")
async def test_wake_word(text: str) -> dict[str, str | bool]:
    """
    Test wake word detection

    Args:
        text: Text to test

    Returns:
        Dictionary with detection result
    """
    settings = get_settings()
    voice_service = VoiceService()

    detected = voice_service.detect_wake_word(text, settings.wake_word)

    return {
        "text": text,
        "wake_word": settings.wake_word,
        "detected": detected,
    }


@router.post("/text-to-speech")
async def text_to_speech(text: str) -> dict[str, str]:
    """
    Convert text to speech using Deepgram TTS

    Args:
        text: Text to convert to speech

    Returns:
        Base64 encoded audio data
    """
    try:
        voice_service = VoiceService()
        audio_bytes = await voice_service.text_to_speech(text)

        # Encode to base64 for JSON transport
        import base64
        audio_base64 = base64.b64encode(audio_bytes).decode("utf-8")

        return {
            "text": text,
            "audio": audio_base64,
            "format": "audio/mpeg",
        }

    except Exception as e:
        from fastapi import HTTPException
        print(f"Error in TTS endpoint: {e}")
        raise HTTPException(status_code=500, detail=str(e))
