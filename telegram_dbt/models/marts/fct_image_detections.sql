select
  d.detection_id,
  d.message_id,
  m.channel_username,
  m.channel_title,
  d.detected_object_class,
  d.confidence_score,
  d.image_path,
  d.model_name,
  d.run_ts
from {{ ref('stg_image_detections') }} d
left join {{ ref('fct_messages') }} m
  on m.message_id = d.message_id
