"""
Omi Device Service - Handles connection and communication with Omi glasses
"""
import asyncio
from typing import Callable, Optional
from omi import listen_to_omi, OmiOpusDecoder
from asyncio import Queue


class OmiDeviceService:
    """Service for managing Omi device connection and data streams"""

    def __init__(
        self,
        device_mac: str,
        audio_char_uuid: str = "19B10001-E8F2-537E-4F6C-D104768A1214",
    ) -> None:
        """
        Initialize Omi device service

        Args:
            device_mac: MAC address of the Omi device
            audio_char_uuid: UUID for audio characteristic
        """
        self.device_mac = device_mac
        self.audio_char_uuid = audio_char_uuid
        self.audio_queue: Queue[bytes] = Queue()
        self.frame_buffer: Optional[bytes] = None
        self.is_connected = False
        self.decoder = OmiOpusDecoder()

    async def connect(self, on_audio_callback: Callable[[bytes], None]) -> None:
        """
        Connect to Omi device and start listening for audio

        Args:
            on_audio_callback: Callback function to handle decoded audio data
        """

        def handle_audio(sender: any, data: bytes) -> None:
            """Handle raw audio data from Omi device"""
            try:
                # Decode Opus audio to PCM
                pcm_data = self.decoder.decode_packet(data)
                if pcm_data:
                    # Put decoded audio in queue
                    self.audio_queue.put_nowait(pcm_data)
                    # Call the callback
                    on_audio_callback(pcm_data)
            except Exception as e:
                print(f"Error handling audio: {e}")

        try:
            print(f"Connecting to Omi device: {self.device_mac}")

            # Start listening to Omi device
            await listen_to_omi(
                self.device_mac,
                self.audio_char_uuid,
                handle_audio,
            )

            self.is_connected = True
            print("Successfully connected to Omi device")

        except Exception as e:
            print(f"Error connecting to Omi device: {e}")
            self.is_connected = False
            raise

    async def get_audio_stream(self) -> Queue[bytes]:
        """
        Get the audio stream queue

        Returns:
            Queue containing decoded PCM audio chunks
        """
        return self.audio_queue

    async def capture_frame(self) -> Optional[bytes]:
        """
        Capture current camera frame from glasses

        Returns:
            Frame data as bytes, or None if not available
        """
        # Note: The current Omi SDK doesn't expose camera directly
        # This would need to be implemented when camera API is available
        # For now, this is a placeholder
        return self.frame_buffer

    def set_frame(self, frame_data: bytes) -> None:
        """
        Set current camera frame (when camera API becomes available)

        Args:
            frame_data: Raw frame data
        """
        self.frame_buffer = frame_data

    async def disconnect(self) -> None:
        """Disconnect from Omi device"""
        try:
            self.is_connected = False
            print("Disconnected from Omi device")
        except Exception as e:
            print(f"Error disconnecting: {e}")

    def get_connection_status(self) -> bool:
        """Get current connection status"""
        return self.is_connected
