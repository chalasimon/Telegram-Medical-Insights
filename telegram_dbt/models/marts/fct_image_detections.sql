with messages as (
    select
        message_id,
        channel_id as channel_username
       -- channel_title
    from {{ ref('fct_messages') }}
),
detections as (
    select
        *
    from {{ ref('stg_image_detections') }} d
)
select
    d.message_id,
    d.detection_id,
    m.channel_username,
    --d.channel_title,
    d.image_path,
    d.detected_class,
    d.confidence,
    d.bbox_xmin,
    d.bbox_ymin,
    d.bbox_xmax,
    d.bbox_ymax,
    d.model_name
from detections d
left join messages m
    on d.message_id = m.message_id

