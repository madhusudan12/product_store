import csv
from django.core.management.base import BaseCommand
from metadata_store.models import Location, Department, Category, SubCategory, Product

class Command(BaseCommand):
    """
    Custom Django management command to populate the database with initial data from CSV files.
    """
    help = 'Populates the database with initial data from a CSV file'

    def handle(self, *args, **kwargs):
        """
        Handles the command execution.

        Reads data from CSV files and populates the database with Location, Department,
        Category, SubCategory, and Product instances.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.
        """
        self.populate_locations_and_departments()
        self.populate_products()
        self.stdout.write(self.style.SUCCESS('Successfully populated the database'))

    def populate_locations_and_departments(self):
        """
        Populates the database with Location, Department, Category, and SubCategory instances
        from the 'location_metadata.csv' file.
        """
        with open('metadata_store/data/location_metadata.csv', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                location, _ = Location.objects.get_or_create(name=row['Location'])
                department, _ = Department.objects.get_or_create(name=row['Department'], location=location)
                category, _ = Category.objects.get_or_create(name=row['Category'], department=department)
                subcategory, _ = SubCategory.objects.get_or_create(name=row['SubCategory'], category=category)
                self.stdout.write(f"Created {subcategory}")

    def populate_products(self):
        """
        Populates the database with Product instances from the 'products_data.csv' file.
        """
        with open('metadata_store/data/products_data.csv', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                location, _ = Location.objects.get_or_create(name=row['LOCATION'])
                department, _ = Department.objects.get_or_create(name=row['DEPARTMENT'], location=location)
                category, _ = Category.objects.get_or_create(name=row['CATEGORY'], department=department)
                subcategory, _ = SubCategory.objects.get_or_create(name=row['SUBCATEGORY'], category=category)
                product, _ = Product.objects.get_or_create(name=row['NAME'], subcategory=subcategory)
                self.stdout.write(f"Created {product}")
