from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import generics
from .models import *
from .serializer import *
from django.http import JsonResponse

class InvestorCreateView(generics.CreateAPIView):
    serializer_class = InvestorSerializer

#Получение текущего статуса квалификации
@api_view(['GET', ])
def status_qual(request, pas):
    try:
        investor = Investor.objects.get(number_of_passport=pas)
        qualificat = Qualification.objects.get(invest=investor)
    except Qualification.DoesNotExist:
        temp = Qualification(invest=investor)
        temp.save()
        qualificat = Qualification.objects.get(invest=investor)
    except Investor.DoesNotExist:
        return JsonResponse({'Инвестор':'Инвестора с такими паспортными данными не существует'})

    if request.method == "GET":
        dicti = {}
        serializer = QualificationSerializer(qualificat)
        if serializer.data['qualification'] == True:
            dicti['Квалификация'] = 'Вы квалифицированны'
        else:
            dicti['Квалификация'] = 'Вы не квалифицированны'
        return JsonResponse(dicti)

#Загрузка пастортных данных
@api_view(['POST', ])
def download_passport(request):
    if request.method == "POST":
        serializer = InvestorSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            investor = serializer.save()
            data['surname'] = investor.surname
            data['name'] = investor.name
            data['number_of_passport'] = investor.number_of_passport
        else:
            data = serializer.errors
        return Response(data)


#Загрузка документа паспорта
@api_view(['PUT', ])
def download_file_passport(request, pas):
    try:
        investor = Investor.objects.get(number_of_passport=pas)
    except Investor.DoesNotExist:
        return JsonResponse({'Инвестор':'Инвестора с такими паспортными данными не существует'})

    if request.method == "PUT":
        serializer = InvestorFilesSerializer(investor, data=request.FILES)
        if serializer.is_valid():
            serializer.save()
        return Response("Файл успешно загружен")
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


#Подтверждение присоединения к правилам
@api_view(['PUT', ])
def rule_accept(request, pas):
    try:
        investor = Investor.objects.get(number_of_passport=pas)
        rule = Rules.objects.get(invest=investor)
    except Rules.DoesNotExist:
        temp = Rules(invest=investor)
        temp.save()
        rule = Rules.objects.get(invest=investor)
    except Investor.DoesNotExist:
        return JsonResponse({'Инвестор':'Инвестора с такими паспортными данными не существует'})

    if request.method == "PUT":
        serializer = RulesSerializer(rule, data=request.data)
        if serializer.is_valid():
            serializer.save()
        if (rule.rule_1 and rule.rule_2 and rule.rule_3) == 0:
            return Response("Вы не подтвердили присоединение к правилам")
        else:
            return Response("Вы подтвердили присоединение к правилам можете подтверждать свою квалификацию")

#Загрузка документа квалификации
@api_view(['POST', ])
def download_file_qualification(request, pas):
    try:
        investor = Investor.objects.get(number_of_passport=pas)
        qualificat = Qualification.objects.get(invest=investor)
    except Qualification.DoesNotExist:
        temp = Qualification(invest=investor)
        temp.save()
        qualificat = Qualification.objects.get(invest=investor)
    except Investor.DoesNotExist:
        return JsonResponse({'Инвестор':'Инвестора с такими паспортными данными не существует'})

    if request.method == "POST":
        serializer = QualificationFileSerializer(qualificat, data=request.FILES)
        if serializer.is_valid():
            serializer.save()
        return Response("Файл успешно загружен")
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#Подтверждение квалификации
@api_view(['PUT', ])
def qualification_permission(request, pas):
    try:
        investor = Investor.objects.get(number_of_passport=pas)
        qualificat = Qualification.objects.get(invest=investor)
        rule = Rules.objects.get(invest=investor)
    except Qualification.DoesNotExist:
        temp = Qualification(invest=investor)
        temp.save()
        qualificat = Qualification.objects.get(invest=investor)
    except Rules.DoesNotExist:
        temp = Rules(invest=investor)
        temp.save()
        rule = Rules.objects.get(invest=investor)
    except Investor.DoesNotExist:
        return JsonResponse({'Инвестор':'Инвестора с такими паспортными данными не существует'})

    if request.method == "PUT":
        if investor.file_of_pass == None:
            return Response("Вы не загрузили файл паспорта")
        if (rule.rule_1 and rule.rule_2 and rule.rule_3) == 0:
            return Response("Вы не подтвердили присоединение к правилам")
        if qualificat.qualification_file == None:
            return Response("Вы не загрузили файл паспорта")
        serializer = QualificationSerializer(qualificat, data=request.data)
        if serializer.is_valid():
            serializer.save()
        if request.data['qualification'] == False:
            return Response("Отказ в квалификации")
        else:
            return Response("Вы подтвердили квалификацию")
# Create your views here.
