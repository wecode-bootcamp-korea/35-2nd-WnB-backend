from django.urls    import path 

from rooms.views import RoomsView, RoomDetailView

urlpatterns = [
    path ('', RoomsView.as_view()),
    path('/<int:room_id>', RoomDetailView.as_view())
]