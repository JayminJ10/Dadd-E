"""
Composio integration service for app connections
"""
from typing import Any, Optional
from app.core.config import get_settings


class IntegrationService:
    """Service for managing app integrations via Composio"""

    def __init__(self) -> None:
        try:
            # Lazy import to avoid dependency issues
            from composio_openai import ComposioToolSet
            settings = get_settings()
            self.toolset = ComposioToolSet(api_key=settings.composio_api_key)
        except ImportError as e:
            raise ImportError(
                f"Composio not available: {e}. "
                "Integration features disabled for now."
            ) from e

    async def check_slack_messages(
        self, user_id: str, channel: str = "general"
    ) -> dict[str, Any]:
        """
        Check Slack messages in a specific channel

        Args:
            user_id: User ID for authentication
            channel: Slack channel name

        Returns:
            Dictionary containing messages
        """
        try:
            # Get Slack tools
            tools = self.toolset.get_tools(apps=[App.SLACK])

            # Get messages from channel
            result = self.toolset.execute_action(
                action=Action.SLACK_CONVERSATIONS_HISTORY,
                params={"channel": channel, "limit": 10},
                entity_id=user_id,
            )

            return result

        except Exception as e:
            print(f"Error checking Slack messages: {e}")
            return {"error": str(e), "messages": []}

    async def send_email(
        self,
        user_id: str,
        to: str,
        subject: str,
        body: str,
        attachment_url: Optional[str] = None,
    ) -> dict[str, Any]:
        """
        Send an email via Gmail

        Args:
            user_id: User ID for authentication
            to: Recipient email
            subject: Email subject
            body: Email body
            attachment_url: Optional attachment URL

        Returns:
            Result of email send operation
        """
        try:
            params = {
                "to": to,
                "subject": subject,
                "body": body,
            }

            if attachment_url:
                params["attachment_url"] = attachment_url

            result = self.toolset.execute_action(
                action=Action.GMAIL_SEND_EMAIL,
                params=params,
                entity_id=user_id,
            )

            return result

        except Exception as e:
            print(f"Error sending email: {e}")
            return {"error": str(e), "success": False}

    async def search_google_drive(
        self, user_id: str, query: str, max_results: int = 10
    ) -> dict[str, Any]:
        """
        Search Google Drive for files

        Args:
            user_id: User ID for authentication
            query: Search query
            max_results: Maximum number of results

        Returns:
            Dictionary containing search results
        """
        try:
            result = self.toolset.execute_action(
                action=Action.GOOGLEDRIVE_SEARCH_FILES,
                params={"query": query, "pageSize": max_results},
                entity_id=user_id,
            )

            return result

        except Exception as e:
            print(f"Error searching Google Drive: {e}")
            return {"error": str(e), "files": []}

    async def get_file_url(self, user_id: str, file_id: str) -> Optional[str]:
        """
        Get shareable URL for a Google Drive file

        Args:
            user_id: User ID for authentication
            file_id: Google Drive file ID

        Returns:
            Shareable URL or None
        """
        try:
            result = self.toolset.execute_action(
                action=Action.GOOGLEDRIVE_GET_FILE,
                params={"fileId": file_id},
                entity_id=user_id,
            )

            return result.get("webViewLink") or result.get("webContentLink")

        except Exception as e:
            print(f"Error getting file URL: {e}")
            return None

    async def create_notion_task(
        self, user_id: str, title: str, content: str, database_id: str
    ) -> dict[str, Any]:
        """
        Create a task in Notion

        Args:
            user_id: User ID for authentication
            title: Task title
            content: Task content
            database_id: Notion database ID

        Returns:
            Created task information
        """
        try:
            result = self.toolset.execute_action(
                action=Action.NOTION_CREATE_PAGE,
                params={
                    "parent": {"database_id": database_id},
                    "properties": {
                        "Name": {"title": [{"text": {"content": title}}]},
                    },
                    "children": [
                        {
                            "object": "block",
                            "type": "paragraph",
                            "paragraph": {"rich_text": [{"text": {"content": content}}]},
                        }
                    ],
                },
                entity_id=user_id,
            )

            return result

        except Exception as e:
            print(f"Error creating Notion task: {e}")
            return {"error": str(e), "success": False}

    async def get_calendar_events(
        self, user_id: str, time_min: str, time_max: str
    ) -> dict[str, Any]:
        """
        Get calendar events from Google Calendar

        Args:
            user_id: User ID for authentication
            time_min: Start time (ISO 8601 format)
            time_max: End time (ISO 8601 format)

        Returns:
            Dictionary containing calendar events
        """
        try:
            result = self.toolset.execute_action(
                action=Action.GOOGLECALENDAR_LIST_EVENTS,
                params={"timeMin": time_min, "timeMax": time_max},
                entity_id=user_id,
            )

            return result

        except Exception as e:
            print(f"Error getting calendar events: {e}")
            return {"error": str(e), "events": []}

    def get_connected_accounts(self, user_id: str) -> list[str]:
        """
        Get list of connected accounts for a user

        Args:
            user_id: User ID

        Returns:
            List of connected app names
        """
        try:
            connections = self.toolset.get_entity(entity_id=user_id).connected_accounts
            return [conn.app for conn in connections]
        except Exception as e:
            print(f"Error getting connected accounts: {e}")
            return []
