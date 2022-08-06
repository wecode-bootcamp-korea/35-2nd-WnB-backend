from django.urls import path

from users.views import UserAdditionalInfoView

urlpatterns = [
    path('/additional-info', UserAdditionalInfoView.as_view())
]