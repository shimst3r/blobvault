# Generated by Django 3.0.5 on 2020-04-19 20:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_remove_blob_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='blob',
            name='mimetype',
            field=models.TextField(default='application/octet-stream'),
            preserve_default=False,
        ),
    ]
