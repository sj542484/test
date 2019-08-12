# Generated by Django 2.1.8 on 2019-07-01 01:37

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='EquipmentList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('equipment_name', models.CharField(max_length=50)),
                ('equipment_model', models.CharField(max_length=50)),
                ('equipment_uuid', models.CharField(max_length=50, unique=True)),
                ('platform_verion', models.CharField(max_length=50)),
                ('start_but_statue', models.IntegerField(default=0)),
                ('statue_statue', models.IntegerField(default=0)),
                ('gid', models.IntegerField(null=True)),
                ('report', models.CharField(max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='ItemType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('side', models.CharField(max_length=50)),
                ('item', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='SideType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('side', models.CharField(max_length=50, unique=True)),
            ],
        ),
    ]