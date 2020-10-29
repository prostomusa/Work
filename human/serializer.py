from rest_framework import serializers

from .models import *

class InvestorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Investor
        exclude = ['file_of_pass']

    def save(self):
        investor = Investor(
                name=self.validated_data['name'],
                surname=self.validated_data['surname'],
                patronymic=self.validated_data['patronymic'],
                number_of_passport=self.validated_data['number_of_passport'],
                birthday=self.validated_data['birthday'],
                place_of_birth=self.validated_data['place_of_birth'],
                date_of_passport=self.validated_data['date_of_passport'],
                code=self.validated_data['code'],
                issued_by=self.validated_data['issued_by'],
                place_of_living=self.validated_data['place_of_living'],
        )
        investor.save()
        return investor

class InvestorFilesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Investor
        fields = ['file_of_pass']

class QualificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Qualification
        fields = ['qualification']

class QualificationFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Qualification
        fields = ['qualification_file']

class RulesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rules
        exclude = ['invest']
