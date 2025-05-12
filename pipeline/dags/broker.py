import json
from typing import Dict, List, Optional
from datetime import datetime
from redis import RedisError
from redis.client import Redis
from redis.exceptions import ResponseError
from airflow.providers.redis.hooks.redis import RedisHook


class Broker:
    redis_connection_id: str
    conn: Redis

    def __init__(self, *, redis_connection_id: str = "my-redis") -> None:
        self.redis_connection_id = redis_connection_id
    

    def create_connection(self) -> Redis:
        self.conn = RedisHook(redis_conn_id=self.redis_connection_id).get_conn()
    

    def create_xgroup(self, stream_name: str, group_name: str):
        try:
            self.conn.xgroup_create(stream_name, group_name, id='0', mkstream=True)
        
        except ResponseError as e:
            if "BUSYGROUP" in str(e):
                print(f'Consumer group {group_name} already exists on {stream_name}.')

        return
    
    
    def _decode(self, entry_id, fields: Dict[bytes, bytes]) -> Dict:
        decoded_fields = {k.decode(): v.decode() for k, v in fields.items()}
        data = decoded_fields.get('data')
        
        result = json.loads(data)
        result['entry_id'] = entry_id.decode()
        
        return result
    

    def ack(self, stream_name: str, group_name: str, *entry_ids: str):
        return self.conn.xack(stream_name, group_name, *entry_ids)


    def read(self, stream_name: str, group_name: str, consumer_name: str, batch_size: int, block_time_ms: int) -> Optional[List[Dict]]:
        messages = self.conn.xreadgroup(
            group_name,
            consumer_name,
            {stream_name: '>'},
            count=batch_size,
            block=block_time_ms
        )

        if not messages or not messages[0][1]:
            return None
        
        decoded_messages = []
        
        for stream_name, entries in messages:
            for entry_id, fields in entries:
                decoded_messages.append(self._decode(entry_id, fields))

        return decoded_messages

    
    def write(self, stream_name: str, obj: Dict):
        try:
            self.conn.xadd(stream_name, {'data': json.dumps(obj)})
        
        except RedisError as e:
            print(f'Failed to push to Redis stream {stream_name}: {e}')
            raise

        return
    

    def write_pipeline(self, stream_name: str, *objs: Dict):
        pipeline = self.conn.pipeline()

        for obj in objs:
            pipeline.xadd(stream_name, {'data': json.dumps(obj)})
        
        return pipeline.execute()
    

    def xtrim(self, stream_name: str, stream_len: int):
        return self.conn.xtrim(stream_name, maxlen=stream_len)
    

    def xdel(self, stream_name: str, *entry_ids: str):
        return self.conn.xdel(stream_name, *entry_ids)