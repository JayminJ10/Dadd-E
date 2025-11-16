"""
Simple TTS test script
"""
import asyncio
import aiohttp


async def test_tts():
    """Test the TTS endpoint"""
    print("🧪 Testing TTS...")

    async with aiohttp.ClientSession() as session:
        # Test TTS endpoint
        tts_payload = {
            "text": "Hello! I am Daddy, your AI assistant. How can I help you today?",
            "voice": "nova",  # Try: alloy, echo, fable, onyx, nova, shimmer
            "speed": 1.0
        }

        print(f"📝 Speaking: {tts_payload['text']}")
        print(f"🎤 Voice: {tts_payload['voice']}")

        async with session.post(
            "http://localhost:8000/tts/speak",
            json=tts_payload
        ) as response:
            if response.status == 200:
                print("✅ TTS successful!")

                # Save audio to file
                audio_data = await response.read()
                with open("test_output.mp3", "wb") as f:
                    f.write(audio_data)

                print("💾 Saved to: test_output.mp3")
                print("🔊 Playing audio...")

                # Play using macOS afplay
                import subprocess
                subprocess.run(["afplay", "test_output.mp3"])

                print("✅ Audio playback complete!")

            else:
                error_text = await response.text()
                print(f"❌ TTS failed: {response.status} - {error_text}")


if __name__ == "__main__":
    asyncio.run(test_tts())
