# Generated by Django 4.1.5 on 2024-03-14 22:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('project', '0001_initial'),
        ('lms', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='projectparcel',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='project.project'),
        ),
    ]