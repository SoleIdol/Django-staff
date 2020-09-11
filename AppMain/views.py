import os
from math import ceil
import random
import string

from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse

from App.models import User
from AppMain.models import Employee
from staff.settings import BASE_DIR


def main(request):
    """首页：所有员工信息展示页"""
    uid = request.session.get('uid', '')
    u_name = request.session.get('u_name', '')
    u_icon = request.session.get('u_icon', '')
    
    # if not uid:
    #     messages.warning(request, '你还没有登录，请先登录')
    #     return redirect(reverse('app:login'))
    # own = User.objects.get(pk=int(uid))
    
    page = int(request.GET.get('page', 1))
    
    per_page = 10
    offset = per_page * (page - 1)
    
    max_page = ceil(Employee.objects.count() / per_page)
    
    if max_page <= 7:
        start, end = 1, max_page
    elif page <= 3:
        start, end = 1, 7
    elif page > (max_page - 3):
        start, end = max_page - 6, max_page
    else:
        start, end = (page - 3), (page + 3)
    page_list = list(range(start, end + 1))
    
    e_list = Employee.objects.all()[offset: offset + per_page]
    
    context = {
        'e_list': e_list,
        'uid': uid,
        'u_name': u_name,
        'u_icon': u_icon,
        'page': page,
        'page_list': page_list,
        'start': start,
        'end': end,
        'max_page': max_page,
        
    }
    return render(request, 'main.html', context=context)


def addData(request):
    """添加一个新员工"""
    if request.method == 'POST':
        
        if not request.POST.get('e_age').isdigit():
            messages.warning(request, '年龄应为一个整数！！！')
            return redirect(reverse('appMain:addData'))
        e = Employee()
        e.e_name = request.POST.get('e_name', '')
        e.e_age = int(request.POST.get('e_age'))
        e.e_gender = bool(int(request.POST.get('e_gender')))
        e.e_tel = request.POST.get('e_tel', '')
        
        e.save()
        
        return redirect(reverse('appMain:main'))
    else:
        uid = request.session.get('uid', '')
        u_name = request.session.get('u_name', '')
        u_icon = request.session.get('u_icon', '')
        return render(request, 'addData.html', context=locals())


def deleteData(request):
    """删除员工信息"""
    e = Employee.objects.get(pk=int(request.GET.get('eid')))
    e.delete()
    return JsonResponse({'idDel': 'ok'})


def updateData(request):
    """更新员工信息"""
    uid = request.session.get('uid', '')
    u_name = request.session.get('u_name', '')
    u_icon = request.session.get('u_icon', '')
    
    # uid = request.session.get('uid', '')
    # if not uid:
    #     return render(request, 'err.html', context={'err_msg': '你还没有登录！！！'})
    # own = User.objects.get(pk=int(uid))
    
    if request.method == 'POST':
        e = Employee.objects.get(pk=int(request.POST.get('eid')))
        
        e.e_name = request.POST.get('e_name')
        if not request.POST.get('e_age').isdigit():
            messages.warning(request, '年龄应为一个整数！！！')
            
            context = {
                'emp': e,
                'uid': uid,
                'u_name': u_name,
                'u_icon': u_icon,
            }
            return render(request, 'updateData.html', context=context)
        
        e.e_age = int(request.POST.get('e_age', 22))
        
        e.e_gender = bool(int(request.POST.get('e_gender')))
        
        e.e_tel = request.POST.get('e_tel')
        
        e.save()
        
        return redirect(reverse('appMain:main'))
    
    else:
        eid = int(request.GET.get('eid'))
        emp = Employee.objects.get(pk=eid)
        context = {
            'emp': emp,
            'uid': uid,
            'u_name': u_name,
            'u_icon': u_icon,
        }
        return render(request, 'updateData.html', context=context)


def userInfo(request):
    """用户信息展示"""
    uid = request.session.get('uid', '')
    u_name = request.session.get('u_name', '')
    u_icon = request.session.get('u_icon', '')
    
    # own = User.objects.get(pk=int(request.session.get('uid')))
    
    emp = Employee.objects.get(pk=int(request.GET.get('eid')))
    context = {
        'emp': emp,
        'uid': uid,
        'u_name': u_name,
        'u_icon': u_icon,
    }
    return render(request, 'userInfo.html', context=context)


def uploadIcon(request):
    """头像上传"""
    uid = request.session.get('uid', '')
    u_name = request.session.get('u_name', '')
    u_icon = request.session.get('u_icon', '')
    
    # own = User.objects.get(pk=int(request.session.get('uid')))
    
    emp = Employee.objects.get(pk=int(request.POST.get('eid')))
    file = request.FILES.get('file')
    suffix = file.name.rsplit('.', 1)[1]
    emp.e_icon = f'icon{emp.id}.{suffix}'
    
    path = os.path.join(BASE_DIR, 'static', 'upload', emp.e_icon)
    f = open(path, 'wb')
    for chunk in file.chunks():
        f.write(chunk)
    f.close()
    
    emp.save()
    
    context = {
        'emp': emp,
        'uid': uid,
        'u_name': u_name,
        'u_icon': u_icon,
    }
    return render(request, 'userInfo.html', context=context)


def createEmpData(request, num):
    """创建num条员工信息"""
    strs = string.ascii_lowercase
    digs = string.digits
    for i in range(int(num)):
        e = Employee()
        e.e_name = ''.join(random.choices(strs, k=random.randint(3, 8))).title()
        e.e_age = random.choice(range(18, 36))
        e.e_gender = random.choice([True, False])
        e.e_tel = random.choice(['131', '133', '138', '155', '173', '188']) + ''.join(random.choices(digs, k=8))
        e.save()
    return HttpResponse(f'已创建{num}条员工信息')


def selectData(request):
    """查找符合条件的员工信息"""
    uid = request.session.get('uid', '')
    u_name = request.session.get('u_name', '')
    u_icon = request.session.get('u_icon', '')
    
    # uid = request.session.get('uid', '')
    # if not uid:
    #     return render(request, 'err.html', context={'err_msg': '你还没有登录！！！'})
    # own = User.objects.get(pk=int(uid))
    
    page = int(request.GET.get('page', 1))
    per_page = 10
    offset = per_page * (page - 1)
    
    # 查询功能的实现
    subId = request.GET.get('subId', '').strip()
    subName = request.GET.get('subName', '').strip()
    subGender = int(request.GET.get('subGender', 2))
    subAge = request.GET.get('subAge', '').strip()
    e_list = Employee.objects
    
    if subId:
        if not subId.isdigit():
            messages.warning(request, 'id应为一个整数!!!')
            return redirect(reverse('appMain:main'))
        e_list = e_list.filter(id=subId)
    
    if subName:
        e_list = e_list.filter(e_name__contains=subName)
    
    if subGender == 1:
        e_list = e_list.filter(e_gender=True)
    elif subGender == 0:
        e_list = e_list.filter(e_gender=False)
    
    if subAge:
        if not subAge.isdigit():
            messages.warning(request, '年龄应为一个整数!!!')
            return redirect(reverse('appMain:main'))
            # return render(request, 'err2.html', context={'err_msg': '年龄应为一个整数！！！'})
        e_list = e_list.filter(e_age=subAge)
    
    max_page = ceil(e_list.count() / per_page)
    e_list = e_list.all()[offset: offset + per_page]
    
    if max_page <= 7:
        start, end = 1, max_page
    elif page <= 3:
        start, end = 1, 7
    elif page > (max_page - 3):
        start, end = max_page - 6, max_page
    else:
        start, end = (page - 3), (page + 3)
    page_list = list(range(start, end + 1))
    
    context = {
        'e_list': e_list,
        'uid': uid,
        'u_name': u_name,
        'u_icon': u_icon,
        'page': page,
        'page_list': page_list,
        'start': start,
        'end': end,
        'max_page': max_page,
        'subId': subId,
        'subName': subName,
        'subGender': subGender,
        'subAge': subAge,
    }
    return render(request, 'selectData.html', context=context)
