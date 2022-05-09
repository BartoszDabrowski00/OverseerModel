from overseer.web.app import get_cfg

celery_cfg = get_cfg().get('celery')

broker_url = celery_cfg.get('broker_url')

redis_db = celery_cfg.get('redis_db')
redis_host = celery_cfg.get('redis_url')
redis_port = celery_cfg.get('redis_port')
result_backend = celery_cfg.get('backend')
task_serializer = celery_cfg.get('serializer')
