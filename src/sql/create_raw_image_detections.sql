create schema if not exists raw;

create table if not exists raw.image_detections (
  detection_id     bigserial primary key,
  message_id       bigint not null,                     -- FK to raw/public message id 
  image_path       text   not null,
  detected_class   text   not null,
  confidence       double precision,
  bbox_xmin        double precision,
  bbox_ymin        double precision,
  bbox_xmax        double precision,
  bbox_ymax        double precision,
  model_name       text,
  run_ts           timestamptz not null default now()
);

-- helpful indexes
create index if not exists idx_image_detections_msg on raw.image_detections (message_id);
create index if not exists idx_image_detections_class on raw.image_detections (detected_class);
