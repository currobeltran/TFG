# Generated by Django 3.1.6 on 2021-04-22 16:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_auto_20210422_1613'),
    ]

    operations = [
        migrations.AlterField(
            model_name='asignatura',
            name='CreditosGA',
            field=models.DecimalField(decimal_places=2, max_digits=2),
        ),
        migrations.AlterField(
            model_name='asignatura',
            name='CreditosGR',
            field=models.DecimalField(decimal_places=2, max_digits=2),
        ),
    ]