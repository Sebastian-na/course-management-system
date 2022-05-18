from rest_framework.serializers import ValidationError
from django.utils import timezone

def date_greater_than_now(d):
    if d < timezone.now():
        raise ValidationError("Date must be in the past")
    return d

def period_validator(period: int):
    if len(str(period)) != 5:
        raise ValidationError("Period must be a five digit number, e.g. 20222, where the four digits are the year and the last digit is the semester.")
    if str(period)[4] != '1' and str(period)[4] != '2':
        raise ValidationError("Semester must be either 1 or 2.")
    return period