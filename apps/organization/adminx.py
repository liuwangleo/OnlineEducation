import xadmin

from .models import CityDict, CourseOrg, Teacher


class CityDictAdmin(object):
    '''城市'''

    list_display = ['name', 'desc', 'add_time']
    search_fields = ['name', 'desc']
    list_filter = ['name', 'desc', 'add_time']


class CourseOrgAdmin(object):
    '''机构'''
    data_chats = {
        "order_amount": {'title': '订单金额', "x-field": "add_time", "y-field": ('name',),
                         "order": ('add_time',)},
        "order_count": {'title': '订单量', "x-field": "add_time", "y-field": ('name',),
                        "order": ('add_time',)},
    }
    list_display = ['name', 'desc', 'click_nums', 'fav_nums', 'students', 'course_nums', 'add_time']
    search_fields = ['name', 'desc', 'click_nums', 'fav_nums']
    list_filter = ['name', 'desc', 'click_nums', 'fav_nums', 'city__name', 'address', 'add_time']
    list_per_page = 5

    def get_city_name(self):
        pass


class TeacherAdmin(object):
    '''老师'''

    list_display = ['name', 'org', 'work_years', 'work_company', 'add_time']
    search_fields = ['org', 'name', 'work_years', 'work_company']
    list_filter = ['org__name', 'name', 'work_years', 'work_company', 'click_nums', 'fav_nums', 'add_time']


xadmin.site.register(CityDict, CityDictAdmin)
xadmin.site.register(CourseOrg, CourseOrgAdmin)
xadmin.site.register(Teacher, TeacherAdmin)
