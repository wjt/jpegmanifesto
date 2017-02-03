from django.conf.urls import url

from . import views

urlpatterns = [  # pylint: disable=C0103
    url(r'^$', views.index, name='index'),
    url(r'^image/(?P<public_id>[0-9a-f-]{32,})$', views.image, name='image'),
    url(r'^image/(?P<public_id>[0-9a-f-]{32,})/moar$',
        views.moar, name='moar'),
]
