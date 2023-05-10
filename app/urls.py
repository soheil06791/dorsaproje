from django.urls import path
from .views import paramsum, Total, History

urlpatterns = [
    path('sum/', paramsum),
    path('total/', Total.as_view(), name = 'total'),
    path('history/', History.as_view(), name = 'history')
]