
import uuid
from django.db import models


class BaseModel(models.Model):
    """
    Abstract base model providing common fields for other models.

    Fields:
        id (UUIDField): Primary key, generated automatically.
        created_at (DateTimeField): The date and time when the object was created.
        updated_at (DateTimeField): The date and time when the object was last updated.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Location(BaseModel):
    """
    Model representing location information.

    Fields:
        name (CharField): The name of the location.
    """
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class Department(BaseModel):
    """
    Model representing a department within a location.

    Fields:
        name (CharField): The name of the department.
        location (ForeignKey): The location to which the department belongs.

    Meta:
        constraints (list): Ensures that each department name is unique within a location.
    """
    name = models.CharField(max_length=255)
    location = models.ForeignKey(Location, related_name='departments', on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['location', 'name'], name='unique_location_department_name')
        ]

    def __str__(self):
        return f"{self.location.name}>{self.name}"


class Category(BaseModel):
    """
    Model representing a category within a department.

    Fields:
        name (CharField): The name of the category.
        department (ForeignKey): The department to which the category belongs.

    Meta:
        constraints (list): Ensures that each category name is unique within a department.
    """
    name = models.CharField(max_length=255)
    department = models.ForeignKey(Department, related_name='categories', on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['department', 'name'], name='unique_department_category__name')
        ]

    def __str__(self):
        return f"{self.department.location.name}>{self.department.name}>{self.name}"


class SubCategory(BaseModel):
    """
    Model representing a subcategory within a category.

    Fields:
        name (CharField): The name of the subcategory.
        category (ForeignKey): The category to which the subcategory belongs.

    Meta:
        constraints (list): Ensures that each subcategory name is unique within a category.
    """
    name = models.CharField(max_length=255)
    category = models.ForeignKey(Category, related_name='subcategories', on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['category', 'name'], name='unique_category_subcategory__name')
        ]

    def __str__(self):
        return f"{self.category.department.location.name}>{self.category.department.name}>{self.category.name}>{self.name}"


class Product(BaseModel):
    """
    Model representing a product within a subcategory.

    Fields:
        name (CharField): The name of the product.
        subcategory (ForeignKey): The subcategory to which the product belongs.
    """
    name = models.CharField(max_length=255)
    subcategory = models.ForeignKey(SubCategory, related_name='products', on_delete=models.CASCADE)

    # TODO: do (subcategory,name) fields need to be unique together?

    # TODO: can a product be included in multiple subcategories?

    def __str__(self):
        return self.name
