from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.hashers import make_password
from django.shortcuts import render, redirect

# Create your views here.

from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from django.views.generic.base import View

from course.models import Course
from users.forms import LoginForm, RegisterForm, ForgetPwdForm, ModifyPwdForm
from users.models import UserProfile, EmailVerifyRecord, Banner
from utils.email_send import send_register_email


class CustomBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            # 用户名不能重复
            user = UserProfile.objects.get(Q(username=username) | Q(email=username))
            # 由于后台的密码加密，使用UserProfile继承的AbstractUser中有def check_password(self, raw_password):
            if user.check_password(password):
                return user
        except Exception as e:
            return None


class IndexView(View):
    '''首页'''

    def get(self, request):
        # 轮播图
        all_banners = Banner.objects.all().order_by('index')
        # 课程
        courses = Course.objects.filter(is_banner=False)[:6]
        # 轮播课程
        banner_courses = Course.objects.filter(is_banner=True)[:3]
        # 课程机构
        course_orgs = Course.objects.all()[:15]
        return render(request, 'index.html', {
            'all_banners': all_banners,
            'courses': courses,
            'banner_courses': banner_courses,
            'course_orgs': course_orgs,
        })

    pass


class LoginView(View):
    def get(self, request):
        return render(request, 'login.html')
        pass

    def post(self, request):
        # username = request.POST.get('username')
        # password = request.POST.get('password')
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = CustomBackend.authenticate(self, request, username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return render(request, 'index.html')
                else:
                    return render(request, 'login.html', {'msg': '您的账号未激活！', 'login_form': login_form})
            else:
                return render(request, 'login.html', {'msg': '用户名或者密码错误！', 'login_form': login_form})
        else:
            return render(request, 'login.html', {'msg': '用户名或者密码错误！', 'login_form': login_form})


class RegisterView(View):
    def get(self, request):
        register_form = RegisterForm()
        return render(request, 'register.html', {'register_form': register_form})

    def post(self, request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            username = request.POST.get('email', None)
            if UserProfile.objects.filter(email=username):
                return render(request, 'register.html', {'register_form': register_form, 'msg': '用户已经存在'})
            password = request.POST.get('password', None)
            userProfile = UserProfile()
            userProfile.username = username
            userProfile.password = make_password(password)
            userProfile.email = username
            userProfile.is_active = False
            userProfile.save()
            send_register_email(username, 'register')
            return render(request, 'login.html')
        else:
            return render(request, 'register.html', {"register_form": register_form})


class ActiveUserView(View):
    def get(self, request, active_code):
        print(active_code)
        all_record = EmailVerifyRecord.objects.filter(code=active_code)
        if all_record:
            for record in all_record:
                email = record.email
                user = UserProfile.objects.get(email=email)
                user.is_active = True
                user.save()
                return render(request, 'login.html')
        else:
            return render(request, 'active_fail.html')
        return render(request, 'register.html', {'msg': "您的激活链接失效"})


class ForgetPwdView(View):
    def get(self, request):
        forget_form = ForgetPwdForm(request.GET)
        return render(request, 'forgetpwd.html', {'forget_form': forget_form})

    def post(self, request):
        forget_form = ForgetPwdForm(request.POST)
        if forget_form.is_valid():
            email = request.POST.get('email')
            send_register_email(email, 'forget')
            return render(request, 'send_success.html')
        else:
            render(request, 'forgetpwd.html', {'forget_form': forget_form})


class ResetPwdView(View):
    def get(self, request, active_code):
        all_records = EmailVerifyRecord.objects.filter(code=active_code)
        if all_records:
            for record in all_records:
                email = record.email
                return render(request, "password_reset.html", {"email": email})
        else:
            return render(request, "active_fail.html")
        return render(request, "login.html")

    pass


class ModifyPwdView(View):
    def post(self, request):
        modify_form = ModifyPwdForm(request.POST)
        if modify_form.is_valid():
            pwd1 = request.POST.get('password1')
            pwd2 = request.POST.get('password2')
            email = request.POST.get('email')
            if pwd1 != pwd2:
                return render(request, 'password_reset.html', {'modify_form': modify_form, 'msg': '两次密码不一致'})
            user = UserProfile.objects.get(email=email)
            user.password = make_password(pwd1)
            user.save()
            return render(request, 'login.html')
        else:
            email = request.POST.get("email", "")
            return render(request, "password_reset.html", {"email": email, "modify_form": modify_form})

    pass


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('index')


from django.shortcuts import render_to_response


def pag_not_found(request):
    # 全局404处理函数
    response = render_to_response('404.html', {})
    response.status_code = 404
    return response


def page_error(request):
    # 全局500处理函数
    from django.shortcuts import render_to_response
    response = render_to_response('500.html', {})
    response.status_code = 500
    return response
