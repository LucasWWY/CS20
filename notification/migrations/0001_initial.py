# Generated by Django 4.1.5 on 2024-03-25 13:51

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('summary', models.CharField(max_length=256)),
                ('url', models.CharField(blank=True, max_length=100, null=True)),
                ('target_id', models.CharField(blank=True, max_length=36, null=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'ordering': ['-timestamp'],
            },
        ),
        migrations.CreateModel(
            name='NotificationStatus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_read', models.BooleanField(default=False)),
                ('notification', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='status', to='notification.notification')),
            ],
            options={
                'ordering': ['-notification__timestamp'],
            },
        ),
    ]
