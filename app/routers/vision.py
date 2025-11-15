"""
Vision endpoints for image analysis
"""
from fastapi import APIRouter, UploadFile, File, HTTPException
from app.services.vision import VisionService
from app.services.database import DatabaseService
from app.models.schemas import VisionResponse

router = APIRouter(prefix="/vision", tags=["vision"])


@router.post("/analyze", response_model=VisionResponse)
async def analyze_scene(
    user_id: str,
    image: UploadFile = File(...),
    prompt: str = "What do you see in this image?",
) -> VisionResponse:
    """
    Analyze an image from the Omi glasses camera

    Args:
        user_id: User ID
        image: Image file to analyze
        prompt: Question about the image

    Returns:
        Vision analysis result
    """
    try:
        vision_service = VisionService()
        db_service = DatabaseService()

        # Read image data
        image_data = await image.read()

        # Analyze image
        result = await vision_service.analyze_image(image_data, prompt)

        # Log to database
        await db_service.log_vision_analysis(
            {
                "user_id": user_id,
                "prompt": prompt,
                "description": result["description"],
                "model": result["model"],
            }
        )

        return VisionResponse(
            description=result["description"],
            objects=[],  # Can be enhanced with object detection
            text_detected=None,  # Can be enhanced with OCR
        )

    except Exception as e:
        print(f"Error analyzing image: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/describe")
async def describe_scene(
    user_id: str,
    image: UploadFile = File(...),
) -> dict[str, str]:
    """
    Simple endpoint to describe what's in front of the user

    Args:
        user_id: User ID
        image: Image from glasses camera

    Returns:
        Description of the scene
    """
    try:
        vision_service = VisionService()

        # Read image data
        image_data = await image.read()

        # Analyze with default prompt
        result = await vision_service.analyze_image(
            image_data,
            "Describe what you see in this image in 2-3 sentences. "
            "Focus on the main objects, people, and context.",
        )

        return {
            "user_id": user_id,
            "description": result["description"],
        }

    except Exception as e:
        print(f"Error describing scene: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/read-text")
async def read_text(
    user_id: str,
    image: UploadFile = File(...),
) -> dict[str, str]:
    """
    Extract and read text from an image

    Args:
        user_id: User ID
        image: Image containing text

    Returns:
        Extracted text
    """
    try:
        vision_service = VisionService()

        # Read image data
        image_data = await image.read()

        # Analyze with OCR-focused prompt
        result = await vision_service.analyze_image(
            image_data,
            "Extract and list all visible text from this image. "
            "Maintain the original formatting and order.",
        )

        return {
            "user_id": user_id,
            "text": result["description"],
        }

    except Exception as e:
        print(f"Error reading text: {e}")
        raise HTTPException(status_code=500, detail=str(e))
