# Generated by Django 3.2.18 on 2023-05-11 12:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='achareuser',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]
