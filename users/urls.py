from django.urls import path

from users.views import KakaoSignUpView, ExtraUserInfoView

urlpatterns = [
    path('/signup', KakaoSignUpView.as_view()),
    path('/info', ExtraUserInfoView.as_view())
]