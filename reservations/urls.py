from django.urls            import path

from reservations.views     import MainResevationsView, DetailReservationView

urlpatterns = [
    path('', MainResevationsView.as_view()),
    path('/<str:reservation_number>', DetailReservationView.as_view())
]