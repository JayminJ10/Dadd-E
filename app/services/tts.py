"""
Text-to-Speech service using OpenAI
"""
import asyncio
from pathlib import Path
from typing import Optional
import httpx
from app.core.config import get_settings


class TTSService:
    """Service for converting text to speech using OpenAI TTS"""

    def __init__(self) -> None:
        settings = get_settings()
        self.api_key = settings.openai_api_key
        self.voice = "alloy"  # Options: alloy, echo, fable, onyx, nova, shimmer
        self.model = "tts-1"  # tts-1 (faster) or tts-1-hd (higher quality)

    async def speak(
        self,
        text: str,
        voice: Optional[str] = None,
        speed: float = 1.0,
    ) -> bytes:
        """
        Convert text to speech

        Args:
            text: Text to convert to speech
            voice: Voice to use (alloy, echo, fable, onyx, nova, shimmer)
            speed: Speed of speech (0.25 to 4.0)

        Returns:
            Audio data as bytes (MP3 format)
        """
        try:
            # Use httpx directly to avoid AsyncOpenAI version conflicts
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    "https://api.openai.com/v1/audio/speech",
                    headers={
                        "Authorization": f"Bearer {self.api_key}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "model": self.model,
                        "voice": voice or self.voice,
                        "input": text,
                        "speed": speed
                    },
                    timeout=30.0
                )
                response.raise_for_status()
                return response.content

        except Exception as e:
            print(f"❌ TTS error: {e}")
            raise

    async def speak_and_save(
        self,
        text: str,
        output_path: str,
        voice: Optional[str] = None,
        speed: float = 1.0,
    ) -> str:
        """
        Convert text to speech and save to file

        Args:
            text: Text to convert
            output_path: Path to save audio file
            voice: Voice to use
            speed: Speed of speech

        Returns:
            Path to saved audio file
        """
        try:
            audio_data = await self.speak(text, voice, speed)

            # Save to file
            with open(output_path, "wb") as f:
                f.write(audio_data)

            return output_path

        except Exception as e:
            print(f"❌ Error saving TTS audio: {e}")
            raise

    def set_voice(self, voice: str) -> None:
        """
        Change the default voice

        Args:
            voice: Voice name (alloy, echo, fable, onyx, nova, shimmer)
        """
        valid_voices = ["alloy", "echo", "fable", "onyx", "nova", "shimmer"]
        if voice in valid_voices:
            self.voice = voice
        else:
            raise ValueError(f"Invalid voice. Choose from: {valid_voices}")

    def set_model(self, model: str) -> None:
        """
        Change the TTS model

        Args:
            model: tts-1 (faster) or tts-1-hd (higher quality)
        """
        if model in ["tts-1", "tts-1-hd"]:
            self.model = model
        else:
            raise ValueError("Model must be 'tts-1' or 'tts-1-hd'")
