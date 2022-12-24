# Generated by Django 4.1.3 on 2022-11-18 13:36

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0017_debtor_final_payment_date_debtor_second_payment_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='debtor',
            name='final_payment_date',
            field=models.DateField(default=datetime.date(2023, 2, 16), null=True),
        ),
        migrations.AlterField(
            model_name='debtor',
            name='first_payment_date',
            field=models.DateField(default=datetime.date(2022, 12, 18), null=True),
        ),
        migrations.AlterField(
            model_name='debtor',
            name='second_payment_date',
            field=models.DateField(default=datetime.date(2023, 1, 17), null=True),
        ),
    ]
