from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_nested.routers import NestedSimpleRouter
from metadata_store.views import LocationViewSet, DepartmentViewSet, CategoryViewSet, SubCategoryViewSet, ProductViewSet


router = DefaultRouter()
router.register(r'locations', LocationViewSet)
router.register(r'products', ProductViewSet, basename="products")


locations_router = NestedSimpleRouter(router, r'locations', lookup='location')
locations_router.register(r'departments', DepartmentViewSet, basename='location-departments')

departments_router = NestedSimpleRouter(locations_router, r'departments', lookup='department')
departments_router.register(r'categories', CategoryViewSet, basename='department-categories')

categories_router = NestedSimpleRouter(departments_router, r'categories', lookup='category')
categories_router.register(r'subcategories', SubCategoryViewSet, basename='category-subcategories')


urlpatterns = [
    path('', include(router.urls)),
    path('', include(locations_router.urls)),
    path('', include(departments_router.urls)),
    path('', include(categories_router.urls)),
]
