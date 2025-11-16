"""
Deepgram voice transcription (STT) service
Using Deepgram SDK v2.12.0 (compatible with omi-sdk)
"""
import asyncio
import inspect
from typing import Callable, Union, Awaitable, Optional
from deepgram import Deepgram
from app.core.config import get_settings


class VoiceService:
    """Service for real-time voice transcription using Deepgram v2 API"""

    def __init__(self) -> None:
        settings = get_settings()
        self.client = Deepgram(settings.deepgram_api_key)
        self.connection: Optional[any] = None
        self.is_listening = False

    async def start_transcription(
        self,
        on_transcript: Union[Callable[[str], None], Callable[[str], Awaitable[None]]],
        language: str = "en",
    ) -> None:
        """
        Start real-time transcription

        Args:
            on_transcript: Callback function (sync or async) to handle transcribed text
            language: Language code for transcription
        """
        try:
            # Create live transcription connection (this is a coroutine in v2)
            # We're sending PCM audio decoded from Opus
            self.connection = await self.client.transcription.live({
                "punctuate": True,
                "interim_results": True,  # Enable for faster feedback
                "language": language,
                "model": "nova-2",
                "smart_format": True,
                "encoding": "linear16",  # PCM 16-bit (decoded from Opus)
                "sample_rate": 16000,  # 16kHz
                "channels": 1,  # Mono
            })

            # Set up event handlers
            def on_message(data: any) -> None:
                try:
                    # Deepgram v2 SDK response format varies
                    transcript = None

                    # Try different response formats
                    if isinstance(data, dict):
                        # Format 1: data['channel']['alternatives'][0]['transcript']
                        if "channel" in data and "alternatives" in data["channel"]:
                            transcript = data["channel"]["alternatives"][0]["transcript"]
                        # Format 2: data['alternatives'][0]['transcript']
                        elif "alternatives" in data:
                            transcript = data["alternatives"][0]["transcript"]
                        # Format 3: data['transcript']
                        elif "transcript" in data:
                            transcript = data["transcript"]

                    if transcript and len(transcript) > 0:
                        print(f"✅ Got transcript: {transcript}")
                        # Handle both sync and async callbacks
                        if inspect.iscoroutinefunction(on_transcript):
                            asyncio.create_task(on_transcript(transcript))
                        else:
                            on_transcript(transcript)
                except (KeyError, IndexError, TypeError) as e:
                    print(f"⚠️  Error parsing transcript: {e}, data: {data}")

            def on_error(error: any) -> None:
                print(f"Deepgram error: {error}")

            # Register event handlers
            self.connection.registerHandler(
                self.connection.event.CLOSE,
                lambda _: print("Deepgram connection closed")
            )
            self.connection.registerHandler(
                self.connection.event.TRANSCRIPT_RECEIVED,
                on_message
            )
            self.connection.registerHandler(
                self.connection.event.ERROR,
                on_error
            )

            self.is_listening = True
            print("Deepgram connection started successfully")

        except Exception as e:
            print(f"Error starting transcription: {e}")
            raise

    async def send_audio(self, audio_data: bytes) -> None:
        """
        Send audio data to Deepgram for transcription

        Args:
            audio_data: Raw audio bytes to transcribe
        """
        if self.connection and self.is_listening:
            try:
                self.connection.send(audio_data)
                # Log first send to confirm
                if not hasattr(self, '_sent_first'):
                    self._sent_first = True
                    print(f"📤 Sending audio to Deepgram ({len(audio_data)} bytes)")
            except Exception as e:
                print(f"❌ Error sending audio: {e}")

    async def stop_transcription(self) -> None:
        """Stop the transcription connection"""
        if self.connection:
            try:
                self.connection.finish()
                self.is_listening = False
                print("Deepgram connection closed")
            except Exception as e:
                print(f"Error stopping transcription: {e}")

    def detect_wake_word(self, text: str, wake_word: str = "dadd-e") -> bool:
        """
        Detect wake word in transcribed text

        Args:
            text: Transcribed text to check
            wake_word: Wake word to detect

        Returns:
            True if wake word detected, False otherwise
        """
        return wake_word.lower() in text.lower()

    async def text_to_speech(self, text: str) -> bytes:
        """
        Convert text to speech using Deepgram TTS

        Note: TTS is not available in Deepgram SDK v2.12.0
        This is a placeholder for future upgrade to v3+

        Args:
            text: Text to convert to speech

        Returns:
            Audio bytes
        """
        # TTS not available in v2.12.0
        # Would need to upgrade to deepgram-sdk v3+ which conflicts with omi-sdk
        raise NotImplementedError(
            "TTS is not available in Deepgram SDK v2.12.0. "
            "Requires v3+ which conflicts with omi-sdk. "
            "Use OpenAI TTS or ElevenLabs as alternative."
        )
