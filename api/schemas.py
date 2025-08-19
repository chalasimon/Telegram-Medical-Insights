from pydantic import BaseModel

class ProductReport(BaseModel):
    product_name: str
    mention_count: int