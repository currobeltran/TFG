# Generated by Django 3.1.6 on 2021-04-22 16:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_auto_20210422_0919'),
    ]

    operations = [
        migrations.AlterField(
            model_name='asignatura',
            name='CreditosGA',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='asignatura',
            name='CreditosGR',
            field=models.FloatField(),
        ),
    ]