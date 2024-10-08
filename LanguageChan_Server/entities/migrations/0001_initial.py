# Generated by Django 5.1.1 on 2024-09-22 05:39

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CharaInfo',
            fields=[
                ('charanum', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.TextField(blank=True, null=True)),
                ('headimg', models.TextField(blank=True, null=True)),
                ('fullimg', models.TextField(blank=True, null=True)),
                ('fightimg', models.TextField(blank=True, null=True)),
                ('atkexp', models.TextField(blank=True, null=True)),
                ('dfsxep', models.TextField(blank=True, null=True)),
            ],
            options={
                'db_table': 'CharaInfo',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='EnemyInfo',
            fields=[
                ('enemynum', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.TextField(blank=True, null=True)),
                ('headimg', models.TextField(blank=True, null=True)),
                ('fightimg', models.TextField(blank=True, null=True)),
                ('atk', models.IntegerField(blank=True, null=True)),
                ('dfs', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'db_table': 'EnemyInfo',
                'managed': True,
            },
        ),
    ]
