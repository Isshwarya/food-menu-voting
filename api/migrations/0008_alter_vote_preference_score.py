# Generated by Django 4.2.1 on 2023-05-10 07:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_alter_employee_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vote',
            name='preference_score',
            field=models.IntegerField(choices=[(1, 'First'), (2, 'Second'), (3, 'Third')], default=1),
        ),
    ]
