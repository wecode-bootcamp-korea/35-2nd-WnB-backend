from django.urls import path, include

from rooms.views import RoomView

urlpatterns = [
    path('users', include('users.urls')),
    path('/rooms', RoomView.as_view())
]
