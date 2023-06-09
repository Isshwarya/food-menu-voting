# Generated by Django 4.2.1 on 2023-05-25 14:58

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0010_remove_menu_unique_everyday_menu_per_restaurant_and_more'),
    ]

    operations = [


        migrations.AddField(
            model_name='employee',
            name='date_created',
            field=models.DateField(
                auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='menu',
            name='date_created',
            field=models.DateField(
                auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='restaurant',
            name='date_created',
            field=models.DateField(
                auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='vote',
            name='date_created',
            field=models.DateField(
                auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddConstraint(
            model_name='menu',
            constraint=models.UniqueConstraint(fields=(
                'restaurant', 'date_created'), name='unique_everyday_menu_per_restaurant'),
        ),
        migrations.AddConstraint(
            model_name='vote',
            constraint=models.UniqueConstraint(fields=(
                'employee', 'preference_score', 'date_created'), name='unique_preference_score_per_employee'),
        ),
    ]
