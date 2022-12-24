# Generated by Django 4.1.3 on 2022-12-23 04:24

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0018_alter_debtor_final_payment_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='debtor',
            name='final_payment_date',
            field=models.DateField(default=datetime.date(2023, 3, 22), null=True),
        ),
        migrations.AlterField(
            model_name='debtor',
            name='first_payment_date',
            field=models.DateField(default=datetime.date(2023, 1, 21), null=True),
        ),
        migrations.AlterField(
            model_name='debtor',
            name='second_payment_date',
            field=models.DateField(default=datetime.date(2023, 2, 20), null=True),
        ),
    ]
