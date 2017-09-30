from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^get_job_status/$', views.get_job_status, name='get_job_status'),

    # Main pages
    url(r'^confirmation/(?P<pk>[\w-]*)/$', views.ConfirmationView.as_view(), name="confirmation"),
    url(r'^destruction/(?P<pk>[\w-]*)/$', views.DestructionView.as_view(), name="destruction"),
]
