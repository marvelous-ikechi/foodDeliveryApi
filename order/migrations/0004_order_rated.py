# Generated by Django 3.2 on 2021-04-17 17:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0003_auto_20210417_1646'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='rated',
            field=models.BooleanField(default=False, editable=False),
        ),
    ]
