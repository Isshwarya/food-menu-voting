from datetime import date
from django.db import models
from django.core.exceptions import ValidationError


class CustomBaseModel(models.Model):
    def save(self, *args, **kwargs):
        # Does validation
        self.full_clean()
        return super(CustomBaseModel, self).save(*args, **kwargs)

    class Meta:
        abstract = True


class Restaurant(CustomBaseModel):
    name = models.CharField("Name", max_length=240)
    email = models.EmailField(unique=True)
    address = models.TextField("Address")
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Employee(CustomBaseModel):
    name = models.CharField("Name", max_length=240)
    email = models.EmailField(unique=True)
    employee_id = models.IntegerField(unique=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Menu(CustomBaseModel):
    restaurant = models.ForeignKey(
        "Restaurant",
        on_delete=models.CASCADE,
    )
    menu_details = models.TextField("Menu")
    created = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.id:
            # No id indicates this was the first time, this object is going
            # to be saved.
            # Need not account for the case where user specifies timestamp to
            # created field, as anyways auto_now_add=True and so Django will
            # ignore the user specified value.
            matched = self.__class__.objects.filter(
                created__date=date.today())
            if matched:
                # The object has not completed its validation yet.
                if getattr(self, "restaurant"):
                    name = self.restaurant.name
                else:
                    name = "Missing Restaurant details"
                raise ValidationError("Today's menu for restaurant {} is "
                                      "already posted. You can make only "
                                      "updates to it, please use PUT/PATCH "
                                      "request.".format(name))
        return super(Menu, self).save(*args, **kwargs)

    def __str__(self):
        return "Restaurant {}'s menu on {} is: {}".format(self.restaurant.name, self.created, self.menu_details)


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
    preference_score = models.IntegerField(choices=Preference.choices)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "Vote with score: {} for restaurant {}'s menu on {} by Employee id: {}".format(
            self.preference_score,
            self.menu.restaurant.name,
            self.menu.created,
            self.employee.id
        )
