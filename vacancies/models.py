from django.db import models

from django.db.models import CharField, DateField, IntegerField, URLField, ForeignKey, CASCADE, TextField


class Specialty(models.Model):
    code = CharField(max_length=64)
    title = CharField(max_length=256)
    picture = URLField(default='https://place-hold.it/100x60')


class Company(models.Model):
    name = CharField(max_length=256)
    location = CharField(max_length=256)
    logo = URLField(default='https://place-hold.it/100x60')
    description = TextField()
    employee_count = IntegerField()


class Vacancy(models.Model):
    title = CharField(max_length=256)
    specialty = ForeignKey(Specialty, related_name="vacancies", on_delete=CASCADE)
    company = ForeignKey(Company, related_name="vacancies", on_delete=CASCADE)
    skills = TextField()
    description = TextField()
    salary_min = IntegerField()
    salary_max = IntegerField()
    published_at = DateField()
