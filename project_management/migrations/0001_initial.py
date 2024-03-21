# Generated by Django 4.1.5 on 2024-03-14 22:54

from django.db import migrations, models
import project_management.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Board',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('description', models.TextField(blank=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_updated', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ['-date_updated'],
            },
        ),
        migrations.CreateModel(
            name='Column',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('restID', models.CharField(default=1, max_length=32)),
                ('title', models.CharField(max_length=255)),
                ('column_order', models.PositiveIntegerField(db_index=True, default=0, editable=False)),
                ('is_valid', models.BooleanField(default=1)),
            ],
            options={
                'ordering': ['column_order'],
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Label',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('color', models.CharField(max_length=7)),
            ],
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('restID', models.CharField(default=1, max_length=32)),
                ('title', models.CharField(error_messages={'required': 'Enter title for the task.'}, max_length=255)),
                ('description', models.TextField(blank=True)),
                ('priority', models.CharField(choices=[('H', 'High'), ('M', 'Medium'), ('L', 'Low')], default='M', max_length=1)),
                ('file', models.FileField(blank=True, max_length=1000, null=True, upload_to=project_management.models.get_report_file_uploader_path)),
                ('date', models.DateField(blank=True, null=True)),
                ('task_order', models.PositiveIntegerField(default=0)),
                ('is_valid', models.BooleanField(default=1)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_updated', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ['id'],
            },
        ),
    ]
