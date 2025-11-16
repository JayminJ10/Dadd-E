"""
Text-to-Speech endpoints
"""
from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from app.services.tts import TTSService
import io

router = APIRouter(prefix="/tts", tags=["tts"])


class TTSRequest(BaseModel):
    """TTS request model"""
    text: str
    voice: str = "alloy"  # alloy, echo, fable, onyx, nova, shimmer
    speed: float = 1.0


@router.post("/speak")
async def text_to_speech(request: TTSRequest):
    """
    Convert text to speech and return audio

    Args:
        request: TTS request with text, voice, and speed

    Returns:
        Audio file (MP3 format)
    """
    try:
        tts_service = TTSService()
        audio_data = await tts_service.speak(
            text=request.text,
            voice=request.voice,
            speed=request.speed
        )

        # Return audio as streaming response
        return StreamingResponse(
            io.BytesIO(audio_data),
            media_type="audio/mpeg",
            headers={
                "Content-Disposition": f"attachment; filename=speech.mp3"
            }
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"TTS error: {str(e)}")


@router.get("/voices")
async def get_available_voices():
    """Get list of available TTS voices"""
    return {
        "voices": [
            {"id": "alloy", "description": "Neutral and balanced"},
            {"id": "echo", "description": "Male, clear and articulate"},
            {"id": "fable", "description": "British accent, warm"},
            {"id": "onyx", "description": "Deep, authoritative male"},
            {"id": "nova", "description": "Female, energetic and friendly"},
            {"id": "shimmer", "description": "Female, soft and gentle"}
        ]
    }
