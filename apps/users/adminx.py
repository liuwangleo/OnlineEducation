import xadmin
from .models import EmailVerifyRecord, Banner
from xadmin import views


class BaseSetting(object):
    # 开启主题
    enable_themes = True
    use_bootswatch = True


# 将基本配置管理与view绑定
xadmin.site.register(views.BaseAdminView, BaseSetting)


# 全局修改，固定写法
class GlobalSettings(object):
    # 修改title
    site_title = '后台管理界面'
    # 修改footer
    site_footer = 'OnlineEducation'
    # 收起菜单
    menu_style = 'accordion'

    def get_site_menu(self):
        return [
            {
                'title': '数据统计',
                'icon': 'fa fa-bar-chart-o',
                'menus': (
                    {
                        'title': '数据统计',
                        # 'url': 'baidu.com',
                        'icon': 'fa fa-cny',
                    },
                )
            },
        ]


# 将title和footer信息进行注册
xadmin.site.register(views.CommAdminView, GlobalSettings)


class EmailVerifyRecordAdmin(object):
    # 显示的列
    list_display = ['code', 'email', 'send_type', 'send_time']
    # 搜索的字段，不要添加时间搜索
    search_fields = ['code', 'email', 'send_type']
    # 过滤
    list_filter = ['code', 'email', 'send_type', 'send_time']


xadmin.site.register(EmailVerifyRecord, EmailVerifyRecordAdmin)


class BannerAdmin(object):
    list_display = ['title', 'image', 'url', 'index', 'add_time']
    search_fields = ['title', 'image', 'url', 'index']
    list_filter = ['title', 'image', 'url', 'index', 'add_time']


xadmin.site.register(Banner, BannerAdmin)
