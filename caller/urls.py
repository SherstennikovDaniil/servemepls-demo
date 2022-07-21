from django.urls import path

from .views import *

urlpatterns = [
    path('caller/<str:data>', CallView.as_view(), name='call-view'),
    path('send-notification/', SendNotification.as_view(), name='notif-view')
]
