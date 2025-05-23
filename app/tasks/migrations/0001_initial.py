# Generated by Django 5.2 on 2025-05-11 17:41

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('lessons', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Assignment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('due_date', models.DateTimeField(blank=True, null=True)),
                ('module', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='assignments', to='lessons.module')),
            ],
        ),
    ]
