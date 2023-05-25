# Generated by Django 4.1.3 on 2023-05-25 11:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('request', '0008_alter_friendrequest_group'),
    ]

    operations = [
        migrations.AlterField(
            model_name='friendrequest',
            name='group',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='auth.group'),
        ),
    ]