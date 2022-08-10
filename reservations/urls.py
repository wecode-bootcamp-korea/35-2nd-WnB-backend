from django.urls            import path

from reservations.views     import MainResevationsView

urlpatterns = [
    path('', MainResevationsView.as_view())
]