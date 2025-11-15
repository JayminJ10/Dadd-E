"""
OpenAI vision and LLM service
"""
import base64
from typing import Any, Optional
from openai import AsyncOpenAI
from app.core.config import get_settings
from app.models.schemas import IntentType


class VisionService:
    """Service for vision analysis and LLM reasoning using OpenAI"""

    def __init__(self) -> None:
        settings = get_settings()
        self.client = AsyncOpenAI(api_key=settings.openai_api_key)
        self.settings = settings

    async def analyze_image(
        self, image_data: bytes, prompt: str = "What do you see in this image?"
    ) -> dict[str, Any]:
        """
        Analyze an image using GPT-4 Vision

        Args:
            image_data: Raw image bytes
            prompt: Question to ask about the image

        Returns:
            Dictionary containing description and extracted information
        """
        try:
            # Encode image to base64
            base64_image = base64.b64encode(image_data).decode("utf-8")

            # Call GPT-4 Vision
            response = await self.client.chat.completions.create(
                model=self.settings.vision_model,
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": prompt},
                            {
                                "type": "image_url",
                                "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"},
                            },
                        ],
                    }
                ],
                max_tokens=500,
            )

            description = response.choices[0].message.content or ""

            return {
                "description": description,
                "model": self.settings.vision_model,
                "prompt": prompt,
            }

        except Exception as e:
            print(f"Error analyzing image: {e}")
            raise

    async def classify_intent(
        self, text: str, context: Optional[dict[str, Any]] = None
    ) -> dict[str, Any]:
        """
        Classify user intent from transcribed text

        Args:
            text: User's transcribed speech
            context: Optional conversation context

        Returns:
            Dictionary with intent type, confidence, and extracted entities
        """
        try:
            system_prompt = """You are an intent classifier for Dadd-E, a productivity assistant.
Classify the user's intent into one of these categories:
- DESCRIBE_SCENE: User wants to know what's in front of them
- CHECK_SLACK: User wants to check Slack messages
- SEND_EMAIL: User wants to send an email
- SEARCH_DRIVE: User wants to search Google Drive
- CREATE_TASK: User wants to create a task/note
- CHECK_CALENDAR: User wants to check calendar
- GENERAL_QUERY: General question or conversation
- UNKNOWN: Cannot determine intent

Respond in JSON format:
{
  "intent": "INTENT_NAME",
  "confidence": 0.95,
  "entities": {"key": "value"}
}"""

            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"User said: {text}"},
            ]

            if context:
                messages.insert(
                    1, {"role": "system", "content": f"Context: {context}"}
                )

            response = await self.client.chat.completions.create(
                model=self.settings.openai_model,
                messages=messages,
                response_format={"type": "json_object"},
                temperature=0.3,
            )

            result = response.choices[0].message.content
            if result:
                import json

                return json.loads(result)

            return {
                "intent": "UNKNOWN",
                "confidence": 0.0,
                "entities": {},
            }

        except Exception as e:
            print(f"Error classifying intent: {e}")
            return {
                "intent": "UNKNOWN",
                "confidence": 0.0,
                "entities": {},
            }

    async def generate_response(
        self,
        user_message: str,
        context: Optional[dict[str, Any]] = None,
        system_prompt: Optional[str] = None,
    ) -> str:
        """
        Generate a conversational response

        Args:
            user_message: User's message
            context: Conversation context
            system_prompt: Custom system prompt

        Returns:
            Generated response text
        """
        try:
            default_system = """You are Dadd-E, a helpful productivity assistant.
You help users with their work by checking messages, sending emails, searching documents,
and providing information about their surroundings. Be concise and friendly."""

            messages = [
                {"role": "system", "content": system_prompt or default_system},
            ]

            if context and context.get("conversation_history"):
                messages.extend(context["conversation_history"])

            messages.append({"role": "user", "content": user_message})

            response = await self.client.chat.completions.create(
                model=self.settings.openai_model,
                messages=messages,
                temperature=0.7,
                max_tokens=150,
            )

            return response.choices[0].message.content or ""

        except Exception as e:
            print(f"Error generating response: {e}")
            return "I'm sorry, I couldn't process that request."

    async def decompose_task(self, task_description: str) -> list[dict[str, Any]]:
        """
        Break down a complex task into subtasks

        Args:
            task_description: Description of the complex task

        Returns:
            List of subtasks with actions and parameters
        """
        try:
            prompt = f"""Break down this task into specific subtasks:
"{task_description}"

Return a JSON array of subtasks, each with:
- action: The action to take (e.g., "search_drive", "send_email")
- description: What to do
- parameters: Required parameters

Example:
[
  {{"action": "search_drive", "description": "Find proposal doc", "parameters": {{"query": "proposal"}}}},
  {{"action": "send_email", "description": "Email the doc to Sai", "parameters": {{"to": "sai", "subject": "Proposal"}}}}
]"""

            response = await self.client.chat.completions.create(
                model=self.settings.openai_model,
                messages=[{"role": "user", "content": prompt}],
                response_format={"type": "json_object"},
                temperature=0.3,
            )

            result = response.choices[0].message.content
            if result:
                import json

                parsed = json.loads(result)
                return parsed.get("subtasks", [])

            return []

        except Exception as e:
            print(f"Error decomposing task: {e}")
            return []
