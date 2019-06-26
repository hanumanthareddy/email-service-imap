from django.urls import path
from .views import QsMailService

urlpatterns = [
    # path('', QsDescribeInstances, name='describeInstances'),
    path('', QsMailService, name='qsmailservice')
]
