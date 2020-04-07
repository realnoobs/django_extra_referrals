# Generated by Django 3.0.5 on 2020-04-07 16:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('django_referrals', '0002_auto_20200407_2336'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='is_verified',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='transaction',
            name='verified_at',
            field=models.DateTimeField(blank=True, editable=False, null=True, verbose_name='Verified at'),
        ),
    ]
