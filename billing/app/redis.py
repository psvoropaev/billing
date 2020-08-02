import json

from aredis import StrictRedis

from billing.app.config import config

redis_client = StrictRedis(host=config.REDIS_HOST, port=config.REDIS_PORT, db=config.REDIS_DB)


async def cache_data_payments(*args, correlation_id, **kwargs):
    dump_params = json.dumps({'args': args, 'kwargs': kwargs})
    if not await redis_client.sismember('queue_retry', correlation_id):
        await redis_client.sadd(config.QUEUE_RETRY, correlation_id)
        await redis_client.set(correlation_id, dump_params)
        await redis_client.save()


async def del_cache_data_payments(correlation_id: str):
    await redis_client.delete(correlation_id)
    await redis_client.srem(config.QUEUE_RETRY, correlation_id)
    await redis_client.save()


async def run_errors_payments(async_handler):
    tasks = await redis_client.smembers(config.QUEUE_RETRY)
    for correlation_id in tasks:
        data = json.loads(await redis_client.get(correlation_id))
        args = data.get('args', [])
        kwargs = data.get('kwargs', {})
        await async_handler(*args, correlation_id=correlation_id, **kwargs)