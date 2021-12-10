from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from rest_framework.mixins import (
    ListModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
    CreateModelMixin
    )
from rest_framework.viewsets import GenericViewSet

from itez.beneficiary.models import (
    Agent,
    Beneficiary,
    BeneficiaryParent,
    Province,
    District,
    ServiceArea,
    WorkDetail,
    Drug,
    Lab,
    Service,
    Prescription,
    Facility,
    FacilityType,
    ImplementingPartner,
    Service,
    ServiceProviderPersonel,
    ServiceProviderPersonelQualification,
)

from itez.beneficiary.api.serializers import (
    DrugSerializer,
    LabSerializer,
    ServiceSerializer,
    PrescriptionSerializer,
    FacilitySerializer,
    FacilityTypeSerializer,
    ImplementingPartnerSerializer,
    ServiceSerializer,
    ServiceProviderPersonelSerializer,
    ServiceProviderPersonelQualificationSerializer,
    AgentSerializer,
    BeneficiarySerializer,
    BeneficiaryParentSerializer,
    ProvinceModelSerializer,
    DistrictModelSerializer,
    ServiceAreaModelSerializer,
    WorkDetailModelSerializer
)

    
class DrugAPIView(APIView):
    """
    Retrieve, update or delete a Drug instance.
    """
    def get_object(self, pk):
        try:
            return Drug.objects.get(pk=pk)
        except Drug.DoesNotExist:
            raise Http404

    def get(self, request, format=None):
        drug = Drug.objects.all()
        serializer = DrugSerializer(drug, many=True)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        drug = self.get_object(pk)
        serializer = DrugSerializer(drug, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        drug = self.get_object(pk)
        drug.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    
class LabAPIView(APIView):
    """
    Retrieve, update or delete a Lab instance.
    """
    def get_object(self, pk):
        try:
            return Lab.objects.get(pk=pk)
        except Lab.DoesNotExist:
            raise Http404

    def get(self, request, format=None):
        lab = Lab.objects.all()
        serializer = LabSerializer(lab, many=True)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        lab = self.get_object(pk)
        serializer = LabSerializer(lab, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        lab = self.get_object(pk)
        lab.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class PrescriptionAPIView(APIView):
    """
    Retrieve, update or delete a Prescription instance.
    """
    def get_object(self, pk):
        try:
            return Prescription.objects.get(pk=pk)
        except Prescription.DoesNotExist:
            raise Http404

    def get(self, request, format=None):
        prescription = Prescription.objects.all()
        serializer = PrescriptionSerializer(prescription, many=True)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        prescription = self.get_object(pk)
        serializer = PrescriptionSerializer(prescription, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        prescription = self.get_object(pk)
        prescription.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class FacilityAPIView(APIView):
    """
    Retrieve, update or delete a Facility instance.
    """
    def get_object(self, pk):
        try:
            return Facility.objects.get(pk=pk)
        except Facility.DoesNotExist:
            raise Http404

    def get(self, request, format=None):
        facility = Facility.objects.all()
        serializer = FacilitySerializer(facility, many=True)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        facility = self.get_object(pk)
        serializer = FacilitySerializer(facility, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        facility = self.get_object(pk)
        facility.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class FacilityTypeAPIView(APIView):
    """
    Retrieve, update or delete a Facility Type instance.
    """
    def get_object(self, pk):
        try:
            return FacilityType.objects.get(pk=pk)
        except FacilityType.DoesNotExist:
            raise Http404

    def get(self, request, format=None):
        facility_type = Facility.objects.all()
        serializer = FacilityTypeSerializer(facility_type, many=True)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        facility_type = self.get_object(pk)
        serializer = FacilityTypeSerializer(facility_type, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        facility_type = self.get_object(pk)
        facility_type.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class ImplementingPartnerAPIView(APIView):
    """
    Retrieve, update or delete a Implementing Partner instance.
    """
    def get_object(self, pk):
        try:
            return ImplementingPartner.objects.get(pk=pk)
        except ImplementingPartner.DoesNotExist:
            raise Http404

    def get(self, request, format=None):
        implementing_partner = ImplementingPartner.objects.all()
        serializer = ImplementingPartnerSerializer(implementing_partner, many=True)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        implementing_partner = self.get_object(pk)
        serializer = ImplementingPartnerSerializer(implementing_partner, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        implementing_partner = self.get_object(pk)
        implementing_partner.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ServiceAPIView(APIView):
    """
    Retrieve, update or delete a Service instance.
    """
    def get_object(self, pk):
        try:
            return Service.objects.get(pk=pk)
        except Service.DoesNotExist:
            raise Http404

    def get(self, request, format=None):
        service = Service.objects.all()
        serializer = ServiceSerializer(service, many=True)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        service = self.get_object(pk)
        serializer = ServiceSerializer(service, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        Service = self.get_object(pk)
        Service.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ServiceProviderPersonelAPIView(APIView):
    """
    Retrieve, update or delete a Service Provider Personel instance.
    """
    def get_object(self, pk):
        try:
            return ServiceProviderPersonel.objects.get(pk=pk)
        except ServiceProviderPersonel.DoesNotExist:
            raise Http404

    def get(self, request, format=None):
        service_provider_personel = Service.objects.all()
        serializer = ServiceProviderPersonelSerializer(
            service_provider_personel, 
            many=True
            )
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        service_provider_personel = self.get_object(pk)
        serializer = ServiceProviderPersonelSerializer(
            service_provider_personel, 
            data=request.data
            )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        service_provider_personel = self.get_object(pk)
        service_provider_personel.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ServiceProviderPersonelQualificationAPIView(APIView):
    """
    Retrieve, update or delete a Service Provider Personel Qualification instance.
    """
    def get_object(self, pk):
        try:
            return ServiceProviderPersonelQualification.objects.get(pk=pk)
        except ServiceProviderPersonelQualification.DoesNotExist:
            raise Http404

    def get(self, request, format=None):
        service_provider_personel_qualification = Service.objects.all()
        serializer = ServiceProviderPersonelQualificationSerializer(
            service_provider_personel_qualification, 
            many=True
            )
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        service_provider_personel_qualification = self.get_object(pk)
        serializer = ServiceProviderPersonelSerializer(
            service_provider_personel_qualification, 
            data=request.data
            )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        service_provider_personel_qualification = self.get_object(pk)
        service_provider_personel_qualification.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class AgentAPIView(ListModelMixin, CreateModelMixin,
    GenericViewSet, RetrieveModelMixin, UpdateModelMixin):
    """
    API end point for Agent model list, create and update.
    """
    queryset = Agent.objects.all()
    serializer_class = AgentSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)


class BeneficiaryAPIView(ListModelMixin, CreateModelMixin,
    GenericViewSet, RetrieveModelMixin, UpdateModelMixin):
    """
    API end point for Beneficiary model list, create and update.
    """
    queryset = Beneficiary.objects.all()
    serializer_class = BeneficiarySerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)


class BeneficiaryParentAPIView(ListModelMixin, CreateModelMixin,
    GenericViewSet, RetrieveModelMixin, UpdateModelMixin):
    """
    API end point for BeneficiaryParent model list, create and update.
    """
    queryset = BeneficiaryParent.objects.all()
    serializer_class = BeneficiaryParentSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)


class ProvinceAPIView(ListModelMixin,RetrieveModelMixin,
    CreateModelMixin, UpdateModelMixin,GenericViewSet):
    """
    API end point for Province model list, create and update.
    """
    queryset = Province.objects.all()
    serializer_class = ProvinceModelSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)


class DistrictAPIView(ListModelMixin,RetrieveModelMixin,
    CreateModelMixin, UpdateModelMixin,GenericViewSet):
    """
    API end point for District model list, create and update.
    """
    queryset = District.objects.all()
    serializer_class = DistrictModelSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)


class ServiceAreaAPIView(ListModelMixin,RetrieveModelMixin,
    CreateModelMixin, UpdateModelMixin,GenericViewSet):
    """
    API end point for ServiceArea model list, create and update.
    """
    queryset = ServiceArea.objects.all()
    serializer_class = ServiceAreaModelSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)


class WorkDetailAPIView(ListModelMixin,RetrieveModelMixin,
    CreateModelMixin, UpdateModelMixin,GenericViewSet):
    """
    API end point for WorkDetail model list, create and update.
    """
    queryset = WorkDetail.objects.all()
    serializer_class = WorkDetailModelSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

