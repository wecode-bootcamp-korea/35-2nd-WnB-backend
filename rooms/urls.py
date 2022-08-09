from django.urls    import path 

from rooms.views import RoomsView

urlpatterns = [
    path ('', RoomsView.as_view())
]