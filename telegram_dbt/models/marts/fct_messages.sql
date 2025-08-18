select
    message_id,
    channel_username,
    channel_title,
    message,
    date,
    views,
    has_image
from {{ ref('stg_telegram_messages') }}
