from rest_framework import viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from metadata_store.utils import str_to_bool, cache_response
from metadata_store.models import Location, Department, Category, SubCategory, Product
from metadata_store.serializers import (LocationSerializer, DepartmentSerializer, DepartmentDetailSerializer,
                                        CategorySerializer, CategoryDetailSerializer,
                                        SubCategorySerializer, SubCategoryDetailSerializer,
                                        ProductSerializer, ProductDetailSerializer)


class LocationViewSet(viewsets.ModelViewSet):
    """
    ViewSet for the Location model.

    Provides CRUD operations for Location.

    Attributes:
        queryset (QuerySet): The queryset to retrieve all locations, ordered by creation date.
        serializer_class (Serializer): The serializer class used for this ViewSet.
        permission_classes (list): The list of permissions required for this ViewSet.
    """
    queryset = Location.objects.all().order_by('-created_at')
    serializer_class = LocationSerializer
    permission_classes = [IsAuthenticated]


class DepartmentViewSet(viewsets.ModelViewSet):
    """
    ViewSet for the Department model.

    Provides CRUD operations for Department within a specific Location.

    Attributes:
        serializer_class (Serializer): The serializer class used for this ViewSet.
        permission_classes (list): The list of permissions required for this ViewSet.
    """
    serializer_class = DepartmentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Retrieves the queryset of departments filtered by location.

        Returns:
            QuerySet: The filtered queryset of departments.
        """
        location_id = self.kwargs['location_pk']
        return Department.objects.filter(location_id=location_id).order_by('-created_at')

    def get_serializer_class(self):
        """
        Determines the serializer class to use based on the request method and query parameters.

        Returns:
            Serializer: The serializer class to use.
        """
        if self.request.method == 'GET' and str_to_bool(self.request.query_params.get("detail", "false")):
            return DepartmentDetailSerializer
        return DepartmentSerializer

    def get_serializer_context(self):
        """
        Provides additional context to the serializer.

        Returns:
            dict: The context dictionary.
        """
        context = super().get_serializer_context()
        context['location_pk'] = self.kwargs['location_pk']
        return context


class CategoryViewSet(viewsets.ModelViewSet):
    """
    ViewSet for the Category model.

    Provides CRUD operations for Category within a specific Department.

    Attributes:
        serializer_class (Serializer): The serializer class used for this ViewSet.
        permission_classes (list): The list of permissions required for this ViewSet.
    """
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Retrieves the queryset of categories filtered by department and location.

        Returns:
            QuerySet: The filtered queryset of categories.
        """
        department_id = self.kwargs['department_pk']
        location_id = self.kwargs['location_pk']
        try:
            department = Department.objects.get(id=department_id, location_id=location_id)
        except Department.DoesNotExist:
            raise ValidationError("The specified department doesn't belong to the location")
        return Category.objects.filter(department_id=department_id).order_by('-created_at')

    def get_serializer_class(self):
        """
        Determines the serializer class to use based on the request method and query parameters.

        Returns:
            Serializer: The serializer class to use.
        """
        if self.request.method == 'GET' and str_to_bool(self.request.query_params.get("detail", "false")):
            return CategoryDetailSerializer
        return CategorySerializer

    def get_serializer_context(self):
        """
        Provides additional context to the serializer.

        Returns:
            dict: The context dictionary.
        """
        context = super().get_serializer_context()
        context['location_pk'] = self.kwargs['location_pk']
        context['department_pk'] = self.kwargs['department_pk']
        return context


class SubCategoryViewSet(viewsets.ModelViewSet):
    """
    ViewSet for the SubCategory model.

    Provides CRUD operations for SubCategory within a specific Category.

    Attributes:
        serializer_class (Serializer): The serializer class used for this ViewSet.
        permission_classes (list): The list of permissions required for this ViewSet.
    """
    serializer_class = SubCategorySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Retrieves the queryset of subcategories filtered by category, department, and location.

        Returns:
            QuerySet: The filtered queryset of subcategories.
        """
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
        """
        Determines the serializer class to use based on the request method and query parameters.

        Returns:
            Serializer: The serializer class to use.
        """
        if self.request.method == 'GET' and str_to_bool(self.request.query_params.get("detail", "false")):
            return SubCategoryDetailSerializer
        return SubCategorySerializer

    def get_serializer_context(self):
        """
        Provides additional context to the serializer.

        Returns:
            dict: The context dictionary.
        """
        context = super().get_serializer_context()
        context['category_pk'] = self.kwargs['category_pk']
        context['department_pk'] = self.kwargs['department_pk']
        context['location_pk'] = self.kwargs['location_pk']
        return context


class ProductViewSet(viewsets.ModelViewSet):
    """
    ViewSet for the Product model.

    Provides CRUD operations for Product.

    Attributes:
        serializer_class (Serializer): The serializer class used for this ViewSet.
        permission_classes (list): The list of permissions required for this ViewSet.
    """
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Retrieves the queryset of products, filtered by optional query parameters.

        Returns:
            QuerySet: The filtered queryset of products.
        """
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
        """
        Determines the serializer class to use based on the request method and query parameters.

        Returns:
            Serializer: The serializer class to use.
        """
        if self.request.method == 'GET' and str_to_bool(self.request.query_params.get("detail", "false")):
            return ProductDetailSerializer
        return ProductSerializer

    @cache_response('product_list')
    def list(self, request, *args, **kwargs):
        """
        Overrides the list method to cache the response.

        Args:
            request (Request): The HTTP request.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.

        Returns:
            Response: The HTTP response.
        """
        return super().list(request, *args, **kwargs)

    @cache_response('product_retrieve')
    def retrieve(self, request, *args, **kwargs):
        """
        Overrides the retrieve method to cache the response.

        Args:
            request (Request): The HTTP request.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.

        Returns:
            Response: The HTTP response.
        """
        return super().retrieve(request, *args, **kwargs)
