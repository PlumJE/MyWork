from django.db import models

# Create your models here.
class CharaInfo(models.Model):
    charanum = models.IntegerField(primary_key=True)
    name = models.TextField(blank=True, null=True)
    headimg = models.TextField(blank=True, null=True)
    fullimg = models.TextField(blank=True, null=True)
    fightimg = models.TextField(blank=True, null=True)
    atkexp = models.TextField(blank=True, null=True)
    dfsxep = models.TextField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'CharaInfo'


class EnemyInfo(models.Model):
    enemynum = models.IntegerField(primary_key=True)
    name = models.TextField(blank=True, null=True)
    headimg = models.TextField(blank=True, null=True)
    fightimg = models.TextField(blank=True, null=True)
    atk = models.IntegerField(blank=True, null=True)
    dfs = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'EnemyInfo'
