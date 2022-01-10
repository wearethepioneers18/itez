from rest_framework import serializers

from itez.beneficiary.models import (
    Agent,
    Beneficiary,
    BeneficiaryParent,
    Province,
    District,
    ServiceArea,
    WorkDetail,
    Drug,
    Service,
    Facility,
    FacilityType,
    ImplementingPartner,
    Service,
    ServiceProviderPersonel,
    ServiceProviderPersonelQualification,
)


class DrugSerializer(serializers.ModelSerializer):
    """
    Drug serializer.
    """

    class Meta:
        model = Drug
        fields = "__all__"

class ServiceSerializer(serializers.ModelSerializer):
    """
    Service serializer.
    """

    class Meta:
        model = Service
        fields = "__all__"

class FacilityTypeSerializer(serializers.ModelSerializer):
    """
    FacilityType serializer.
    """

    class Meta:
        model = FacilityType
        fields = "__all__"


class FacilitySerializer(serializers.ModelSerializer):
    """
    Facility serializer.
    """

    class Meta:
        model = Facility
        fields = "__all__"


class ImplementingPartnerSerializer(serializers.ModelSerializer):
    """
    ImplementingPartner serializer.
    """

    class Meta:
        model = ImplementingPartner
        fields = "__all__"


class ServiceProviderPersonelSerializer(serializers.ModelSerializer):
    """
    ServiceProviderPersonel serializer.
    """

    class Meta:
        model = ServiceProviderPersonel
        fields = "__all__"


class ServiceProviderPersonelQualificationSerializer(serializers.ModelSerializer):
    """
    ServiceProvider Personel Qualification's serializer.
    """

    class Meta:
        model = ServiceProviderPersonelQualification
        fields = "__all__"


class AgentSerializer(serializers.ModelSerializer):
    """
    Agent serializer.
    """

    class Meta:
        model = Agent
        fields = "__all__"


class BeneficiarySerializer(serializers.ModelSerializer):
    """
    Beneficiary serializer.
    """

    class Meta:
        model = Beneficiary
        fields = "__all__"


class BeneficiaryParentSerializer(serializers.ModelSerializer):
    """
    BeneficiaryParent serializer.
    """

    class Meta:
        model = BeneficiaryParent
        fields = "__all__"


class ProvinceModelSerializer(serializers.ModelSerializer):
    """
    Province Serializer.
    """

    class Meta:
        model = Province
        fields = "__all__"


class DistrictModelSerializer(serializers.ModelSerializer):
    """
    District Serializer.
    """

    class Meta:
        model = District
        fields = "__all__"


class ServiceAreaModelSerializer(serializers.ModelSerializer):
    """
    Service Area Serializer.
    """

    class Meta:
        model = ServiceArea
        fields = "__all__"


class WorkDetailModelSerializer(serializers.ModelSerializer):
    """
    Work Detail Serializer.
    """

    class Meta:
        model = WorkDetail
        fields = "__all__"
        depth = 2
