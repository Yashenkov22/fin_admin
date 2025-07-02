# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from datetime import datetime
from django.db import models
from django.forms import ValidationError
from django.utils import timezone

class AlembicVersion(models.Model):
    version_num = models.CharField(primary_key=True, max_length=32)

    class Meta:
        managed = False
        db_table = 'alembic_version'


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.SmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class Users(models.Model):
    tg_id = models.BigAutoField(primary_key=True)
    username = models.CharField(blank=True, null=True)
    first_name = models.CharField(blank=True, null=True)
    last_name = models.CharField(blank=True, null=True)
    time_create = models.DateTimeField('Время добавления',
                                       blank=True,
                                       null=True)
    last_login_time = models.DateTimeField(blank=True, null=True)
    utm_source = models.CharField('UTM метка',
                                  blank=True,
                                  null=True)
    is_active = models.BooleanField('Активность', default=True)
    class Meta:
        managed = False
        db_table = 'users'
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return f'Пользователь - ID {self.tg_id} {self.username}'
    


class Orders(models.Model):

    request_type_chioces = [
        ('Сотрудничество', 'Сотрудничество'),
        ('Сообщить об ошибке', 'Сообщить об ошибке'),
    ]
    request_type = models.CharField('Тип обращения',
                                    max_length=255,
                                    choices=request_type_chioces)
    comment = models.TextField('Комментарий к обращению')
    user = models.ForeignKey(Users,
                             on_delete=models.CASCADE,
                             verbose_name='Пользователь')
    time_create = models.DateTimeField('Время добавления',
                                       blank=True,
                                       null=True)
    class Meta:
        managed = False
        db_table = 'orders'
        verbose_name = 'Обращение'
        verbose_name_plural = 'Обращения'

    def __str__(self):
        return f'Обращение от {self.time_create}, юзер {self.user}'


class UTM(models.Model):
    keitaro_id = models.CharField(max_length=255, blank=True, null=True)
    utm_source = models.CharField(max_length=255, blank=True, null=True)
    utm_medium = models.CharField(max_length=255, blank=True, null=True)
    utm_campaign = models.CharField(max_length=255, blank=True, null=True)
    utm_content = models.CharField(max_length=255, blank=True, null=True)
    utm_term = models.CharField(max_length=255, blank=True, null=True)
    banner_id = models.CharField(max_length=255, blank=True, null=True)
    campaign_name = models.CharField(max_length=255, blank=True, null=True)
    campaign_name_lat = models.CharField(max_length=255, blank=True, null=True)
    campaign_type = models.CharField(max_length=255, blank=True, null=True)
    campaign_id = models.CharField(max_length=255, blank=True, null=True)
    creative_id = models.CharField(max_length=255, blank=True, null=True)
    device_type = models.CharField(max_length=255, blank=True, null=True)
    gbid = models.CharField(max_length=255, blank=True, null=True)
    keyword = models.CharField(max_length=255, blank=True, null=True)
    phrase_id = models.CharField(max_length=255, blank=True, null=True)
    coef_goal_context_id = models.CharField(max_length=255, blank=True, null=True)
    match_type = models.CharField(max_length=255, blank=True, null=True)
    matched_keyword = models.CharField(max_length=255, blank=True, null=True)
    adtarget_name = models.CharField(max_length=255, blank=True, null=True)
    adtarget_id = models.CharField(max_length=255, blank=True, null=True)
    position = models.CharField(max_length=255, blank=True, null=True)
    position_type = models.CharField(max_length=255, blank=True, null=True)
    source = models.CharField(max_length=255, blank=True, null=True)
    source_type = models.CharField(max_length=255, blank=True, null=True)
    region_name = models.CharField(max_length=255, blank=True, null=True)
    region_id = models.CharField(max_length=255, blank=True, null=True)
    yclid = models.CharField(max_length=255, blank=True, null=True)
    client_id = models.CharField(max_length=255, blank=True, null=True)
    user = models.OneToOneField(Users, on_delete=models.CASCADE, related_name='utm')
    
    class Meta:
        db_table = 'utms'
        managed = False

    def __str__(self):
        return f'{self.user.tg_id} {self.keitaro_id} {self.source}'
    

class MassSendMessage(models.Model):
    send_to_list = [
        (None, None),
        ('Fin бот группа', 'Fin бот группа'),
        ('Fin бот канал', 'Fin бот канал'),
        ('Админу', 'Админу'),
    ]
    name = models.CharField('Название',
                            max_length=255)
    content = models.TextField('Контент')
    delay_time = models.DateTimeField('Отложить выполенение до',
                                      blank=True,
                                      null=True,
                                      default=None,
                                      help_text='Если оставить поле пустым пост отправится сразу после нажатия соответствующих кнопок снизу')
    send_to = models.CharField('Куда отправить отложенный пост', max_length=255, choices=send_to_list, default=None, null=True, blank=True)
    has_delayed_task = models.BooleanField('Запланировано отложенная отправка?', default=False)

    class Meta:
        db_table = 'mass_send_message'
        managed = False
        verbose_name = 'Массовая рассылка'
        verbose_name_plural = 'Массовые рассылки'

    def __str__(self):
        return self.name


    def clean(self):
        super().clean()

        if any(el for el in (self.delay_time, self.send_to)) and not (all(el for el in (self.delay_time, self.send_to))):
            raise ValidationError('Нужно выбрать И дату И куда отправить')
        
        if self.delay_time and self.delay_time < timezone.now():
            raise ValidationError('Введите корректную дату отложенного поста')
            
# Модель изображений связанных с рассылкой 
# class MassSendFile(models.Model):
#     image = models.ImageField('Изображение',
#                               upload_to='mass_send/files/')
#     message = models.OneToOneField(MassSendMessage,
#                                  on_delete=models.CASCADE,
#                                  verbose_name='Cообщение',
#                                  related_name='image')
#     file_id = models.CharField('ID файла',
#                                max_length=255,
#                                null=True,
#                                blank=True,
#                                default=None)
    
#     def __str__(self):
#         return f'Изображение {self.id}'
    
#     class Meta:
#         db_table = 'mass_send_image'
#         managed = False
#         verbose_name = 'Изображение для расслыки'
#         verbose_name_plural = 'Изображения для расслыки'

# Модель видео связанных с рассылкой 
# class MassSendVideo(models.Model):
#     video = models.FileField('Видео',
#                              upload_to='mass_send/videos/')
#     message = models.OneToOneField(MassSendMessage,
#                                  on_delete=models.CASCADE,
#                                  verbose_name='Cообщение',
#                                  related_name='video')
#     file_id = models.CharField('ID файла',
#                                max_length=255,
#                                null=True,
#                                blank=True,
#                                default=None)

#     def __str__(self):
#         return f'Видео {self.id}'

#     class Meta:
#         db_table = 'mass_send_video'
#         managed = False
#         verbose_name = 'Видео для расслыки'
#         verbose_name_plural = 'Видео для расслыки'


# Модель файлов связанных с рассылкой 
class MassSendFile(models.Model):
    file = models.FileField('Файл',
                            upload_to='mass_send/files/')
    message = models.OneToOneField(MassSendMessage,
                                 on_delete=models.CASCADE,
                                 verbose_name='Cообщение',
                                 related_name='file')
    file_id = models.CharField('ID файла',
                               max_length=255,
                               null=True,
                               blank=True,
                               default=None)
    
    def __str__(self):
        return f'Файл {self.id}'

    class Meta:
        db_table = 'mass_send_file'
        managed = False
        verbose_name = 'Файл для расслыки'
        verbose_name_plural = 'Файлы для расслыки'


