with funnel as (
    select ts
         , device_id
         , item
         , pm_stype
         , pm_type
         , section
         , page
         , lag(page, 1) over (partition by device_id order by ts)     as lag_page
    from yeogi_log.user_action_log_basic
    where true
      and (year || month) = '202206'
      and action = 'load'
      and service = 'YG'

), agg as (
    select date(ts) as ymd, device_id, count(1) as view_cnt
    from funnel
    where lag_page = 'list/category/acm'
    group by ymd, device_id
) select ymd, avg(view_cnt) as avg_view_cnt from agg group by ymd order by ymd;

