from django.conf.urls import url
from django.views.generic import TemplateView

from . import views

urlpatterns = [
    # Authentication and authorization
    url(r'^authorize/$', views.AuthorizeRedirectView.as_view(), name='authorize'),
    url(r'^oauth_callback/$', views.OAuthCallbackRedirectView.as_view(), name='oauth_callback'),
]
