# Generated by Django 2.2.4 on 2019-08-27 19:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tenants', '0001_initial'),
        ('ds', '0008_auto_20190827_1621'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='dictionary',
            unique_together={('tenant', 'grpname', 'typekbn', 'distword')},
        ),
    ]
