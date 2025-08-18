select distinct
    date::date as date,
    extract(year from date) as year,
    extract(month from date) as month,
    extract(day from date) as day,
    extract(week from date) as week
from {{ ref('stg_telegram_messages') }};
