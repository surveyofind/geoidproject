# Generated by Django 5.0.4 on 2024-11-05 05:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('geocalculation_app', '0004_user_goverment_idcard_no_user_student_idcard_no_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='user_types',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
