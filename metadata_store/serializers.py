from rest_framework import serializers
from .models import Location, Department, Category, SubCategory, Product


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = "__all__"


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = "__all__"

    def to_internal_value(self, data):
        location_id = self.context['location_pk']
        data["location"] = location_id
        return super().to_internal_value(data)


class DepartmentDetailSerializer(DepartmentSerializer):
    location = LocationSerializer()

    class Meta(DepartmentSerializer.Meta):
        fields = "__all__"


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"

    def to_internal_value(self, data):
        department_id = self.context['department_pk']
        data["department"] = department_id
        return super().to_internal_value(data)

    def validate(self, validated_data):
        location_id = self.context['location_pk']
        department_id = self.context['department_pk']
        try:
            department = Department.objects.get(id=department_id, location_id=location_id)
        except Department.DoesNotExist:
            raise serializers.ValidationError("The specified location does not exist.")
        return validated_data


class CategoryDetailSerializer(CategorySerializer):
    department = DepartmentDetailSerializer()

    class Meta(CategorySerializer.Meta):
        fields = "__all__"


class SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = "__all__"

    def to_internal_value(self, data):
        category_id = self.context['category_pk']
        data["category"] = category_id
        return super().to_internal_value(data)

    def validate(self, validated_data):
        category_id = self.context['category_pk']
        department_id = self.context['department_pk']
        location_id = self.context['location_pk']

        try:
            category = Category.objects.get(id=category_id, department_id=department_id)
            department = Department.objects.get(id=department_id, location_id=location_id)
        except Category.DoesNotExist:
            raise serializers.ValidationError("The specified category does not belong to the given department.")
        except Department.DoesNotExist:
            raise serializers.ValidationError("The specified department does not belong to the given location.")

        return validated_data


class SubCategoryDetailSerializer(SubCategorySerializer):
    category = CategoryDetailSerializer()

    class Meta(SubCategorySerializer.Meta):
        fields = "__all__"


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"


class ProductDetailSerializer(ProductSerializer):
    subcategory = SubCategoryDetailSerializer()

    class Meta(ProductSerializer.Meta):
        fields = "__all__"
