-- models/staging/stg_image_detections.sql
select
    detection_id,
    message_id,
    image_path,
    detected_class,
    confidence,
    bbox_xmin,
    bbox_ymin,
    bbox_xmax,
    bbox_ymax,
    model_name
from raw.image_detections

