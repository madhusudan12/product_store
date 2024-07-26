import csv
from django.core.management.base import BaseCommand
from metadata_store.models import Location, Department, Category, SubCategory, Product


class Command(BaseCommand):
    help = 'Populates the database with initial data from a CSV file'

    def handle(self, *args, **kwargs):
        with open('metadata_store/data/location_metadata.csv', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                location, _ = Location.objects.get_or_create(name=row['Location'])
                department, _ = Department.objects.get_or_create(name=row['Department'], location=location)
                category, _ = Category.objects.get_or_create(name=row['Category'], department=department)
                subcategory, _ = SubCategory.objects.get_or_create(name=row['SubCategory'], category=category)
                self.stdout.write(f"Created {subcategory}")

        with open('metadata_store/data/products_data.csv', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                location, _ = Location.objects.get_or_create(name=row['LOCATION'])
                department, _ = Department.objects.get_or_create(name=row['DEPARTMENT'], location=location)
                category, _ = Category.objects.get_or_create(name=row['CATEGORY'], department=department)
                subcategory, _ = SubCategory.objects.get_or_create(name=row['SUBCATEGORY'], category=category)
                product, _ = Product.objects.get_or_create(name=row['NAME'], subcategory=subcategory)
                self.stdout.write(f"Created {product}")

        self.stdout.write(self.style.SUCCESS('Successfully populated the database'))
