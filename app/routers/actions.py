"""
Action endpoints for executing tasks via Composio integrations
"""
from fastapi import APIRouter, HTTPException
from app.services.integrations import IntegrationService
from app.services.vision import VisionService
from app.services.database import DatabaseService
from app.models.schemas import ActionRequest, ActionResponse, IntentType

router = APIRouter(prefix="/actions", tags=["actions"])


@router.post("/execute", response_model=ActionResponse)
async def execute_action(request: ActionRequest) -> ActionResponse:
    """
    Execute an action based on user intent

    Args:
        request: Action request with intent and parameters

    Returns:
        Action execution result
    """
    try:
        integration_service = IntegrationService()
        vision_service = VisionService()
        db_service = DatabaseService()

        result_message = ""
        result_data = {}

        # Route to appropriate action handler
        if request.intent == IntentType.CHECK_SLACK:
            channel = request.parameters.get("channel", "general")
            slack_result = await integration_service.check_slack_messages(
                request.user_id, channel
            )

            if "error" in slack_result:
                result_message = f"Error checking Slack: {slack_result['error']}"
            else:
                messages = slack_result.get("messages", [])
                if messages:
                    # Format messages for response
                    msg_summary = []
                    for msg in messages[:5]:  # Top 5 messages
                        user = msg.get("user", "Unknown")
                        text = msg.get("text", "")
                        msg_summary.append(f"{user}: {text}")

                    result_message = (
                        f"Here are recent messages from #{channel}:\n"
                        + "\n".join(msg_summary)
                    )
                    result_data = {"messages": messages[:5]}
                else:
                    result_message = f"No recent messages in #{channel}"

        elif request.intent == IntentType.SEND_EMAIL:
            to = request.parameters.get("to", "")
            subject = request.parameters.get("subject", "")
            body = request.parameters.get("body", "")
            attachment_url = request.parameters.get("attachment_url")

            if not to or not subject:
                raise HTTPException(
                    status_code=400,
                    detail="Missing required parameters: 'to' and 'subject'",
                )

            email_result = await integration_service.send_email(
                request.user_id, to, subject, body, attachment_url
            )

            if email_result.get("success", False):
                result_message = f"Email sent successfully to {to}"
                result_data = email_result
            else:
                result_message = f"Failed to send email: {email_result.get('error')}"

        elif request.intent == IntentType.SEARCH_DRIVE:
            query = request.parameters.get("query", "")
            if not query:
                raise HTTPException(status_code=400, detail="Missing 'query' parameter")

            drive_result = await integration_service.search_google_drive(
                request.user_id, query
            )

            if "error" in drive_result:
                result_message = f"Error searching Drive: {drive_result['error']}"
            else:
                files = drive_result.get("files", [])
                if files:
                    file_names = [f['name'] for f in files[:5]]
                    result_message = (
                        f"Found {len(files)} files. Top results: "
                        + ", ".join(file_names)
                    )
                    result_data = {"files": files[:5]}
                else:
                    result_message = f"No files found for '{query}'"

        elif request.intent == IntentType.CREATE_TASK:
            title = request.parameters.get("title", "")
            content = request.parameters.get("content", "")
            database_id = request.parameters.get("database_id", "")

            if not title:
                raise HTTPException(status_code=400, detail="Missing 'title' parameter")

            task_result = await integration_service.create_notion_task(
                request.user_id, title, content, database_id
            )

            if task_result.get("success", False):
                result_message = f"Task '{title}' created successfully"
                result_data = task_result
            else:
                result_message = f"Failed to create task: {task_result.get('error')}"

        elif request.intent == IntentType.CHECK_CALENDAR:
            time_min = request.parameters.get("time_min", "")
            time_max = request.parameters.get("time_max", "")

            cal_result = await integration_service.get_calendar_events(
                request.user_id, time_min, time_max
            )

            if "error" in cal_result:
                result_message = f"Error checking calendar: {cal_result['error']}"
            else:
                events = cal_result.get("events", [])
                if events:
                    event_summary = []
                    for event in events[:5]:
                        summary = event.get("summary", "Untitled")
                        start = event.get("start", {}).get("dateTime", "")
                        event_summary.append(f"{summary} at {start}")

                    result_message = "Upcoming events:\n" + "\n".join(event_summary)
                    result_data = {"events": events[:5]}
                else:
                    result_message = "No upcoming events"

        else:
            # For general queries or unknown intents
            response_text = await vision_service.generate_response(
                request.parameters.get("text", ""),
                context=request.context,
            )
            result_message = response_text

        # Log action to database
        await db_service.log_action(
            {
                "user_id": request.user_id,
                "action_type": request.intent.value,
                "parameters": request.parameters,
                "result": result_message,
            }
        )

        return ActionResponse(
            success=True,
            message=result_message,
            data=result_data if result_data else None,
        )

    except Exception as e:
        print(f"Error executing action: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/complex-task")
async def execute_complex_task(
    user_id: str,
    task_description: str,
) -> ActionResponse:
    """
    Execute a complex multi-step task

    Example: "Check my Slack for messages from Sai about proposal,
    find the proposal doc in Drive, and email it to him"

    Args:
        user_id: User ID
        task_description: Natural language description of the task

    Returns:
        Execution result
    """
    try:
        vision_service = VisionService()
        integration_service = IntegrationService()
        db_service = DatabaseService()

        # Decompose task into subtasks
        subtasks = await vision_service.decompose_task(task_description)

        if not subtasks:
            return ActionResponse(
                success=False,
                message="Could not understand the task. Please try rephrasing.",
            )

        results = []

        # Execute each subtask
        for subtask in subtasks:
            action = subtask.get("action", "")
            description = subtask.get("description", "")
            params = subtask.get("parameters", {})

            # Map action to intent
            intent_map = {
                "check_slack": IntentType.CHECK_SLACK,
                "send_email": IntentType.SEND_EMAIL,
                "search_drive": IntentType.SEARCH_DRIVE,
                "create_task": IntentType.CREATE_TASK,
            }

            intent = intent_map.get(action, IntentType.GENERAL_QUERY)

            # Execute subtask
            request = ActionRequest(
                intent=intent,
                user_id=user_id,
                parameters=params,
            )

            result = await execute_action(request)
            results.append(
                {
                    "description": description,
                    "result": result.message,
                    "success": result.success,
                }
            )

        # Create summary
        summary = f"Completed {len(subtasks)} tasks:\n"
        for i, r in enumerate(results, 1):
            summary += f"{i}. {r['description']}: {r['result']}\n"

        return ActionResponse(
            success=True,
            message=summary,
            data={"subtasks": results},
        )

    except Exception as e:
        print(f"Error executing complex task: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/connected-apps")
async def get_connected_apps(user_id: str) -> dict[str, list[str]]:
    """
    Get list of connected apps for a user

    Args:
        user_id: User ID

    Returns:
        List of connected app names
    """
    try:
        integration_service = IntegrationService()
        apps = integration_service.get_connected_accounts(user_id)

        return {
            "user_id": user_id,
            "connected_apps": apps,
        }

    except Exception as e:
        print(f"Error getting connected apps: {e}")
        raise HTTPException(status_code=500, detail=str(e))
