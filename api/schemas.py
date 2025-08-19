from pydantic import BaseModel

class ProductReport(BaseModel):
    product_name: str
    mention_count: int
class ChannelActivity(BaseModel):
    channel_id: str
    daily_posts: int
    weekly_posts: int
class MessageSearchResult(BaseModel):
    message_id: int
    channel_id: str
    message: str