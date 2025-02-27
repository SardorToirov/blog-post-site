from django.urls import path
from .views import (
    login_page,
    register_page,
    PostList,
    post_detail,
    logout_page,
)

app_name = "home"

urlpatterns = [
    path('', PostList.as_view(), name='home'),
    path('login/', login_page, name='login'),
    path('logout/', logout_page, name='logout'),
    path('register/', register_page, name='register'),

    # Post tafsilotlari
    path('<int:year>/<int:month>/<int:day>/<slug:slug>/', post_detail, name='post_detail'),
]
