# Generated by Django 4.1.3 on 2023-05-11 13:13

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('request', '0004_rename_timestamp_friendrequest_created_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='friendrequest',
            name='fromUser',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='fromUser', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='friendrequest',
            name='toUser',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='toUser', to=settings.AUTH_USER_MODEL),
        ),
    ]
