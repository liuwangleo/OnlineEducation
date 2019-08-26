from django.urls import path, include, re_path
from .views import CourseListView, CourseDetailView, CourseInfoView, CourseCommentView, AddCommentView, VideoPlayView

app_name = "course"
urlpatterns = [
    # 课程列表
    path('course_list/', CourseListView.as_view(), name="course_list"),
    # 课程详情
    re_path('course_detail/(?P<course_id>\d+)/', CourseDetailView.as_view(), name="course_detail"),
    # 课程章节信息
    re_path('course_info/(?P<course_id>\d+)/', CourseInfoView.as_view(), name="course_info"),
    # 课程评论
    re_path('course_comment/(?P<course_id>\d+)', CourseCommentView.as_view(), name="course_comment"),
    # 发布评论
    path('add_comment/',AddCommentView.as_view(),name="add_comment"),
    # 播放课程视频
   re_path('video_play/(?P<video_id>\d+)/',VideoPlayView.as_view(),name="video_play"),
]
