# Generated by Django 4.0.1 on 2022-08-06 08:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0006_alter_taskcaserelevance_case'),
    ]

    operations = [
        migrations.AddField(
            model_name='taskcaserelevance',
            name='cases_sequence',
            field=models.TextField(default=[], null=True, verbose_name='用例顺序'),
        ),
    ]