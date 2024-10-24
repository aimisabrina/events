from django.urls import path
from . import views

urlpatterns = [
    path("",views.index, name="index"),
    path("signup/",views.signup, name="signup"),
    path("signup/login/",views.login, name="login"),
    path("login/main/",views.main, name="main"),
    path("login/staffmain/",views.staffmain, name="staffmain"),
    path("login/staffmain/manageevent/",views.manageevent, name="manageevent"),
    path("login/staffmain/supdate/<str:eventid>/",views.supdate, name="supdate"),
    path("login/staffmain/supdate/save_supdate/<str:eventid>/",views.save_supdate, name="save_supdate"),
    path("login/staffmain/sdelete/<str:eventid>/",views.sdelete, name="sdelete"),
    path("login/main/event/",views.event, name="event"),
    path('join_event/<str:eventid>/',views.join_event, name="join_event"),
    path("search/",views.search_results, name="search_results"),
    path("logout/",views.logout, name="logout"),
    
]