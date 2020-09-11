from django.conf.urls import url

from AppMain import views

urlpatterns = [
    url(r'^main/', views.main, name='main'),
    url(r'^addData/', views.addData, name='addData'),
    url(r'^deleteData/', views.deleteData, name='deleteData'),
    url(r'^updateData/', views.updateData, name='updateData'),
    url(r'^selectData/', views.selectData, name='selectData'),
    url(r'^userInfo/', views.userInfo, name='userInfo'),
    url(r'^uploadIcon/', views.uploadIcon, name='uploadIcon'),
    url(r'^createEmpData/(\d+)/', views.createEmpData, name='createEmpData')
]
