from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^get_job_status/$', views.get_job_status, name='get_job_please'),

    # Main page
    url(r'^destruction/(?P<identifier>[\w-]*)/$', views.DestructionView.as_view(), name="destruction"),
]
