# Create your views here.
import math

from django.http import HttpResponse
from django.views.generic import View
from django.shortcuts import render
from pure_pagination import Paginator, PageNotAnInteger

from course.models import Course
from operation.models import UserAsk
from organization.forms import UserAskForm
from organization.models import CourseOrg, CityDict, Teacher


class OrgListView(View):
    def get(self, request):
        # 所有课程机构
        all_orgs = CourseOrg.objects.all()
        # 按照点击率排名
        hot_orgs = all_orgs.order_by('-click_nums')[:3]
        # 所有的城市
        all_citys = CityDict.objects.all()

        city_id = request.GET.get('city', '')
        print(city_id)
        if city_id:
            all_orgs = all_orgs.filter(city_id=city_id)
        print(all_orgs)
        category = request.GET.get('ct', '')
        if category:
            all_orgs = all_orgs.filter(category=category)

        sort = request.GET.get('sort', '')
        if sort:
            if sort == 'students':
                all_orgs = all_orgs.order_by('-students')
            elif sort == 'courses':
                all_orgs = all_orgs.order_by('-course_nums')
        print(all_orgs)
        # 机构的数量
        org_nums = all_orgs.count()
        # 对课程机构进行分页
        # 尝试获取前台get请求传递过来的page参数
        # 如果是不合法的配置参数默认返回第一页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_orgs, 2, request=request)
        all_orgs = p.page(page)
        context = {
            'all_orgs': all_orgs,
            'all_citys': all_citys,
            'org_nums': org_nums,
            'last_page': math.ceil(int(org_nums) / 2),
            'city_id': city_id,
            'category': category,
            'hot_orgs': hot_orgs,
            'sort': sort
        }
        return render(request, 'org-list.html', context=context)

    def post(self, request):
        pass


class UserAskView(View):
    def post(self, request):
        useraskform = UserAskForm(request.POST)
        if useraskform.is_valid():
            name = request.POST.get('name')
            mobile = request.POST.get('mobile')
            course_name = request.POST.get('course_name')
            userAsk = UserAsk()
            userAsk.name = name
            userAsk.mobile = mobile
            userAsk.course_name = course_name
            userAsk.save()
            # user_ask = useraskform.save(commit=True)
            # 如果保存成功,返回json字符串,后面content type是告诉浏览器返回的数据类型
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            # 如果保存失败，返回json字符串,并将form的报错信息通过msg传递到前端
            return HttpResponse('{"status":"fail", "msg":"添加出错"}', content_type='application/json')
        pass


class OrgHomeView(View):
    def get(self, request, org_id):
        course_org = CourseOrg.objects.get(id=int(org_id))
        all_courses = course_org.course_set.all()[:4]
        all_teachers = course_org.teacher_set.all()[:2]
        context = {
            'course_org': course_org,
            'all_courses': all_courses,
            'all_teachers': all_teachers
        }
        return render(request, 'org-detail-homepage.html', context=context)

    pass


class OrgCoursesView(View):
    def get(self, request, org_id):
        course_org = CourseOrg.objects.get(id=org_id)
        all_courses = course_org.course_set.all()
        context = {
            'course_org': course_org,
            'all_courses': all_courses,
        }
        return render(request, 'org-detail-course.html', context=context)
        pass


class OrgDescView(View):
    def get(self, request, org_id):
        course_org = CourseOrg.objects.get(id=org_id)
        all_courses = course_org.course_set.all()
        context = {
            'course_org': course_org,
            'all_courses': all_courses,
        }
        return render(request, 'org-detail-desc.html', context=context)

    pass


class OrgTeacherView(View):
    def get(self, request, org_id):
        course_org = CourseOrg.objects.get(id=org_id)
        all_teachers = course_org.teacher_set.all()
        context = {
            'course_org': course_org,
            'all_teachers': all_teachers,
        }
        return render(request, 'org-detail-teachers.html', context=context)


class TeacherListView(View):
    def get(self, request):
        all_teachers = Teacher.objects.all()
        # 总共有多少老师使用count进行统计
        teacher_nums = all_teachers.count()
        # 人气排序
        sort = request.GET.get('sort', '')
        if sort:
            if sort == 'hot':
                all_teachers = all_teachers.order_by('-click_nums')

        # 讲师排行榜
        sorted_teacher = Teacher.objects.all().order_by('-click_nums')[:3]
        # 进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_teachers, 1, request=request)
        teachers = p.page(page)
        context = {
            "all_teachers": teachers,
            "teacher_nums": teacher_nums,
            'sorted_teacher': sorted_teacher,
            'sort': sort
        }
        return render(request, "teachers-list.html", context=context)

    pass


class TeacherDetailView(View):
    def get(self, request, teacher_id):
        teacher = Teacher.objects.get(id=int(teacher_id))
        all_course = Course.objects.filter(teacher=teacher)

        # 讲师排行榜
        sorted_teacher = Teacher.objects.all().order_by('-click_nums')[:3]
        return render(request, 'teacher-detail.html', {
            'teacher': teacher,
            'all_course': all_course,
            'sorted_teacher': sorted_teacher,
        })
    pass
