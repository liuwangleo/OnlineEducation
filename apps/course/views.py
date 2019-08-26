import math

from django.db.models import Q
from django.http import HttpResponse
from pure_pagination import PageNotAnInteger, Paginator
from django.shortcuts import render

# Create your views here.
from django.views.generic.base import View

from course.models import Course, CourseResource, Video
from operation.models import CourseComments, UserCourse
from utils.mixin_utils import LoginRequiredMixin


class CourseListView(View):
    def get(self, request):
        all_courses = Course.objects.all().order_by('-add_time')
        hot_courses = Course.objects.all().order_by('-click_nums')[:2]
        last_page = math.ceil(int(all_courses.count()) / 3)
        search_keywords = request.GET.get('keywords', '')
        if search_keywords:
            all_courses = all_courses.filter(
                Q(name__icontains=search_keywords) | Q(desc__icontains=search_keywords) | Q(
                    detail__icontains=search_keywords))
        sort = request.GET.get('sort', "")
        if sort:
            if sort == "students":
                all_courses = all_courses.order_by("-students")
            elif sort == "hot":
                all_courses = all_courses.order_by("-click_nums")
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_courses, 3, request=request)
        all_courses = p.page(page)
        context = {
            'all_courses': all_courses,
            'hot_courses': hot_courses,
            'last_page': last_page,
            'sort': sort
        }
        return render(request, 'course-list.html', context=context)

    pass


class CourseDetailView(View):
    def get(self, request, course_id):
        course = Course.objects.get(id=int(course_id))
        course.click_nums += 1
        course.save()
        tag = course.tag
        if tag:
            related_courses = Course.objects.filter(tag=tag).exclude(id=course_id).order_by('-students')[:2]
        else:
            related_courses = []
        print(related_courses)
        context = {
            'course': course,
            'related_courses': related_courses,
        }
        return render(request, 'course-detail.html', context=context)
        pass


class CourseInfoView(LoginRequiredMixin, View):
    def get(self, request, course_id):
        # 根据id获取该课程信息
        course = Course.objects.get(id=course_id)
        user_courses = UserCourse.objects.filter(user=request.user, course=course)
        if not user_courses:
            user_course = UserCourse(user=request.user, course=course)
            user_course.save()
        # 根据当前课程获取所有的该课程的资源
        all_resources = CourseResource.objects.filter(course=course)
        # 根据当前课程获取该课程的用户信息
        user_courses = UserCourse.objects.filter(course=course)
        # 获取该课程中所有的用户id
        user_ids = [user_course.user_id for user_course in user_courses]
        print(user_ids)
        # 根据所有的用户id获取用户课程信息
        all_user_courses = UserCourse.objects.filter(user_id__in=user_ids)
        print(all_user_courses)
        # 取出所有课程id
        course_ids = [all_user_course.course_id for all_user_course in all_user_courses]
        print(course_ids)
        # 通过所有课程的id,找到所有的课程，按点击量去五个
        relate_courses = Course.objects.filter(id__in=course_ids).exclude(id=course_id).order_by("-click_nums")[:5]
        context = {
            'course': course,
            'all_resources': all_resources,
            'relate_courses': relate_courses
        }
        return render(request, 'course-video.html', context=context)
        pass


class CourseCommentView(View):
    def get(self, request, course_id):
        course = Course.objects.get(id=int(course_id))
        all_resources = CourseResource.objects.filter(course=course)
        all_comments = CourseComments.objects.all()
        context = {
            "course": course,
            "all_resources": all_resources,
            'all_comments': all_comments,
        }
        return render(request, 'course-comment.html', context=context)
        pass


class AddCommentView(View):
    def post(self, request):
        if not request.user.is_authenticated:
            # 未登录时返回json提示未登录，跳转到登录页面是在ajax中做的
            return HttpResponse('{"status":"fail", "msg":"用户未登录"}', content_type='application/json')
        course_id = request.POST.get("course_id", 0)
        comments = request.POST.get("comments", "")
        if int(course_id) > 0 and comments:
            # 实例化一个course_comments对象
            course_comments = CourseComments()
            # 获取评论的是哪门课程
            course = Course.objects.get(id=int(course_id))
            # 分别把评论的课程、评论的内容和评论的用户保存到数据库
            course_comments.course = course
            course_comments.comments = comments
            course_comments.user = request.user
            course_comments.save()
            return HttpResponse('{"status":"success", "msg":"评论成功"}', content_type='application/json')
        else:
            return HttpResponse('{"status":"fail", "msg":"评论失败"}', content_type='application/json')


class VideoPlayView(View):
    '''课程章节视频播放页面'''

    def get(self, request, video_id):
        video = Video.objects.get(id=int(video_id))
        # 通过外键找到章节再找到视频对应的课程
        course = video.lesson.course

        course.students += 1
        course.save()

        # 查询用户是否已经学习了该课程
        user_courses = UserCourse.objects.filter(user=request.user, course=course)
        if not user_courses:
            # 如果没有学习该门课程就关联起来
            user_course = UserCourse(user=request.user, course=course)
            user_course.save()

        # 相关课程推荐
        # 找到学习这门课的所有用户
        user_courses = UserCourse.objects.filter(course=course)
        # 找到学习这门课的所有用户的id
        user_ids = [user_course.user_id for user_course in user_courses]
        # 通过所有用户的id,找到所有用户学习过的所有过程
        all_user_courses = UserCourse.objects.filter(user_id__in=user_ids)
        # 取出所有课程id
        course_ids = [all_user_course.course_id for all_user_course in all_user_courses]
        # 通过所有课程的id,找到所有的课程，按点击量去五个
        relate_courses = Course.objects.filter(id__in=course_ids).order_by("-click_nums")[:5]

        # 资源
        all_resources = CourseResource.objects.filter(course=course)
        return render(request, 'course-play.html', {
            'course': course,
            'all_resources': all_resources,
            'relate_courses': relate_courses,
            'video': video,
        })

    pass
