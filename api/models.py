from datetime import date
from django.conf import settings
from django.db import models
from django.core.exceptions import ValidationError
import django.contrib.auth as django_auth


class CustomBaseModel(models.Model):
    def save(self, *args, **kwargs):
        # Does validation
        self.full_clean()
        return super(CustomBaseModel, self).save(*args, **kwargs)

    created = models.DateTimeField(auto_now_add=True)
    # This duplication in data between created and date_created is
    # intended just to make it easier to layout Unique Constraints
    # later. Other solutions increases query complexity whereas
    # the extra storage spent for storing this duplicated data is
    # not significant.
    date_created = models.DateField(auto_now_add=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        blank=True, null=True
    )

    class Meta:
        abstract = True


class Restaurant(CustomBaseModel):
    name = models.CharField("Name", max_length=240)
    email = models.EmailField(unique=True)
    address = models.TextField("Address")

    def __str__(self):
        return self.name


class Employee(CustomBaseModel):
    user = models.OneToOneField(
        django_auth.models.User, on_delete=models.CASCADE,
        related_name="identifying_user")
    employee_id = models.IntegerField(unique=True)

    def __str__(self):
        return self.user.username


class Menu(CustomBaseModel):
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["restaurant", "date_created"], name="unique_everyday_menu_per_restaurant"
            )
        ]
    restaurant = models.ForeignKey(
        "Restaurant",
        on_delete=models.CASCADE,
    )
    menu_details = models.TextField("Menu")

    def __str__(self):
        return "Restaurant {}'s menu on {}".format(self.restaurant.name, self.created.date())


class Vote(CustomBaseModel):
    class Preference(models.IntegerChoices):
        FIRST = 1
        SECOND = 2
        THIRD = 3

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["employee", "preference_score", "date_created"], name="unique_preference_score_per_employee"
            )
        ]
    menu = models.ForeignKey(
        "Menu",
        on_delete=models.CASCADE,
    )
    employee = models.ForeignKey(
        "Employee",
        on_delete=models.CASCADE,
    )
    preference_score = models.IntegerField(choices=Preference.choices,
                                           default=Preference.FIRST)

    def __str__(self):
        return "Vote with score: {} for restaurant {}'s menu on {} by Employee id: {}".format(
            self.preference_score,
            self.menu.restaurant.name,
            self.menu.created,
            self.employee.employee_id
        )
