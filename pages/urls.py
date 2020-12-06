from django.urls import path,re_path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.http import StreamingHttpResponse

urlpatterns = [
    path('api/v1/wallet/create', views.create, name='create'),
    path('api/v1/wallet/api', views.api, name='api'),
    path('api/v1/wallet/details_long', views.details_long, name='details_long'),
    path('api/v1/wallet/details_short', views.details_short, name='details_short'),
    path('api/v1/wallet/create_session', views.create_session, name='create_session'),
    path('api/v1/wallet/create_address', views.create_address, name='create_address'),
    path('api/v1/wallet/transfer_funds/<int:amount>', views.transfer_funds, name='transfer'),
    path('api/v1/wallet/generate', views.generate, name='generate'),
]

 
