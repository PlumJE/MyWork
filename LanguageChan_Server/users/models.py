from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class UsersChara(models.Model):
    usernum = models.IntegerField(null=True)# .ForeignKey(User, models.DO_NOTHING, db_column='usernum', blank=True, null=True)
    charanum = models.IntegerField(null=True)# .ForeignKey('entities.CharaInfo', models.DO_NOTHING, db_column='charanum', blank=True, null=True)
    lvl = models.IntegerField(null=True)

    class Meta:
        managed = True
        db_table = 'UsersChara'
        unique_together = ('usernum', 'charanum')


class UsersFriends(models.Model):
    usernum = models.IntegerField(null=True)# .ForeignKey(User, models.DO_NOTHING, db_column='usernum', blank=True, null=True)
    friendnum = models.IntegerField(null=True)# .ForeignKey(User, models.DO_NOTHING, db_column='friendnum', related_name='usersfriends_friendnum_set', blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'UsersFriends'
        unique_together = ('usernum', 'friendnum')


class UsersItem(models.Model):
    usernum = models.IntegerField(unique=True, null=True)# .ForeignKey(User, models.DO_NOTHING, db_column='usernum', blank=True, null=True)
    money = models.IntegerField(null=True)
    jewel = models.IntegerField(null=True)

    class Meta:
        managed = True
        db_table = 'UsersItem'


class UsersProgress(models.Model):
    usernum = models.IntegerField(null=True)# .ForeignKey(User, models.DO_NOTHING, db_column='usernum', blank=True, null=True)
    lessonmapnum = models.IntegerField(null=True)# .ForeignKey('lessons.LessonMap', models.DO_NOTHING, db_column='lessonmapnum', blank=True, null=True)
    progress = models.IntegerField(null=True)

    class Meta:
        managed = True
        db_table = 'UsersProgress'
        unique_together = ('usernum', 'lessonmapnum')


class UsersOption(models.Model):
    usernum = models.IntegerField(unique=True, null=True)# .ForeignKey(User, models.DO_NOTHING, db_column='usernum', blank=True, null=True)
    birthday = models.TextField(null=True)
    language = models.TextField(default='Korean')
    
    class Meta:
        managed = True
        db_table = 'UsersOption'
