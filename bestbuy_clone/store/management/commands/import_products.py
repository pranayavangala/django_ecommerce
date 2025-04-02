import csv
import os

import boto3
import io
from django.core.management.base import BaseCommand
#from store.models import Product, Category
from django.conf import settings

from bestbuy_clone.store.models import Category, Product


#from .store.models import Product, Category


class Command(BaseCommand):
    help = "Import products from a CSV file stored in S3"

    def handle(self, *args, **kwargs):
        # Replace with your actual values
        bucket_name = 'product999'
        s3_file_key = 's3://product999/products11.csv'
        image_folder = 'product_images'

        # Connect to S3
        s3 = boto3.client('s3')

        # Read object
        obj = s3.get_object(Bucket=bucket_name, Key=s3_file_key)
        csv_data = obj['Body'].read().decode('utf-8')
        reader = csv.DictReader(io.StringIO(csv_data))

        for row in reader:
            category_id = row['category']
            try:
                category = Category.objects.get(id=category_id)
            except Category.DoesNotExist:
                self.stdout.write(self.style.WARNING(f"Category ID {category_id} not found. Skipping."))
                continue

            product_name = row['name'].lower().replace(' ', '_')
            image_filename = f"{product_name}.jpg"
            local_image_path = os.path.join(image_folder, image_filename)

            if os.path.exists(local_image_path):
                s3.upload_file(local_image_path, bucket_name, image_filename)
                image = f"https://product999.s3.amazonaws.com/flowers1/"
            else:
                image = row.get('image', '')
                self.stdout.write(self.style.WARNING(f"Image not found for {row['name']}, using original or blank."))

            Product.objects.update_or_create(
                id=row['id'],
                defaults={
                    'name': row['name'],
                    'description': row['description'],
                    'price': row['price'],
                    'image': image,
                    'category': category
                }
            )

        self.stdout.write(self.style.SUCCESS("✅ Products imported from S3 CSV!"))
