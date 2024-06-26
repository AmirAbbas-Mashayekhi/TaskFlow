# Generated by Django 5.0.6 on 2024-06-24 21:49

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0013_alter_task_assignees_alter_task_description_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='task',
            name='assignees',
        ),
        migrations.AlterField(
            model_name='task',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.CreateModel(
            name='Assignee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tasks.task')),
                ('team_member', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='assigned', to='tasks.teammember')),
            ],
        ),
    ]
