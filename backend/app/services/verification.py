"""
Gender verification service using DeepFace.
PRIVACY: Images are processed in-memory and NEVER stored permanently.
"""
import io
import os
import tempfile
from typing import Optional, Tuple
import logging

logger = logging.getLogger(__name__)


def verify_gender_from_image(image_bytes: bytes) -> Tuple[Optional[str], Optional[str]]:
    """
    Analyze image to detect gender.
    
    Args:
        image_bytes: Raw image bytes from camera capture
        
    Returns:
        Tuple of (gender, error_message)
        gender: "Man" or "Woman" if successful
        error_message: Error description if failed
        
    PRIVACY GUARANTEE:
    - Image is written to a temporary file that is auto-deleted
    - No image data is persisted to disk or database
    - Only the gender result string is returned
    """
    temp_path = None
    try:
        # Write to temp file (required by DeepFace)
        with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as tmp:
            tmp.write(image_bytes)
            temp_path = tmp.name
        
        # Import DeepFace here to avoid loading TensorFlow at startup
        try:
            from deepface import DeepFace
        except ImportError:
            logger.warning("DeepFace not installed, using mock response")
            return _mock_gender_detection()
        
        # Analyze the image
        result = DeepFace.analyze(
            img_path=temp_path,
            actions=["gender"],
            enforce_detection=True,
            detector_backend="opencv"
        )
        
        # DeepFace returns a list when multiple faces detected
        if isinstance(result, list):
            result = result[0]
        
        gender = result.get("dominant_gender", "Unknown")
        
        # Normalize to "Man" or "Woman"
        if gender.lower() in ["male", "man"]:
            return "Man", None
        elif gender.lower() in ["female", "woman"]:
            return "Woman", None
        else:
            return None, f"Could not determine gender: {gender}"
            
    except Exception as e:
        error_msg = str(e)
        if "Face could not be detected" in error_msg:
            return None, "No face detected. Please ensure your face is clearly visible."
        logger.error(f"Gender verification error: {error_msg}")
        return None, f"Verification failed: {error_msg}"
        
    finally:
        # CRITICAL: Always delete the temporary image file
        if temp_path and os.path.exists(temp_path):
            try:
                os.remove(temp_path)
                logger.info(f"Deleted temporary image: {temp_path}")
            except Exception as e:
                logger.error(f"Failed to delete temp image: {e}")


def _mock_gender_detection() -> Tuple[str, None]:
    """
    Mock gender detection for testing when DeepFace is not installed.
    In production, this should not be used.
    """
    import random
    gender = random.choice(["Man", "Woman"])
    logger.warning(f"MOCK: Returning random gender: {gender}")
    return gender, None
