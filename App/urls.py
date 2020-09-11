from django.conf.urls import url

from App import views

urlpatterns = [
    url(r'^login/', views.login, name='login'),
    url(r'^register/', views.register, name='register'),
    url(r'^logout/', views.logout, name='logout'),
    url(r'^userExists/', views.userExists, name='userExists'),
    url(r'^checkAge/', views.checkAge, name='checkAge'),
    url(r'^checkTel/', views.checkTel, name='checkTel'),
    url(r'^get_verify_img/', views.get_verify_img, name='get_verify_img'),

]
