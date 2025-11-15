"""
Pydantic models for Dadd-E
"""
from datetime import datetime
from enum import Enum
from typing import Any, Optional
from pydantic import BaseModel, Field


class IntentType(str, Enum):
    """Types of user intents"""

    DESCRIBE_SCENE = "describe_scene"
    CHECK_SLACK = "check_slack"
    SEND_EMAIL = "send_email"
    SEARCH_DRIVE = "search_drive"
    CREATE_TASK = "create_task"
    CHECK_CALENDAR = "check_calendar"
    GENERAL_QUERY = "general_query"
    UNKNOWN = "unknown"


class TranscriptionRequest(BaseModel):
    """Request for audio transcription"""

    audio_data: bytes
    user_id: str
    language: str = "en"


class TranscriptionResponse(BaseModel):
    """Response from audio transcription"""

    text: str
    confidence: float
    language: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class VisionRequest(BaseModel):
    """Request for vision analysis"""

    image_data: bytes
    user_id: str
    prompt: Optional[str] = "What do you see in this image?"


class VisionResponse(BaseModel):
    """Response from vision analysis"""

    description: str
    objects: list[str] = []
    text_detected: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class IntentRequest(BaseModel):
    """Request for intent classification"""

    text: str
    user_id: str
    context: Optional[dict[str, Any]] = None


class IntentResponse(BaseModel):
    """Response from intent classification"""

    intent: IntentType
    confidence: float
    entities: dict[str, Any] = {}
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class ActionRequest(BaseModel):
    """Request to execute an action"""

    intent: IntentType
    user_id: str
    parameters: dict[str, Any] = {}
    context: Optional[dict[str, Any]] = None


class ActionResponse(BaseModel):
    """Response from action execution"""

    success: bool
    message: str
    data: Optional[dict[str, Any]] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class SessionState(BaseModel):
    """User session state"""

    user_id: str
    session_id: str
    context: dict[str, Any] = {}
    last_intent: Optional[IntentType] = None
    conversation_history: list[dict[str, str]] = []
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class DeviceStatus(BaseModel):
    """Omi device status"""

    device_id: str
    user_id: str
    is_connected: bool
    battery_level: Optional[int] = None
    last_seen: datetime = Field(default_factory=datetime.utcnow)


class UserProfile(BaseModel):
    """User profile"""

    user_id: str
    email: str
    name: Optional[str] = None
    connected_apps: list[str] = []
    preferences: dict[str, Any] = {}
    created_at: datetime = Field(default_factory=datetime.utcnow)
