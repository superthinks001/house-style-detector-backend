from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from app.predictor import run_prediction
from app.feedback import save_feedback

app = FastAPI()

# Enable frontend-backend connection
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace with specific domain for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/predict")
async def predict_style(file: UploadFile = File(...)):
    return await run_prediction(file)

@app.post("/feedback")
async def submit_feedback(data: dict):
    return save_feedback(data)
