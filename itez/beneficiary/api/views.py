from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.mixins import (
    ListModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
    CreateModelMixin
    )
from rest_framework.viewsets import GenericViewSet

from itez.beneficiary.models import (
    AgentDetail,
    Beneficiary,
    BeneficiaryParent,
    Province,
    District,
    ServiceArea,
    WorkDetail
)

from itez.beneficiary.api.serializers import (
    AgentDetailSerializer,
    BeneficiarySerializer,
    BeneficiaryParentSerializer,
    ProvinceModelSerializer,
    DistrictModelSerializer,
    ServiceAreaModelSerializer,
    WorkDetailModelSerializer
)


class AgentDetailAPIView(ListModelMixin, CreateModelMixin,
    GenericViewSet, RetrieveModelMixin, UpdateModelMixin):
    """
    API end point for AgentDetail model list, create and update.
    """
    queryset = AgentDetail.objects.all()
    serializer_class = AgentDetailSerializer

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