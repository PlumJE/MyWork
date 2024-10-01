from django.db import models

# Create your models here.
class LessonMap(models.Model):
    lessonmapnum = models.IntegerField(primary_key=True)
    name = models.TextField(blank=True, null=True)
    bgimg = models.TextField(blank=True, null=True)
    
    class Meta:
        managed = True
        db_table = 'LessonMap'

class Lesson(models.Model):
    lessonnum = models.IntegerField(primary_key=True)
    theme = models.TextField(blank=True, null=True)
    x_cor = models.FloatField(blank=True, null=True)
    y_cor = models.FloatField(blank=True, null=True)
    btnimg = models.TextField(blank=True, null=True)
    bgimg = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
    
class English(Lesson):
    class Meta:
        managed = True
        db_table = 'English'

class Chinese(Lesson):
    class Meta:
        managed = True
        db_table = 'Chinese'