from django.contrib import admin
from django.urls import path
from home.views import home_page, add_student, edit_student, delete_student, user_login, user_logout, user_signup

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_page),
    path('add/', add_student),
    path('edit/<int:id>/', edit_student),
    path('delete/<int:id>/', delete_student),
    path('login/', user_login),
    path('logout/', user_logout),
    path('signup/', user_signup),
]
