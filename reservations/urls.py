from django.urls            import path

from reservations.views     import ResevationsView

urlpatterns = [
    path('', ResevationsView.as_view())
]