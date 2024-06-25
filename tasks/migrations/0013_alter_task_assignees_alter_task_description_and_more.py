# Generated by Django 5.0.6 on 2024-06-23 17:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0012_alter_task_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='assignees',
            field=models.ManyToManyField(blank=True, to='tasks.teammember'),
        ),
        migrations.AlterField(
            model_name='task',
            name='description',
            field=models.TextField(default='Description'),
            preserve_default=False,
        ),
        migrations.AlterUniqueTogether(
            name='teammember',
            unique_together={('team', 'participant')},
        ),
    ]