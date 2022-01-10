from django.urls import path

from itez.users.views import (
    user_detail_view,
    user_redirect_view,
    user_update_view,
    UserCreateView,
    user_profile,
    user_profile_photo_update,
)

app_name = "users"
urlpatterns = [
    path("create_user/", view=UserCreateView, name="create_user"),
    path("user/profile/photo/upload/", user_profile_photo_update, name="profile_photo"),
    path("user/profile/", user_profile, name="profile"),
    path("~redirect/", view=user_redirect_view, name="redirect"),
    path("~update/", view=user_update_view, name="update"),
    path("<str:username>/", view=user_detail_view, name="detail"),
]
