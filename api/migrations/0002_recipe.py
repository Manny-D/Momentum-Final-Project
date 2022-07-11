# Generated by Django 4.0.5 on 2022-06-17 21:41

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Recipe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('recipe', models.TextField()),
                ('ingredients', models.TextField()),
                ('recipe_complete', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('chef', models.ForeignKey(max_length=255, on_delete=django.db.models.deletion.CASCADE, related_name='chef', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]