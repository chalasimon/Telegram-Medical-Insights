from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Telegram Medical Insights API is running!"}
