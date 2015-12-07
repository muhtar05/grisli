from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$',views.LinkList.as_view(),name='index'),
    url(r'^(?P<pk>[0-9]+)/$', views.LinkDetail.as_view(), name='detail'),
]
