# Generated by Django 5.0.6 on 2024-06-04 03:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth_setup', '0002_alter_user_is_active_friendrequest'),
    ]

    operations = [
        migrations.CreateModel(
            name='Test_mode',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, null=True)),
                ('password', models.CharField(max_length=8)),
            ],
        ),
        migrations.RemoveField(
            model_name='user',
            name='password1',
        ),
        migrations.RemoveField(
            model_name='user',
            name='password2',
        ),
    ]
