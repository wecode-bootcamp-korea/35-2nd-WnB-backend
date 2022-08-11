from django.urls import path

from hosts.views import HostingRoomView

urlpatterns = [
    path('', HostingRoomView.as_view())
]