import io
import os
from hashlib import sha256

from PIL import Image, ImageDraw, ImageFont
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
import string
import random

# Create your views here.
from django.urls import reverse

from App.models import User
from staff.settings import BASE_DIR


def make_password(password):
    """
    产生一个安全的密码
    :return: 加密后的password
    """
    if not isinstance(password, bytes):
        password = str(password).encode('utf8')
    
    # 计算哈希值
    hash_value = sha256(password).hexdigest()
    
    # 产生一个随机盐
    salt = os.urandom(16).hex()
    
    # 加盐，产生安全密码
    safe_password = salt + hash_value
    # print(f'注册：\n\t原密码：{len(password)}  --  {password}\n\t计算后：{len(hash_value)}  --  {hash_value}\n\t'
    #       f'加盐后：{len(safe_password)}  --  {safe_password}')
    #
    return safe_password


def check_password(password, safe_password):
    """
    密码验证
    :param password:页面输入的密码
    :param safe_password:数据库中的密码
    :return: Boolean
    """
    if not isinstance(password, bytes):
        password = str(password).encode('utf8')
    
    # 计算哈希值
    hash_value = sha256(password).hexdigest()
    #
    # print(f'验证：\n\t输入密码：{len(password)}  --  {password}\n\t'
    #       f'计算的：{len(hash_value)}  --  {hash_value}\n\t'
    #       f'数据库：{len(safe_password[32:])}  --  {safe_password[32:]}\n\t')
    #
    return hash_value == safe_password[32:]


def login(request):
    """登录页面"""
    if request.method == 'POST':
        
        if request.POST.get('checkNum1').strip().lower() != request.session.get('code').lower():
            messages.warning(request, '验证码输入有误！！！')
            return redirect(reverse('app:login'))
        users = User.objects.filter(u_name=request.POST.get('u_name')).all()
        if not users:
            messages.warning(request, '用户不存在！！！')
            return redirect(reverse('app:login'))
        user = users[0]
        
        if not check_password(request.POST.get('u_password'), user.u_password):
            messages.warning(request, '密码错误！！！')
            return redirect(reverse('app:login'))
        
        request.session['uid'] = user.id
        request.session['u_name'] = user.u_name
        request.session['u_icon'] = user.u_icon
        
        return redirect(reverse('appMain:main'))
    
    else:
        str1 = string.ascii_letters + string.digits
        checkNum = ''.join(random.choices(str1, k=4))
        context = {
            'checkNum': checkNum,
        }
        
        return render(request, 'login.html', context=context)


def register(request):
    """注册页面"""
    if request.method == 'POST':
        u = User()
        if not int(request.POST.get('flag')):
            messages.warning(request, '信息输入不符合规范！')
            return redirect(reverse('app:register'))
        u.u_password = make_password(request.POST.get('u_password1'))
        u.u_name = request.POST.get('u_name', '')
        if not request.POST.get('u_age').isdigit():
            messages.warning(request, '年龄应为一个整数')
            return redirect(reverse('app:register'))
        u.u_age = int(request.POST.get('u_age'))
        u.u_gender = bool(int(request.POST.get('u_gender')))
        u.u_tel = request.POST.get('u_tel')
        u.save()
        
        return redirect(reverse('app:login'))
    else:
        return render(request, 'register.html')


def logout(request):
    """退出系统"""
    request.session.flush()
    # response.delete_cookie('uid')
    # response.delete_cookie('u_name')
    return redirect(reverse('app:login'))


def userExists(request):
    # print('验证了用户名是否存在')
    if User.objects.filter(u_name=request.POST.get('u_name')).exists():
        flag = True  # 已存在，不可用
    else:
        flag = False
    return JsonResponse({'exists': flag})


def checkAge(request):
    # print('验证了年龄')
    flag = False
    age = request.POST.get('num')
    if age.isdigit():
        if 0 <= int(age) <= 150:
            # print(age)
            flag = True
    
    return JsonResponse({'is_pass': flag})


def checkTel(request):
    # print('验证了电话')
    flag = False
    tel = request.POST.get('num')
    tel_list = ['134', '135', '136', '137', '138', '139', '147', '150', '151',
                '152', '157', '158', '159', '182', '187', '188', '130', '131',
                '132', '155', '156', '185', '186', '133', '153', '180', '189']
    
    if tel.isdigit():
        if len(tel):
            if tel[0:3] in tel_list:
                flag = True
    
    return JsonResponse({'is_pass': flag})


# 获取随机颜色
def get_random_color():
    R = random.randrange(200)
    G = random.randrange(200)
    B = random.randrange(200)
    return (R, G, B)


def create_lines(draw):
    """绘制干扰线"""
    line_num = random.randint(1, 2)  # 干扰线条数
    
    for i in range(line_num):
        # 起始点
        begin = (random.randint(0, 30), random.randint(10, 40))
        # 结束点
        end = (random.randint(100, 130), random.randint(10, 40))
        draw.line([begin, end], width=3, fill=get_random_color())


def create_points(draw):
    """绘制干扰点"""
    chance = 80
    
    for w in range(130):
        for h in range(70):
            tmp = random.randint(0, 90)
            if tmp > chance:
                draw.point((w, h), fill=get_random_color())


def get_verify_img(request):
    # 定义画布背景颜色
    bg_color = (255, 255, 255)
    # 画布大小
    img_size = (130, 50)
    # 定义画布
    image = Image.new("RGB", img_size, bg_color)
    # 定义画笔
    draw = ImageDraw.Draw(image, "RGB")
    # 创建字体（字体的路径，服务器路径）
    font_path = os.path.join(BASE_DIR, 'static', 'fonts', 'ALGER.TTF')
    # 实例化字体，设置大小是30
    font = ImageFont.truetype(font_path, 30)
    # 准备画布上的字符集
    source = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    # 保存每次随机出来的字符
    code_str = ""
    for i in range(4):
        # 获取数字随机颜色
        text_color = get_random_color()
        # 获取随机数字 len
        tmp_num = random.randrange(len(source))
        # 获取随机字符 画布上的字符集
        random_str = source[tmp_num]
        # 将每次随机的字符保存（遍历） 随机四次
        code_str += random_str
        # 将字符画到画布上
        draw.text((10 + 30 * i, 10), random_str, text_color, font)
    
    # 绘制干扰线
    create_lines(draw)
    # 绘制干扰点
    create_points(draw)
    
    # 记录给哪个请求发了什么验证码
    request.session['code'] = code_str
    
    # 使用画笔将文字画到画布上
    # draw.text((10, 20), "X", text_color, font)
    # draw.text((40, 20), "Q", text_color, font)
    # draw.text((60, 20), "W", text_color, font)
    
    # 获得一个缓存区
    buf = io.BytesIO()
    # 将图片保存到缓存区
    image.save(buf, 'png')
    # 将缓存区的内容返回给前端 .getvalue 是把缓存区的所有数据读取
    return HttpResponse(buf.getvalue(), 'image/png')
