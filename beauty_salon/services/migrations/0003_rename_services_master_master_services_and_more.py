# Generated by Django 5.1 on 2024-08-26 19:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0002_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='master',
            old_name='services',
            new_name='master_services',
        ),
        migrations.AddField(
            model_name='service',
            name='masters',
            field=models.ManyToManyField(related_name='services', to='services.master'),
        ),
    ]