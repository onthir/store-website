from django.conf.urls import url
from . import views

app_name = 'shop'
urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^add-products/$', views.add_products, name='add_products'),
    url(r'^generate-bill/$', views.generate_bill, name='generate_bill'),
    url(r'^remove-product/(?P<id>\d+)/(?P<pid>\d+)/$', views.delete_item, name='delete_item'),
    url(r'^update-stocks/(?P<slug>.*)/$', views.update_stocks, name='update_stocks'),
    url(r'^start-update/$', views.showupdate, name='showupdate'),
    url(r'^change-name/(?P<slug>.*)/(?P<id>\d+)/$', views.change_name, name='change_name'),
    url(r'^change-price/(?P<slug>.*)/(?P<id>\d+)/$', views.change_price, name='change_price'),
    url(r'^login-user/$', views.login_user, name='login_user'),
    url(r'^statistics/$', views.stats, name='stats')
]
