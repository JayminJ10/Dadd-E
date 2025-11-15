"""
Supabase database service
"""
from datetime import datetime
from typing import Any, Optional
from supabase import create_client, Client
from app.core.config import get_settings
from app.models.schemas import UserProfile, SessionState, DeviceStatus


class DatabaseService:
    """Service for database operations using Supabase"""

    def __init__(self) -> None:
        settings = get_settings()
        self.client: Client = create_client(settings.supabase_url, settings.supabase_key)

    # User Management
    async def get_user(self, user_id: str) -> Optional[dict[str, Any]]:
        """Get user profile by ID"""
        try:
            response = self.client.table("users").select("*").eq("user_id", user_id).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            print(f"Error getting user: {e}")
            return None

    async def create_user(self, user_data: dict[str, Any]) -> Optional[dict[str, Any]]:
        """Create a new user profile"""
        try:
            response = self.client.table("users").insert(user_data).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            print(f"Error creating user: {e}")
            return None

    async def update_user(
        self, user_id: str, updates: dict[str, Any]
    ) -> Optional[dict[str, Any]]:
        """Update user profile"""
        try:
            updates["updated_at"] = datetime.utcnow().isoformat()
            response = (
                self.client.table("users")
                .update(updates)
                .eq("user_id", user_id)
                .execute()
            )
            return response.data[0] if response.data else None
        except Exception as e:
            print(f"Error updating user: {e}")
            return None

    # Session Management
    async def create_session(self, session_data: dict[str, Any]) -> Optional[dict[str, Any]]:
        """Create a new session"""
        try:
            response = self.client.table("sessions").insert(session_data).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            print(f"Error creating session: {e}")
            return None

    async def get_session(
        self, user_id: str, session_id: str
    ) -> Optional[dict[str, Any]]:
        """Get session by user ID and session ID"""
        try:
            response = (
                self.client.table("sessions")
                .select("*")
                .eq("user_id", user_id)
                .eq("session_id", session_id)
                .execute()
            )
            return response.data[0] if response.data else None
        except Exception as e:
            print(f"Error getting session: {e}")
            return None

    async def update_session(
        self, session_id: str, updates: dict[str, Any]
    ) -> Optional[dict[str, Any]]:
        """Update session state"""
        try:
            updates["updated_at"] = datetime.utcnow().isoformat()
            response = (
                self.client.table("sessions")
                .update(updates)
                .eq("session_id", session_id)
                .execute()
            )
            return response.data[0] if response.data else None
        except Exception as e:
            print(f"Error updating session: {e}")
            return None

    async def get_active_session(self, user_id: str) -> Optional[dict[str, Any]]:
        """Get the most recent active session for a user"""
        try:
            response = (
                self.client.table("sessions")
                .select("*")
                .eq("user_id", user_id)
                .order("updated_at", desc=True)
                .limit(1)
                .execute()
            )
            return response.data[0] if response.data else None
        except Exception as e:
            print(f"Error getting active session: {e}")
            return None

    # Device Management
    async def register_device(
        self, device_data: dict[str, Any]
    ) -> Optional[dict[str, Any]]:
        """Register a new device"""
        try:
            response = self.client.table("devices").insert(device_data).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            print(f"Error registering device: {e}")
            return None

    async def update_device_status(
        self, device_id: str, status: dict[str, Any]
    ) -> Optional[dict[str, Any]]:
        """Update device status"""
        try:
            status["last_seen"] = datetime.utcnow().isoformat()
            response = (
                self.client.table("devices")
                .update(status)
                .eq("device_id", device_id)
                .execute()
            )
            return response.data[0] if response.data else None
        except Exception as e:
            print(f"Error updating device status: {e}")
            return None

    async def get_user_devices(self, user_id: str) -> list[dict[str, Any]]:
        """Get all devices for a user"""
        try:
            response = (
                self.client.table("devices").select("*").eq("user_id", user_id).execute()
            )
            return response.data if response.data else []
        except Exception as e:
            print(f"Error getting user devices: {e}")
            return []

    # Action History
    async def log_action(self, action_data: dict[str, Any]) -> Optional[dict[str, Any]]:
        """Log an action to history"""
        try:
            response = self.client.table("action_history").insert(action_data).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            print(f"Error logging action: {e}")
            return None

    async def get_action_history(
        self, user_id: str, limit: int = 50
    ) -> list[dict[str, Any]]:
        """Get action history for a user"""
        try:
            response = (
                self.client.table("action_history")
                .select("*")
                .eq("user_id", user_id)
                .order("timestamp", desc=True)
                .limit(limit)
                .execute()
            )
            return response.data if response.data else []
        except Exception as e:
            print(f"Error getting action history: {e}")
            return []

    # Vision Logs
    async def log_vision_analysis(
        self, vision_data: dict[str, Any]
    ) -> Optional[dict[str, Any]]:
        """Log a vision analysis"""
        try:
            response = self.client.table("vision_logs").insert(vision_data).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            print(f"Error logging vision analysis: {e}")
            return None
