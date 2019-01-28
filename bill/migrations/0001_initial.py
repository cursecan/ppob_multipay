# Generated by Django 2.1.5 on 2019-01-28 04:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('payment', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('ppob', '0001_initial'),
        ('instanpay', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Billing',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('update', models.DateTimeField(auto_now=True)),
                ('delete', models.DateTimeField(blank=True, null=True)),
                ('is_delete', models.BooleanField(default=False)),
                ('debit', models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ('credit', models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ('balance', models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ('seq', models.PositiveSmallIntegerField(default=1)),
                ('instanpay_trx', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='instanpay.Transaction')),
            ],
            options={
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='FlagKliring',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('update', models.DateTimeField(auto_now=True)),
                ('delete', models.DateTimeField(blank=True, null=True)),
                ('is_delete', models.BooleanField(default=False)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=12)),
                ('buyer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='f_buyer', to=settings.AUTH_USER_MODEL)),
                ('leader', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='f_leader', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='Kliring',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('update', models.DateTimeField(auto_now=True)),
                ('delete', models.DateTimeField(blank=True, null=True)),
                ('is_delete', models.BooleanField(default=False)),
                ('seq', models.PositiveSmallIntegerField(default=1)),
                ('loan', models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ('payment', models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ('buyer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='buyer', to=settings.AUTH_USER_MODEL)),
                ('flag', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='bill.FlagKliring')),
                ('instanpay_trx', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='instanpay.Transaction')),
                ('leader', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='leader', to=settings.AUTH_USER_MODEL)),
                ('ppob_trx', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='ppob.Transaction')),
                ('prev_kliring', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='bill.Kliring')),
            ],
            options={
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='Profit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('update', models.DateTimeField(auto_now=True)),
                ('delete', models.DateTimeField(blank=True, null=True)),
                ('is_delete', models.BooleanField(default=False)),
                ('profit', models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ('commision', models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ('witdraw', models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ('return_back', models.BooleanField(default=False)),
                ('buyer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='prof_buyer', to=settings.AUTH_USER_MODEL)),
                ('instanpay_trx', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='instanpay.Transaction')),
                ('leader', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='prof_leader', to=settings.AUTH_USER_MODEL)),
                ('ppob_trx', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='ppob.Transaction')),
            ],
            options={
                'ordering': ['-id'],
            },
        ),
        migrations.AddField(
            model_name='billing',
            name='kliring',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='bill.Kliring'),
        ),
        migrations.AddField(
            model_name='billing',
            name='payment',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='payment.Payment'),
        ),
        migrations.AddField(
            model_name='billing',
            name='ppob_trx',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='ppob.Transaction'),
        ),
        migrations.AddField(
            model_name='billing',
            name='prev_bill',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='bill.Billing'),
        ),
        migrations.AddField(
            model_name='billing',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
