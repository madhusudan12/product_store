
import uuid
from django.db import models


class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Location(BaseModel):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class Department(BaseModel):
    name = models.CharField(max_length=255)
    location = models.ForeignKey(Location, related_name='departments', on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['location', 'name'], name='unique_location_department_name')
        ]

    def __str__(self):
        return f"{self.location.name}>{self.name}"


class Category(BaseModel):
    name = models.CharField(max_length=255)
    department = models.ForeignKey(Department, related_name='categories', on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['department', 'name'], name='unique_department_category__name')
        ]

    def __str__(self):
        return f"{self.department.location.name}>{self.department.name}>{self.name}"


class SubCategory(BaseModel):
    name = models.CharField(max_length=255)
    category = models.ForeignKey(Category, related_name='subcategories', on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['category', 'name'], name='unique_category_subcategory__name')
        ]

    def __str__(self):
        return f"{self.category.department.location.name}>{self.category.department.name}>{self.category.name}>{self.name}"


class Product(BaseModel):
    name = models.CharField(max_length=255)
    subcategory = models.ForeignKey(SubCategory, related_name='products', on_delete=models.CASCADE)

    # TODO: do (subcategory,name) fields need to be unique together?

    def __str__(self):
        return self.name
