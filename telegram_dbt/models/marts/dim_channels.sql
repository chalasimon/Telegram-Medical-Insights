select distinct
    channel_username as channel_id,
    channel_title as channel_name
from {{ ref('stg_telegram_messages') }}