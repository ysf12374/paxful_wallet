from django.urls import path,re_path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.http import StreamingHttpResponse

urlpatterns = [
    path('create', views.create, name='create'),
    path('api', views.api, name='api'),
    path('details_long', views.details_long, name='details_long'),
    path('details_short', views.details_short, name='details_short'),
    path('create_session', views.create_session, name='create_session'),
    path('create_address', views.create_address, name='create_address'),
    path('transfer_funds/<int:amount>', views.transfer_funds, name='transfer'),
    path('generate', views.generate, name='generate'),
]

 