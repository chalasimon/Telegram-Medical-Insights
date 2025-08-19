from fastapi import FastAPI

# import schemas and CRUD operations
from .schemas import ProductReport, ChannelActivity, MessageSearchResult
from .crud import get_top_products, get_channel_activity, search_messages

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Telegram Medical Insights API is running!"}


# to get top 10 products
from fastapi import HTTPException

@app.get("/api/reports/top-products", response_model=list[ProductReport])
def top_products(limit: int = 10):
    try:
        return get_top_products(limit)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# to get channel activity
@app.get("/api/channels/{channel_id}/activity", response_model=ChannelActivity)
def channel_activity(channel_id: str):
    return get_channel_activity(channel_id)

# to search messages
@app.get("/api/search/messages", response_model=list[MessageSearchResult])
def search_messages_endpoint(query: str):
    return search_messages(query)