# Generated by Django 4.0.4 on 2022-08-26 07:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pandasdemo', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ethanol',
            name='MTonPrice',
            field=models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=7, null=True),
        ),
    ]
