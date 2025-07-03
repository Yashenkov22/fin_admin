from django.contrib import admin, messages
from django.contrib.auth.models import User, Group
from django.db.models import Count, Sum, Value, OuterRef, Subquery, F
from django.db.models.functions import Coalesce
from django.db import transaction
from django.urls import path
from django.template.response import TemplateResponse
from django.utils.safestring import mark_safe
from django.utils import timezone

from django.conf import settings

from django_summernote.admin import SummernoteModelAdmin
from django_summernote.models import Attachment

from datetime import datetime, timedelta

from .models import Users, UTM, Orders, MassSendMessage, MassSendFile
from .views import custom_admin_view

from rangefilter.filters import (
    DateRangeFilterBuilder,
    DateTimeRangeFilterBuilder,
    NumericRangeFilterBuilder,
    DateRangeQuickSelectListFilterBuilder,
)


def generate_image_icon(icon_url: str):
    return settings.PROTOCOL + settings.SITE_DOMAIN\
                                + icon_url.url


class MassSendFileStacked(admin.StackedInline):
    model = MassSendFile
    extra = 0
    classes = [
        'collapse',
        ]
    readonly_fields = ('image_icon', 'file_id')
    
    def image_icon(self, obj):
        path_url_postfix = obj.file.url.split('.')[-1]

        if path_url_postfix in settings.IMAGE_POSTFIX_SET:
        
            icon_url = generate_image_icon(obj.file)
            # print('image url', icon_url)
            # icon_url = f'http://localhost:8000/django{obj.image.url}'
            ##
            return mark_safe(f"<img src='{icon_url}' width=40")
        else:
            return 'не опрелелено'
    
    image_icon.short_description = 'Изображение'


@admin.register(MassSendMessage)
class MassSendMessageAdmin(SummernoteModelAdmin):
    list_display = ('name', 'has_delayed_task', 'get_delayed_time')
    summernote_fields = ('content', '')
    inlines = [
        MassSendFileStacked,
    ]

    readonly_fields = (
        'has_delayed_task',
        'get_delayed_time',
    )

    def get_delayed_time(self, obj):
        if obj.delay_time is not None and  obj.has_delayed_task == 'Запланировано':
            return obj.delay_time.astimezone(tz=timezone).strftime("%d.%m.%y %H:%M")
        
    get_delayed_time.short_description = 'Запланировано на:'


    fieldsets = [
        (
            None,
            {
                "fields": ["name",
                           "content",
                           "has_delayed_task"]
                        #    "partner_link",
                        #    "is_active",
                        #    "is_vip",
                        #    'high_aml',
                        #    "get_total_direction_count",
                        #    "reserve_amount",
                        #    "age",
                        #    'time_create',
                        #    "country",
                        #    ("period_for_create", "period_for_update", "period_for_parse_black_list"),
                        #    'icon_url',
                        #    'get_icon',
                        #    'link_count'],
            },
        ),
        (
            "Функционал отложенного поста (по времени)",
            {
                "classes": ["collapse"],
                "fields": ["delay_time", "send_to"],
            },
        ),
    ]

    class Media:
        js = ('main/js/test_1.js', )



# class MyAdminSite(admin.AdminSite):

#     def dashboard_page(self, request):
#         return custom_admin_view(request, self=self)

#     def get_urls(self):
#         urls = super().get_urls()
#         # print(urls)
#         custom_urls = [
#             path('dashboard/', admin.site.admin_view(self.dashboard_page), name='dashboard_page'),
#         ]
#         return custom_urls + urls

#     def get_app_list(self, request, app_label=None):
#         app_list = super().get_app_list(request, app_label)
#         if app_label is None or app_label == 'custom':
#             app_list.append(
#                 {
#                     "name": "Общее",
#                     "app_label": "custom",
#                     "models": [
#                         {
#                             "name": "Статистика бота",
#                             "object_name": "dashboard",
#                             "admin_url": "/admin/dashboard",
#                             "view_only": True,
#                         }
#                     ],
#                 }
#             )
#         return app_list
    
    

# admin.site = MyAdminSite()

# admin.site.unregister(User)
# admin.site.unregister(Group)


class CustomDateTimeFilter(admin.SimpleListFilter):
    title = 'Фильтры по дате'
    parameter_name = 'custom_date_filter'

    def lookups(self, request, model_admin):
        return (
            ('today', 'Сегодня'),
            ('yesterday', 'Вчера'),
            ('this_week', 'В течении 7 дней'),
            ('this_month', 'В этом месяце'),
            ('this_year', 'В этом году'),
            ('date_exists', 'Дата указана'),
            ('date_not_exists', 'Дата не указана'),
        )

    def queryset(self, request, queryset):
        today = datetime.now()
        # print(today)
        if self.value() == 'today':
            start_of_today = today.replace(hour=0, minute=0, second=0, microsecond=0)
            end_of_today = today.replace(hour=23, minute=59, second=59, microsecond=999999)
            return queryset.filter(time_create__range=(start_of_today, end_of_today))
        elif self.value() == 'yesterday':
            start_of_yesterday = today.replace(hour=0, minute=0, second=0, microsecond=0) - timedelta(days=1)
            end_of_yesterday = today.replace(hour=0, minute=0, second=0, microsecond=0) - timedelta(seconds=1)
            return queryset.filter(time_create__range=(start_of_yesterday, end_of_yesterday))
        elif self.value() == 'this_week':
            # start_of_week = today - timedelta(days=today.weekday())
            start_of_week = today - timedelta(days=6, hours=23, minutes=59, seconds=59)

            # end_of_week = start_of_week + timedelta(days=6, hours=23, minutes=59, seconds=59)
            end_of_week = today

            return queryset.filter(time_create__range=(start_of_week, end_of_week))
        elif self.value() == 'this_month':
            start_of_month = today.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
            end_of_month = (start_of_month + timedelta(days=32)).replace(day=1) - timedelta(seconds=1)
            return queryset.filter(time_create__range=(start_of_month, end_of_month))
        elif self.value() == 'this_year':
            start_of_year = today.replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0)
            end_of_year = today.replace(month=12, day=31, hour=23, minute=59, second=59, microsecond=999999)
            return queryset.filter(time_create__range=(start_of_year, end_of_year))
        elif self.value() == 'date_exists':
            return queryset.exclude(time_create__isnull=True)
        elif self.value() == 'date_not_exists':
            return queryset.filter(time_create__isnull=True)
        
        return queryset
    

# class UTMSourceFilter(admin.filters.SimpleListFilter):
#     title = 'Кастомный UTM фильтр'
#     parameter_name = 'utm_source_start'

#     def lookups(self, request, model_admin):
#         request_session = request.session

#         # Получаем уникальные значения начала строки
#         # utm_source_start = request.GET.get('utm_source_start')
#         print('lookup',request.GET)
#         print('request session', request_session.__dict__)

#         if request_session.get('prefix_utm') and \
#             request_session.get('second_part_utm'):
#             print('22')

#         utm_source = self.value()
#         print(utm_source)
#         if not utm_source:
#             prefixes = Users.objects.filter(utm_source__isnull=False)\
#                                     .values_list('utm_source', flat=True)\
#                                     .distinct()

#             unique_prefix =  [('_'.join(prefix.split('_')[:2]), '_'.join(prefix.split('_')[:2])) \
#                                 for prefix in set(prefixes) if prefix is not None]
            
#             request_session['prefix_utm'] = None
#             request_session['second_part_utm'] = None

#             return sorted(set(unique_prefix))


#             # return [('_'.join(prefix.split('_')[:2]), '_'.join(prefix.split('_')[:2])) \
#             #         for prefix in set(prefixes) if prefix is not None]
#         else:
#             if utm_source[:2].isdigit():
#                 prefix_utm = request_session.get('prefix_utm')
#                 prefixes = Users.objects.filter(utm_source__isnull=False,
#                                                 utm_source__endswith=utm_source,
#                                                 utm_source__startswith=prefix_utm)\
#                                         .values_list('utm_source', flat=True)\
#                                         .distinct()
                
#                 request.session['second_part_utm'] = utm_source

#             check_value = (utm_source[:2].isdigit()) or (utm_source == '--')
            
#             if not check_value:
#                 prefixes = Users.objects.filter(utm_source__isnull=False,
#                                                 utm_source__startswith=utm_source)\
#                                         .values_list('utm_source', flat=True)\
#                                         .distinct()
                
#                 unique_prefix = [('_'.join(prefix.split('_')[2:]), '_'.join(prefix.split('_')[2:])) \
#                                  for prefix in set(prefixes) if prefix is not None]
                
#                 request.session['prefix_utm'] = utm_source
                
#                 return sorted(set(unique_prefix))

#                 # return [('_'.join(prefix.split('_')[2:]), '_'.join(prefix.split('_')[2:])) \
#                 #         for prefix in set(prefixes) if prefix is not None]
#             else:
#                 # request.session['prefix_utm'] = None
#                 return [('--', '--')]
#         # return [(prefix, prefix) for prefix in set(prefixes) if prefix is not None]


#     def queryset(self, request, queryset):
#         request_session = request.session
        
#         # if any(key for key in request.GET if key.startswith('time_create')):
#         #     request.GET['time_create__isnull'] = ['False']
#         # else:
#         #     try:
#         #         del request.GET['time_create__isnull']
#         #     except Exception as ex:
#         #         print(ex)
#         print(request.GET)
#         print('request session', request_session.__dict__)
#         # utm_source_start = request.GET.get('utm_source_start')
#         utm_source = self.value()
#         # print(utm_source)
#         # print(22)
#         if utm_source:
#         #     # if not utm_source_start:
#             check_value = utm_source[:2].isdigit()
            
#             if not check_value:
#                 queryset = queryset.filter(utm_source__startswith=utm_source,
#                                            utm_source__isnull=False)
#             else:
#                 prefix_utm = request_session.get('prefix_utm')
#                 if prefix_utm:
#                     queryset = queryset.filter(utm_source__startswith=prefix_utm,
#                                             utm_source__endswith=utm_source,
#                                             utm_source__isnull=False)
                    
#                     # request.session['prefix_utm'] = None

#                 # utm_source_start = utm_source_start[0]
#                 # queryset = queryset.filter(utm_source__startswith=utm_source_start)
#         # print(queryset)
#         return queryset


class UTMInline(admin.StackedInline):
    model = UTM
    extra = 0
    classes = [
        'collapse',
        ]

    def has_change_permission(self, request, obj = ...):
        return False

#Отображение комментариев в админ панели
# @admin.register(Users)
class UsersAdmin(admin.ModelAdmin):
    list_display = (
        'username',
        'get_utm_source',
        'utm__utm_campaign',
        # 'product_count',
        # 'product_all_time_count',
        'time_create',
    )
    inlines = [UTMInline]

    def get_utm_source(self, obj):
        return obj.utm_source if obj.utm_source and (obj.utm_source.find('_') != 1) else obj.utm.source
    
    get_utm_source.short_description = 'UTM источник'

    readonly_fields = (
        'username',
        'first_name',
        'last_name',
        'utm_source',
        'time_create',
        # 'product_count',
        # 'product_all_time_count',
    )

    ordering = (
        '-time_create',
    )

    list_filter = (
        CustomDateTimeFilter,
        ("time_create", DateRangeFilterBuilder()),
        )
    
    fieldsets = [
        (
            None,
            {
                "fields": ['username',
                           "first_name",
                           "last_name",
                        #    "subscription",
                           "utm_source",
                        #    "product_count",
                        #    "product_all_time_count",
                        #    'related_utm',
                           "time_create"]
            },
        ),
    ]

    # def product_count(self, obj):
    #     wb_products = obj.wb_product_count if obj.wb_product_count else 0
    #     ozon_products = obj.ozon_product_count if obj.ozon_product_count else 0

    #     product_count = wb_products + ozon_products

    #     return f'{product_count} | wb: {wb_products} | ozon: {ozon_products}'
    
    # def product_all_time_count(self, obj):
    #     wb_products = obj.wb_total_count
    #     ozon_products = obj.ozon_total_count

    #     product_count = wb_products + ozon_products

    #     return f'{product_count} | wb: {wb_products} | ozon: {ozon_products}'

    # product_count.short_description = 'Число продуктов'
    # product_count.admin_order_field = 'all_product_count'

    # product_all_time_count.short_description = 'Число продуктов за всё время'
    # product_all_time_count.admin_order_field = 'all_product_count'
    
admin.site.register(Users, UsersAdmin)


class OrdersAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'request_type',
        'time_create',
    )

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user')
    
admin.site.register(Orders, OrdersAdmin)
# @admin.register(UserProducts)
# class UserProductsAdmin(admin.ModelAdmin):
#     list_display = (
#         'user',
#         'product_name',
#         'product_marker',
#         'time_create',
#     )

#     list_filter = (
#         # 'product__name',
#         'product__product_marker',
#         'user',
#         'time_create',
#     )

#     ordering = (
#         '-time_create',
#     )

#     def product_name(self, obj):
#         return obj.product.name
    
#     product_name.short_description = 'Название продукта'

#     def product_marker(self, obj):
#         return obj.product.product_marker
    
#     product_marker.short_description = 'Маркетплейс'

#     def get_queryset(self, request):
#         return super().get_queryset(request).select_related('product', 'user')
    
#     def has_change_permission(self, request, obj = ...):
#         return False
        # return super().has_change_permission(request, obj)

# @admin.register(UTM)
# class UTMAdmin(admin.ModelAdmin):
#     list_display = (
#         'pretty_user',
#         'source',
#     )

#     def pretty_user(seld, obj):
#         return f'{obj.user.tg_id} {obj.user.username}'
    
#     def get_queryset(self, request):
#         return super().get_queryset(request).select_related('user')
    
# admin.site.register(UTM, UTMAdmin)

# class CategoryChannelLinkInline(admin.TabularInline):
#     model = CategoryChannelLink
#     extra = 1

# class CategoryAdmin(admin.ModelAdmin):
#     list_display = (
#         'name',
#     )
#     inlines = [
#         CategoryChannelLinkInline,
#     ]

# admin.site.register(Category, CategoryAdmin)


# class ChannelLinkAdmin(admin.ModelAdmin):
#     list_display = (
#         'name',
#     )

# admin.site.register(ChannelLink, ChannelLinkAdmin)

# Переопределяем метод get_urls стандартного admin.site
# custom_admin_urls =  [
#         path('dashboard/', admin.site.admin_view(custom_admin_view), name='custom_admin_view'),
#         ]
# admin_urls = admin.site.get_urls()

# def get_admin_urls():
#     custom_urls = [
#         path('dashboard/', admin.site.admin_view(custom_admin_view), name='custom_admin_view'),
#     ]

#     return custom_urls + admin_urls

# admin.site.get_urls = lambda: get_admin_urls()


# class MyAdminSite(admin.AdminSite):
#     # site_header = "Custom Administration"
#     def get_urls(self):
#         urls = super().get_urls()
#         # print(urls)
#         custom_urls = [
#             path('dashboard/', admin.site.admin_view(custom_admin_view), name='custom_admin_view'),
#         ]
#         return custom_urls + urls

#     def get_app_list(self, request, app_label=None):
#         app_list = super().get_app_list(request, app_label)
#         if app_label is None or app_label == 'custom':
#             app_list.append(
#                 {
#                     "name": "Custom",
#                     "app_label": "custom",
#                     "models": [
#                         {
#                             "name": "Dashboard",
#                             "object_name": "dashboard",
#                             "admin_url": "/admin/dashboard",
#                             "view_only": True,
#                         }
#                     ],
#                 }
#             )
#         return app_list

#     def dashboard_view(self, request):
#         context = dict(self.each_context(request))
#         # context['parameters'] = config.get_parameters()
#         return TemplateResponse(request, 'admin/dashboard/custom_admin.page.html', context)
    

# admin.site = MyAdminSite()