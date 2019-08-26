from django.urls import path, re_path

from organization.views import OrgListView, UserAskView, OrgHomeView, OrgCoursesView, OrgDescView, OrgTeacherView, \
    TeacherDetailView, TeacherListView

app_name = 'organization'

urlpatterns = [
    path('org_list/', OrgListView.as_view(), name="org_list"),
    path('user_ask/', UserAskView.as_view(), name="user_ask"),
    # 机构首页
    re_path('org_home/(?P<org_id>\d+)/', OrgHomeView.as_view(), name="org_home"),
    # 机构课程
    re_path('org_course/(?P<org_id>\d+)/', OrgCoursesView.as_view(), name="org_course"),
    # 机构介绍
    re_path('org_desc/(?P<org_id>\d+)/', OrgDescView.as_view(), name='org_desc'),
    # 机构讲师
    re_path('org_teacher/(?P<org_id>\d+)/', OrgTeacherView.as_view(), name='org_teacher'),

    # 讲师列表
    path('teacher_list/',TeacherListView.as_view(),name="teacher_list"),
    # 讲师介绍
    re_path('teacher_detail/(?P<teacher_id>\d+)', TeacherDetailView.as_view(), name='teacher_detail'),
]
