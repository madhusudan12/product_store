
from django.utils.decorators import method_decorator
from django.core.cache import cache
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from metadata_store.utils import str_to_bool, cache_response
from metadata_store.models import Location, Department, Category, SubCategory, Product
from metadata_store.serializers import (LocationSerializer, DepartmentSerializer, DepartmentDetailSerializer,
                                        CategorySerializer, CategoryDetailSerializer,
                                        SubCategorySerializer, SubCategoryDetailSerializer,
                                        ProductSerializer, ProductDetailSerializer)


CACHE_TTL = 60 * 15


class LocationViewSet(viewsets.ModelViewSet):
    queryset = Location.objects.all().order_by('-created_at')
    serializer_class = LocationSerializer
    permission_classes = [IsAuthenticated]


class DepartmentViewSet(viewsets.ModelViewSet):
    serializer_class = DepartmentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        location_id = self.kwargs['location_pk']
        return Department.objects.filter(location_id=location_id).order_by('-created_at')

    def get_serializer_class(self):
        if self.request.method == 'GET' and str_to_bool(self.request.query_params.get("detail", "false")):
            return DepartmentDetailSerializer
        return DepartmentSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['location_pk'] = self.kwargs['location_pk']
        return context


class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        department_id = self.kwargs['department_pk']
        location_id = self.kwargs['location_pk']
        try:
            department = Department.objects.get(id=department_id, location_id=location_id)
        except Department.DoesNotExist:
            raise ValidationError("The specified department doesn't belong to the location")
        return Category.objects.filter(department_id=department_id).order_by('-created_at')

    def get_serializer_class(self):
        if self.request.method == 'GET' and str_to_bool(self.request.query_params.get("detail", "false")):
            return CategoryDetailSerializer
        return CategorySerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['location_pk'] = self.kwargs['location_pk']
        context['department_pk'] = self.kwargs['department_pk']
        return context


class SubCategoryViewSet(viewsets.ModelViewSet):
    serializer_class = SubCategorySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        category_id = self.kwargs['category_pk']
        department_id = self.kwargs['department_pk']
        location_id = self.kwargs['location_pk']
        try:
            category = Category.objects.get(id=category_id, department_id=department_id)
            department = Department.objects.get(id=department_id, location_id=location_id)
        except Category.DoesNotExist:
            raise ValidationError("The specified category does not belong to the given department.")
        except Department.DoesNotExist:
            raise ValidationError("The specified department does not belong to the given location.")
        return SubCategory.objects.filter(category_id=category_id).order_by('-created_at')

    def get_serializer_class(self):
        if self.request.method == 'GET' and str_to_bool(self.request.query_params.get("detail", "false")):
            return SubCategoryDetailSerializer
        return SubCategorySerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['category_pk'] = self.kwargs['category_pk']
        context['department_pk'] = self.kwargs['department_pk']
        context['location_pk'] = self.kwargs['location_pk']
        return context


class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Product.objects.all().order_by('-created_at')
        location_name = self.request.query_params.get('location_name')
        department_name = self.request.query_params.get('department_name')
        category_name = self.request.query_params.get('category_name')
        subcategory_name = self.request.query_params.get('subcategory_name')

        if location_name:
            queryset = queryset.filter(
                subcategory__category__department__location__name=location_name
            )
        if department_name:
            queryset = queryset.filter(
                subcategory__category__department__name=department_name
            )
        if category_name:
            queryset = queryset.filter(
                subcategory__category__name=category_name
            )
        if subcategory_name:
            queryset = queryset.filter(
                subcategory__name=subcategory_name
            )

        return queryset

    def get_serializer_class(self):
        if self.request.method == 'GET' and str_to_bool(self.request.query_params.get("detail", "false")):
            return ProductDetailSerializer
        return ProductSerializer

    @cache_response('product_list')
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @cache_response('product_retrieve')
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

