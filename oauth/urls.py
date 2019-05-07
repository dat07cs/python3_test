from django.conf.urls import url

from oauth import views

handler403 = 'integration.views.permission_denied_view'

urlpatterns = [
    url(r'^login/$', views.oauth_login_view, name='oauth_login_view'),
    url(r'^oath2callback/$', views.oauth_callback_view, name='oauth_callback_view'),
    url(r'^logout/$', views.logout_view, name='logout_view'),
]
