with src as (
    select
        detection_id,
        message_id::bigint                                  as message_id,
        image_path::text                                    as image_path,
        detected_class::text                                as detected_object_class,
        confidence::double precision                        as confidence_score,
        bbox_xmin::double precision                         as bbox_xmin,
        bbox_ymin::double precision                         as bbox_ymin,
        bbox_xmax::double precision                         as bbox_xmax,
        bbox_ymax::double precision                         as bbox_ymax,
        model_name::text                                    as model_name,
        run_ts
    from raw.image_detections
)
select * from src
