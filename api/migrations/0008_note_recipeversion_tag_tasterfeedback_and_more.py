# Generated by Django 4.0.5 on 2022-06-21 20:25

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_rename_title_test_base_recipe_alter_test_chef'),
    ]

    operations = [
        migrations.CreateModel(
            name='Note',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('note', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='RecipeVersion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('version_number', models.CharField(max_length=3)),
                ('ingredients', models.TextField()),
                ('recipe_steps', models.TextField()),
                ('image', models.ImageField(blank=True, null=True, upload_to='')),
                ('ready_for_feedback', models.BooleanField(default=False)),
                ('successful_variation', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('chef', models.ForeignKey(max_length=255, on_delete=django.db.models.deletion.CASCADE, related_name='chefs', to=settings.AUTH_USER_MODEL)),
                ('recipe_note', models.ForeignKey(max_length=255, on_delete=django.db.models.deletion.CASCADE, related_name='recipe_notes', to='api.note')),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tag', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='TasterFeedback',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.CharField(choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5')], default='3', max_length=6)),
                ('saltiness', models.CharField(choices=[('Too Little', 'Too Little'), ('Just Right', 'Just Right'), ('Too Much', 'Too Much')], default='Just Right', max_length=11)),
                ('sweetness', models.CharField(choices=[('Too Little', 'Too Little'), ('Just Right', 'Just Right'), ('Too Much', 'Too Much')], default='Just Right', max_length=11)),
                ('portion', models.CharField(choices=[('Too Little', 'Too Little'), ('Just Right', 'Just Right'), ('Too Much', 'Too Much')], default='Just Right', max_length=11)),
                ('texture', models.CharField(choices=[('Yes', 'Yes'), ('No', 'No')], default='Yes', max_length=5)),
                ('additional_comment', models.CharField(blank=True, max_length=200, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('test_recipe', models.ForeignKey(max_length=255, on_delete=django.db.models.deletion.CASCADE, related_name='test_recipe', to='api.recipeversion')),
                ('test_version_number', models.ForeignKey(max_length=3, on_delete=django.db.models.deletion.CASCADE, related_name='test_version_number', to='api.recipeversion')),
                ('tester', models.ForeignKey(max_length=50, on_delete=django.db.models.deletion.CASCADE, related_name='taster', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.RemoveField(
            model_name='test',
            name='base_recipe',
        ),
        migrations.RemoveField(
            model_name='test',
            name='chef',
        ),
        migrations.DeleteModel(
            name='Recipe',
        ),
        migrations.DeleteModel(
            name='Test',
        ),
        migrations.AddField(
            model_name='recipeversion',
            name='recipe_note_tag',
            field=models.ForeignKey(max_length=255, on_delete=django.db.models.deletion.CASCADE, related_name='tags', to='api.tag'),
        ),
        migrations.AddField(
            model_name='note',
            name='note_tag',
            field=models.ForeignKey(max_length=255, on_delete=django.db.models.deletion.CASCADE, related_name='note_tags', to='api.tag'),
        ),
        migrations.AddField(
            model_name='note',
            name='recipe_version',
            field=models.ForeignKey(max_length=255, on_delete=django.db.models.deletion.CASCADE, related_name='recipe_versions', to='api.recipeversion'),
        ),
    ]
