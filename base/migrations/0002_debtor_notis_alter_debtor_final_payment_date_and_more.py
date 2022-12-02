# Generated by Django 4.1.3 on 2022-12-01 13:01

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('notis', '0001_initial'),
        ('base', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='debtor',
            name='notis',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='notis.notifications'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='debtor',
            name='final_payment_date',
            field=models.DateField(default=datetime.date(2023, 3, 1), null=True),
        ),
        migrations.AlterField(
            model_name='debtor',
            name='first_payment_date',
            field=models.DateField(default=datetime.date(2022, 12, 31), null=True),
        ),
        migrations.AlterField(
            model_name='debtor',
            name='second_payment_date',
            field=models.DateField(default=datetime.date(2023, 1, 30), null=True),
        ),
    ]