from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework import status
from .config import redis_cache, limit_wrong_request_count, limit_time
from .models import BlockIp
from .utils import user_limiter

def render_response(data):
    response = data if isinstance(data, Response) else Response(data=data, status= status.HTTP_400_BAD_REQUEST)
    response.accepted_renderer = JSONRenderer()
    response.accepted_media_type = "application/json"
    response.renderer_context = {}
    response.render()
    return response


def inputmiddleware(get_response):
    def middleware(request: Request):
        methods = request.method
        params = request.GET.dict() if methods == 'GET' else None
        bad_request = False
        if not request.user.is_authenticated and '/admin' not in request.path:
            if '/sum' in request.path :
                try:
                    int(params['a'])
                    int(params['b'])
                except:
                    bad_request = True
            else:
                bad_request = True
        if bad_request:
            user_ip = request.META.get('REMOTE_ADDR')
            user_ip_obj = BlockIp.objects
            _key = user_ip + '|wrong'
            resp = user_limiter(user_ip, _key, limit_wrong_request_count, user_ip_obj)
            if isinstance(resp, Response):
                return render_response(resp)
            counter_ = redis_cache.incrby(_key, amount=1)
            if counter_ == limit_wrong_request_count and not user_ip_obj.filter(ip=user_ip).exists():
                user_ip_obj.create(ip=user_ip)
            return render_response({"detail": "Bad Request"})
        return get_response(request)
    return middleware