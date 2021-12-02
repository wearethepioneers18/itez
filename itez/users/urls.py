from django.urls import path

from itez.users.views import (
    user_detail_view,
    user_redirect_view,
    user_update_view,
    UserCreateView
)

app_name = "users"
urlpatterns = [
    path("create_user/", view=UserCreateView, name="create_user"),
    path("~redirect/", view=user_redirect_view, name="redirect"),
    path("~update/", view=user_update_view, name="update"),
    path("<str:username>/", view=user_detail_view, name="detail"),
]
