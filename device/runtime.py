"""
Omi Device Runtime
Connects Omi glasses to the Dadd-E FastAPI backend
"""
import asyncio
import os
import sys
from typing import Optional
import aiohttp
import websockets
from dotenv import load_dotenv

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from device.omi_service import OmiDeviceService

# Load environment variables
load_dotenv()


class DaddERuntime:
    """Runtime for connecting Omi glasses to Dadd-E backend"""

    def __init__(self) -> None:
        self.device_mac = os.getenv("OMI_DEVICE_MAC", "")
        self.backend_url = os.getenv("BACKEND_URL", "http://localhost:8000")
        self.websocket_url = self.backend_url.replace("http", "ws")
        self.user_id = os.getenv("USER_ID", "test_user")
        self.omi_service: Optional[OmiDeviceService] = None
        self.ws_connection: Optional[any] = None

    async def start(self) -> None:
        """Start the runtime"""
        print("🚀 Starting Dadd-E Runtime")
        print(f"📡 Backend: {self.backend_url}")
        print(f"👤 User ID: {self.user_id}")
        print(f"🎧 Device MAC: {self.device_mac}")

        if not self.device_mac:
            print("❌ Error: OMI_DEVICE_MAC not set in environment")
            return

        # Initialize Omi service
        self.omi_service = OmiDeviceService(self.device_mac)

        # Connect to backend WebSocket
        await self.connect_to_backend()

    async def connect_to_backend(self) -> None:
        """Connect to FastAPI backend via WebSocket"""
        try:
            ws_url = f"{self.websocket_url}/voice/transcribe?user_id={self.user_id}"
            print(f"🔌 Connecting to WebSocket: {ws_url}")

            async with websockets.connect(ws_url) as websocket:
                self.ws_connection = websocket
                print("✅ Connected to backend")

                # Handle audio streaming in the background
                audio_task = asyncio.create_task(self.stream_audio_to_backend())

                # Handle messages from backend
                message_task = asyncio.create_task(self.handle_backend_messages())

                # Wait for both tasks
                await asyncio.gather(audio_task, message_task)

        except Exception as e:
            print(f"❌ Error connecting to backend: {e}")

    async def stream_audio_to_backend(self) -> None:
        """Stream audio from Omi device to backend"""
        if not self.omi_service:
            return

        def on_audio(pcm_data: bytes) -> None:
            """Callback for audio data"""
            if self.ws_connection:
                asyncio.create_task(self.ws_connection.send(pcm_data))

        try:
            # Connect to Omi device and start streaming
            await self.omi_service.connect(on_audio)
        except Exception as e:
            print(f"❌ Error streaming audio: {e}")

    async def handle_backend_messages(self) -> None:
        """Handle messages from backend"""
        if not self.ws_connection:
            return

        try:
            async for message in self.ws_connection:
                # Parse JSON message
                import json

                data = json.loads(message)
                msg_type = data.get("type", "")

                if msg_type == "transcription":
                    text = data.get("text", "")
                    wake_word_active = data.get("wake_word_active", False)

                    if wake_word_active:
                        print(f"🎙️  [ACTIVE] {text}")
                    else:
                        print(f"🎙️  {text}")

                elif msg_type == "wake_word":
                    print(f"🔔 {data.get('message', 'Wake word detected!')}")

                elif msg_type == "intent":
                    intent = data.get("intent", "")
                    confidence = data.get("confidence", 0)
                    print(f"🎯 Intent: {intent} (confidence: {confidence:.2f})")

                elif msg_type == "error":
                    print(f"❌ Error: {data.get('message', 'Unknown error')}")

        except Exception as e:
            print(f"❌ Error handling backend messages: {e}")

    async def capture_and_analyze_scene(self) -> None:
        """Capture frame and send for vision analysis"""
        if not self.omi_service:
            return

        try:
            # Capture frame (placeholder - needs camera API)
            frame = await self.omi_service.capture_frame()

            if frame:
                # Send to vision API
                async with aiohttp.ClientSession() as session:
                    form_data = aiohttp.FormData()
                    form_data.add_field("image", frame, filename="frame.jpg")

                    async with session.post(
                        f"{self.backend_url}/vision/describe",
                        params={"user_id": self.user_id},
                        data=form_data,
                    ) as response:
                        result = await response.json()
                        description = result.get("description", "")
                        print(f"👁️  Scene: {description}")
            else:
                print("⚠️  No frame available (camera API not yet implemented)")

        except Exception as e:
            print(f"❌ Error analyzing scene: {e}")


async def main() -> None:
    """Main entry point"""
    runtime = DaddERuntime()
    await runtime.start()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n👋 Shutting down Dadd-E Runtime")
