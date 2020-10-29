from django.db import models

# Create your models here.

class Investor(models.Model):
    surname = models.CharField(max_length=150, verbose_name="Фамилия")
    name = models.CharField(max_length=150, verbose_name="Имя")
    patronymic = models.CharField(max_length=150, verbose_name="Отчество")
    number_of_passport = models.IntegerField(unique=True)
    birthday = models.DateField(max_length=150, verbose_name="Дата рождения")
    place_of_birth = models.CharField(max_length=150, verbose_name="Место рождения")
    date_of_passport = models.DateField(max_length=150, verbose_name="Дата получения паспорта")
    code = models.SlugField(max_length=150, verbose_name="Код-подразделения")
    issued_by = models.CharField(max_length=150, verbose_name="Кем выдан")
    place_of_living = models.CharField(max_length=150, verbose_name="Место прописки")
    file_of_pass = models.FileField(verbose_name="Файл документа", blank=True)

    def __str__(self):
        return (str(self.surname) + " " + str(self.name) + " : " + str(self.number_of_passport))

class Rules(models.Model):
    rule_1 = models.BooleanField(default = False)
    rule_2 = models.BooleanField(default = False)
    rule_3 = models.BooleanField(default = False)
    invest = models.OneToOneField(Investor, on_delete = models.CASCADE)


class Qualification(models.Model):
    invest = models.OneToOneField(Investor, on_delete = models.CASCADE)
    qualification_file = models.FileField(blank=True)
    qualification = models.BooleanField(default = False)
