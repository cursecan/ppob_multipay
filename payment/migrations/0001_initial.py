# Generated by Django 2.1.5 on 2019-01-28 04:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='KlirPayment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('update', models.DateTimeField(auto_now=True)),
                ('delete', models.DateTimeField(blank=True, null=True)),
                ('is_delete', models.BooleanField(default=False)),
                ('pay', models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ('extra_pay', models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ('receiver', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='c_receiver', to=settings.AUTH_USER_MODEL)),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='c_sender', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('update', models.DateTimeField(auto_now=True)),
                ('delete', models.DateTimeField(blank=True, null=True)),
                ('is_delete', models.BooleanField(default=False)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=12)),
                ('description', models.TextField(blank=True, max_length=500)),
                ('kliring_payment', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='payment.KlirPayment')),
                ('receiver', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='receiver', to=settings.AUTH_USER_MODEL)),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sender', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-id'],
            },
        ),
    ]
