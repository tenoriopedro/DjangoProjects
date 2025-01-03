# Generated by Django 5.1.4 on 2025-01-03 13:09

import utils.model_validator
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('site_setup', '0004_sitesetup_favicon'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sitesetup',
            name='favicon',
            field=models.ImageField(blank=True, default='', upload_to='assets/favicon/%Y/%m', validators=[utils.model_validator.validate_png]),
        ),
    ]