# Generated by Django 4.0.5 on 2022-06-30 17:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0023_alter_tasterfeedback_tester'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tasterfeedback',
            name='additional_comment',
            field=models.CharField(max_length=200, null=True),
        ),
    ]
