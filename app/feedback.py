from google.cloud import bigquery
from google.oauth2 import service_account
import os
from fastapi.responses import JSONResponse
from datetime import datetime

# Use your JSON key filename here or from env var
KEY_PATH = "keys/ai-architectural-classifier-e1c42811d822.json"

credentials = service_account.Credentials.from_service_account_file(KEY_PATH)
client = bigquery.Client(credentials=credentials, project=credentials.project_id)

TABLE_ID = "ai-architectural-classifier.house_style_feedback.user_feedback"

def save_feedback(data: dict):
    try:
        row = {
            "image_id": data["image_id"],
            "image_name": data["image_name"],
            "predicted_style": data["predicted_style"],
            "predicted_confidence": float(data["predicted_confidence"]),
            "is_correct": data["is_correct"],
            "correct_style": data.get("correct_style", None),
            "timestamp": datetime.utcnow()
        }

        errors = client.insert_rows_json(TABLE_ID, [row])
        if errors == []:
            return JSONResponse(content={"message": "Feedback saved successfully"}, status_code=200)
        else:
            return JSONResponse(content={"error": errors}, status_code=500)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
