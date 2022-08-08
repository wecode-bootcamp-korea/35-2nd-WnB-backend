from django.urls import path

from users.views import KakaoOauthView, UserAdditionalInfoView

urlpatterns = [
    path('/kakao/oauth', KakaoOauthView.as_view()),
    path('/additional-info', UserAdditionalInfoView.as_view())
]