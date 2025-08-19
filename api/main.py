from fastapi import FastAPI

# import schemas and CRUD operations
from .schemas import ProductReport, ChannelActivity, MessageSearchResult
from .crud import get_top_products, get_channel_activity, search_messages

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Telegram Medical Insights API is running!"}
