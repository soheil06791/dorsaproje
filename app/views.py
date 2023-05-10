from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework import generics
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Sum
from .models import DataModel, BlockIp
from .serializer import DataModelSerializer
from .config import redis_cache, limit_time, limit_request_count
from .permissions import JustAdminPermission
from .utils import user_limiter

# Create your views here.

@api_view(http_method_names=['GET'])
def paramsum(request: Request):
    params = request.query_params.dict()
    user_ip = request.META.get('REMOTE_ADDR')
    user_ip_obj = BlockIp.objects
    resp = user_limiter(user_ip, user_ip, limit_request_count, user_ip_obj)
    if isinstance(resp, Response):
        return resp
    counter_ = redis_cache.incr(user_ip)
    if counter_ == limit_request_count and not user_ip_obj.filter(ip=user_ip).exists():
        user_ip_obj.create(ip=user_ip)
    response_data = {
            'result': int(params['a']) + int(params['b'])
    }
    DataModel.objects.create(**request.query_params.dict())
    return Response(data=response_data, status= status.HTTP_200_OK)


class Total(generics.ListAPIView):
    permission_classes = [JustAdminPermission,]
    def get(self, request: Request):
        info = DataModel.objects.aggregate(total = Sum('a') + Sum('b'))
        return Response(data=info, status=status.HTTP_200_OK)


class History(generics.ListAPIView):
    permission_classes = [JustAdminPermission,]
    serializer_class = DataModelSerializer
    queryset = DataModel.objects.all()