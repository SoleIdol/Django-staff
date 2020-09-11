from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.deprecation import MiddlewareMixin


class LoginCheck(MiddlewareMixin):
    def process_request(self, request):
        path_list = [
            '/appMain/main/',
            '/appMain/addData/',
            '/appMain/deleteData/',
            '/appMain/updateData/',
            '/appMain/selectData/',
            '/appMain/userInfo/',
            '/appMain/uploadIcon/',
        
        ]
        
        if request.path in path_list:
            if not request.session.get('uid'):
                messages.warning(request, '你还没有登录，请登录')
                return redirect(reverse('app:login'))
