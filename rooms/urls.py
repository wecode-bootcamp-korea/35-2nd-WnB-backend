from django.urls    import path 

from rooms.views import RoomDetailView, ReservationFilterView

urlpatterns = [
    path('/<int:room_id>', RoomDetailView.as_view()),
    path ('', ReservationFilterView.as_view())
]
#as_view = ''주소로 들어오면 내가 쓴 view로 들어간다고 한다.