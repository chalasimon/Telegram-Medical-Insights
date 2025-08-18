with source as (
    select * from raw.telegram_messages
),
renamed as (
    select
        id::bigint as message_id,
        channel_username,
        channel_title,
        text as message,
        date,
        views,
        case when media_path is not null then true else false end as has_image
    from source
)
select * from renamed
