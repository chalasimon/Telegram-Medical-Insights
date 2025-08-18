select
    m.message_id,
    c.channel_id,
    m.date,
    m.views,
    m.has_image,
    m.message
from {{ ref('stg_telegram_messages') }} m
left join {{ ref('dim_channels') }} c
    on m.channel_username = c.channel_id
