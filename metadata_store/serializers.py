from rest_framework import serializers
from .models import Location, Department, Category, SubCategory, Product


class LocationSerializer(serializers.ModelSerializer):
    """
    Serializer for the Location model.

    Meta:
        model (Location): The model to serialize.
        fields (str): All fields of the model are included.
    """
    class Meta:
        model = Location
        fields = "__all__"


class DepartmentSerializer(serializers.ModelSerializer):
    """
    Serializer for the Department model. Automatically assigns the location
    based on the context.

    Meta:
        model (Department): The model to serialize.
        fields (str): All fields of the model are included.
    """
    class Meta:
        model = Department
        fields = "__all__"

    def to_internal_value(self, data):
        """
        Convert the input data to a native value. Assigns the location ID from
        the context to the data.

        Args:
            data (dict): The input data.

        Returns:
            dict: The validated and transformed data.
        """
        location_id = self.context['location_pk']
        data["location"] = location_id
        return super().to_internal_value(data)


class DepartmentDetailSerializer(DepartmentSerializer):
    """
    Serializer for the Department model with detailed nested location information.

    Meta:
        model (Department): The model to serialize.
        fields (str): All fields of the model are included.
    """
    location = LocationSerializer()

    class Meta(DepartmentSerializer.Meta):
        fields = "__all__"


class CategorySerializer(serializers.ModelSerializer):
    """
    Serializer for the Category model. Automatically assigns the department
    based on the context.

    Meta:
        model (Category): The model to serialize.
        fields (str): All fields of the model are included.
    """
    class Meta:
        model = Category
        fields = "__all__"

    def to_internal_value(self, data):
        """
        Convert the input data to a native value. Assigns the department ID
        from the context to the data.

        Args:
            data (dict): The input data.

        Returns:
            dict: The validated and transformed data.
        """
        department_id = self.context['department_pk']
        data["department"] = department_id
        return super().to_internal_value(data)

    def validate(self, validated_data):
        """
        Validate the input data. Checks if the department belongs to the
        given location.

        Args:
            validated_data (dict): The validated data.

        Returns:
            dict: The validated data.

        Raises:
            serializers.ValidationError: If the department does not belong to
            the given location.
        """
        location_id = self.context['location_pk']
        department_id = self.context['department_pk']
        try:
            department = Department.objects.get(id=department_id, location_id=location_id)
        except Department.DoesNotExist:
            raise serializers.ValidationError("The specified department does not belong to the given location.")
        return validated_data


class CategoryDetailSerializer(CategorySerializer):
    """
    Serializer for the Category model with detailed nested department information.

    Meta:
        model (Category): The model to serialize.
        fields (str): All fields of the model are included.
    """
    department = DepartmentDetailSerializer()

    class Meta(CategorySerializer.Meta):
        fields = "__all__"


class SubCategorySerializer(serializers.ModelSerializer):
    """
    Serializer for the SubCategory model. Automatically assigns the category
    based on the context.

    Meta:
        model (SubCategory): The model to serialize.
        fields (str): All fields of the model are included.
    """
    class Meta:
        model = SubCategory
        fields = "__all__"

    def to_internal_value(self, data):
        """
        Convert the input data to a native value. Assigns the category ID
        from the context to the data.

        Args:
            data (dict): The input data.

        Returns:
            dict: The validated and transformed data.
        """
        category_id = self.context['category_pk']
        data["category"] = category_id
        return super().to_internal_value(data)

    def validate(self, validated_data):
        """
        Validate the input data. Checks if the category belongs to the given
        department and if the department belongs to the given location.

        Args:
            validated_data (dict): The validated data.

        Returns:
            dict: The validated data.

        Raises:
            serializers.ValidationError: If the category does not belong to
            the given department or if the department does not belong to the
            given location.
        """
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
    """
    Serializer for the SubCategory model with detailed nested category information.

    Meta:
        model (SubCategory): The model to serialize.
        fields (str): All fields of the model are included.
    """
    category = CategoryDetailSerializer()

    class Meta(SubCategorySerializer.Meta):
        fields = "__all__"


class ProductSerializer(serializers.ModelSerializer):
    """
    Serializer for the Product model.

    Meta:
        model (Product): The model to serialize.
        fields (str): All fields of the model are included.
    """
    class Meta:
        model = Product
        fields = "__all__"


class ProductDetailSerializer(ProductSerializer):
    """
    Serializer for the Product model with detailed nested subcategory information.

    Meta:
        model (Product): The model to serialize.
        fields (str): All fields of the model are included.
    """
    subcategory = SubCategoryDetailSerializer()

    class Meta(ProductSerializer.Meta):
        fields = "__all__"
