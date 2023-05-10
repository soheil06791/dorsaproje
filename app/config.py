import redis


limit_time = 3600
limit_request_count = 100
limit_wrong_request_count = 15
redis_cache = redis.Redis(host='127.0.0.1', port='6379', db='0')