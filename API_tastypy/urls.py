from django.conf.urls import url, include
from django.urls import path
from .models import AutamaResource, AccountsResource
from tastypie.api import Api

v1_api = Api(api_name='v1')
v1_api.register(AutamaResource())
v1_api.register(AccountsResource())

urlpatterns = [
    # The normal jazz here...
    path('', include(v1_api.urls)),
    ]
