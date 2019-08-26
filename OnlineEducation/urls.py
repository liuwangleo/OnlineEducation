"""OnlineEducation URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.views.static import serve
from django.urls import path, include, re_path

from OnlineEducation.settings import MEDIA_ROOT, STATIC_ROOT
from organization import urls
import xadmin

from django.views.generic import TemplateView

from users.views import LoginView, RegisterView, LogoutView, ActiveUserView, ForgetPwdView, ResetPwdView, ModifyPwdView, \
    IndexView

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('xadmin/', xadmin.site.urls),
    # path('', TemplateView.as_view(template_name='index.html'), name='index'),
    path('', IndexView.as_view(), name='index'),
    path('login/', LoginView.as_view(), name="login"),
    path('register/', RegisterView.as_view(), name="register"),
    # 激活账号
    re_path('active_user/(?P<active_code>.*)/', ActiveUserView.as_view(), name="active_user"),
    path('forget_pwd/', ForgetPwdView.as_view(), name="forget_pwd"),
    # 重置密码
    re_path('reset_pwd/(?P<active_code>.*)', ResetPwdView.as_view(), name='reset_pwd'),
    # 修改密码
    path('modify_pwd/', ModifyPwdView.as_view(), name="modify_pwd"),
    path('logout/', LogoutView.as_view(), name='logout'),

    # 机构
    path('org/', include(('organization.urls', 'organization'), namespace='org')),
    # 课程
    path('course/', include(('course.urls', 'course'), namespace='course')),
    # 处理图片的url 使用Django自带serve,传入参数告诉它去哪个路径找，我们有配置好的路径MEDIAROOT
    re_path(r'^media/(?P<path>.*)', serve, {"document_root": MEDIA_ROOT}),
    path('captcha/', include('captcha.urls')),
    re_path(r'^static/(?P<path>.*)', serve, {"document_root": STATIC_ROOT}),
]
