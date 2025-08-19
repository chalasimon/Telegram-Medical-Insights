from pydantic import BaseModel

class ProductReport(BaseModel):
    product_name: str
    mention_count: int
class ChannelActivity(BaseModel):
    channel_name: str
    daily_posts: int
    weekly_posts: int