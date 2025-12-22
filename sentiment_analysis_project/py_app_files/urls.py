from django.contrib import admin
from django.urls import path
from sent_app import views

app_name="sent_app"

urlpatterns=[
    path('admin/',admin.site.urls),
    path("",views.index,name="index"),
    path("sentiment/",views.sentiment,name="sentiment"),
    path("404/",views.error_page,name="404"),
    path("buttons/",views.buttons,name="buttons"),
    path("cards/",views.cards,name="cards"),
    path("charts/",views.charts,name="charts"),
    path("forgot_password/",views.forgot_password,name="forgot_password"),
    path("register/",views.register,name="register"),
    path("login/",views.login,name="login"),
    path("tables/",views.tables,name="tables"),
    path("Save_data/",views.data_save,name="data_save"),
    path("utilities-animation/",views.utilities_animation,name="utilities-animation"),
    path("utilities-border/",views.utilities_border,name="utilities-border"),
    path("utilities-color/",views.utilities_color,name="utilities-color"),
    path("utilities-other/",views.utilities_other,name="utilities-other"),
    path("analyze_user_account/",views.get_user_account,name="analyze_user_account"),
    path("get_user_acc_comm/",views.get_user_account_comments,name="get_user_acc_comments"),
]