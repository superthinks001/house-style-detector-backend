import tempfile
from ultralytics import YOLO
from fastapi.responses import JSONResponse
from PIL import Image
import io

# Load the model once when the app starts
model = YOLO("weights/best.pt")

# Load style config
import json
with open("style_config.json", "r") as f:
    STYLE_LABELS = json.load(f)["labels"]

async def run_prediction(file):
    try:
        # Save uploaded image to a temporary location
        contents = await file.read()
        with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as temp_img:
            temp_img.write(contents)
            temp_path = temp_img.name

        # Run YOLOv8 inference
        results = model(temp_path)

        # Assume single object detection per image
        pred = results[0].probs
        predicted_index = int(pred.top1)
        predicted_style = STYLE_LABELS[predicted_index]
        confidence = round(float(pred.top1conf), 4)

        return JSONResponse(
            content={
                "predicted_style": predicted_style,
                "predicted_confidence": confidence
            },
            status_code=200
        )
    except Exception as e:
        return JSONResponse(
            content={"error": str(e)},
            status_code=500
        )
