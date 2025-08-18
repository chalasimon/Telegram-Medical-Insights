with source as (
    select * from raw.raw_telegram_messages
),
renamed as (
    select
        id::bigint as message_id,
        channel_id::bigint,
        sender::text,
        message::text,
        date::timestamp,
        case when media_url is not null then true else false end as has_image
    from source
)
select * from renamed;
