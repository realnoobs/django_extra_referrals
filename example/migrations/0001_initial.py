# Generated by Django 3.0.5 on 2020-04-07 21:24

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('django_referrals', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Withdraw',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fullname', models.CharField(max_length=150)),
                ('amount', models.DecimalField(decimal_places=2, default=0, max_digits=15)),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('referral', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='django_referrals.Referral')),
            ],
        ),
        migrations.CreateModel(
            name='Donation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fullname', models.CharField(max_length=150)),
                ('amount', models.DecimalField(decimal_places=2, default=0, max_digits=15)),
                ('creator', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('referral', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='django_referrals.Referral')),
            ],
        ),
    ]