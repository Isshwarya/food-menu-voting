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
    restaurant = models.ForeignKey(
        "Restaurant",
        on_delete=models.CASCADE,
    )
    menu_details = models.TextField("Menu")

    def save(self, *args, **kwargs):
        if not self.id:
            # No id indicates this was the first time, this object is going
            # to be saved.
            # Need not account for the case where user specifies timestamp to
            # created field, as anyways auto_now_add=True and so Django will
            # ignore the user specified value.
            matched = self.__class__.objects.filter(
                restaurant=self.restaurant,
                created__date=date.today())
            if matched:
                # The object has not completed its validation yet.
                if getattr(self, "restaurant"):
                    name = self.restaurant.name
                else:
                    name = "Missing Restaurant details"
                raise ValidationError("Today's menu for restaurant {} is "
                                      "already posted. You can make only "
                                      "updates to it".format(name))
        return super(Menu, self).save(*args, **kwargs)

    def __str__(self):
        return "Restaurant {}'s menu on {}".format(self.restaurant.name, self.created.date())


class Vote(CustomBaseModel):
    class Preference(models.IntegerChoices):
        FIRST = 1
        SECOND = 2
        THIRD = 3
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

    def save(self, *args, **kwargs):
        if not self.id and getattr(self, "employee"):
            # Check if the user has already voted for that particular
            # preference score for the current day
            existing = self.__class__.objects.filter(
                employee=self.employee,
                preference_score=self.preference_score,
                created__date=date.today()
            )
            if existing.count():
                raise Exception("You have already voted for "
                                "preference_score {} against restaurant {}"
                                " so you cannot vote for the same "
                                "preference again.".format(
                                    self.preference_score,
                                    existing[0].menu.restaurant.name))
        return super(Vote, self).save(*args, **kwargs)

    def __str__(self):
        return "Vote with score: {} for restaurant {}'s menu on {} by Employee id: {}".format(
            self.preference_score,
            self.menu.restaurant.name,
            self.menu.created,
            self.employee.employee_id
        )
