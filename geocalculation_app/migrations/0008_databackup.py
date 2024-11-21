# Generated by Django 5.0.7 on 2024-11-14 08:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('geocalculation_app', '0007_alter_user_status'),
    ]

    operations = [
        migrations.CreateModel(
            name='databackup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(blank=True, max_length=100, null=True)),
                ('user_type', models.CharField(blank=True, max_length=100, null=True)),
                ('pointdownload', models.CharField(blank=True, max_length=100, null=True)),
                ('updatetime', models.CharField(blank=True, max_length=45, null=True)),
            ],
        ),
    ]
