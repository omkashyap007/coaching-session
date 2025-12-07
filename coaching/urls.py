from django.urls import path
from coaching.views import homePage, createSessions, joinSession, completeSession

urlpatterns = [
    path("", homePage, name="home"),
    path("sessions/<int:expert_id>/", createSessions, name="create-session"),
    path("session-join/<int:session_id>/", joinSession, name="join-session"),
    path("complete-session/<int:session_id>/", completeSession, name="complete-session"),
]