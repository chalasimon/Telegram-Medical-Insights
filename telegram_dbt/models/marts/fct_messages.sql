select
    m.message_id,
    m.channel_id,
    m.date::date as date,
    length(m.message) as message_length,
    m.has_image
from {{ ref('stg_telegram_messages') }} m;
