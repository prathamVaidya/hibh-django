
from hibh_api import views
from django.urls import path

urlpatterns = [
    path('tracker/verify/<str:email_token>', views.verifyTracker),
    path('tracker/<str:private_key>', views.getTrackerStats),
    path("tracker", views.TrackerView.as_view(), name = "tracker"),
    path("alert/<str:public_key>", views.createAlert, name = "alert"),
    path("download/html/<str:private_key>", views.getTrackerHTMLFile, name = "download tracking as HTML File"),
]
