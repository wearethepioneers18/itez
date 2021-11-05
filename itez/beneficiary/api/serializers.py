from rest_framework import serializers
from itez.beneficiary.models import (
    Province,
    District,
    ServiceArea,
    WorkDetail
)

class ProvinceModelSerializer(serializers.ModelSerializer):
    """
    Province Serializer.
    """
    class Meta:
        model = Province
        fields = '__all__'


class DistrictModelSerializer(serializers.ModelSerializer):
    """
    District Serializer.
    """
    class Meta:
        model = District
        fields = '__all__'


class ServiceAreaModelSerializer(serializers.ModelSerializer):
    """
    Service Area Serializer.
    """
    class Meta:
        model = ServiceArea
        fields = '__all__'



class WorkDetailModelSerializer(serializers.ModelSerializer):
    """
    Work Detail Serializer.
    """
    class Meta:
        model = WorkDetail
        fields = '__all__'
        

