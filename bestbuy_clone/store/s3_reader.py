# store/s3_reader.py

import boto3
from django.conf import settings

# store/s3_reader.py
import boto3
from django.conf import settings

def fetch_products_from_s3(prefix='flowers1/'):
    s3 = boto3.client(
        's3',
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        region_name=settings.AWS_REGION
    )

    # Predefined product metadata (name, description, price)
    product_metadata = {
        "0001.png": {
            "name": "fortuneflower",
            "description": "Fragrant white flowers",
            "price": 699.99
        },
        "0002.png": {
            "name": "Orchid ",
            "description": "Romantic red roses",
            "price": 799.99
        },
        "0003.png": {
            "name": "Lily",
            "description": "Elegant white lilies",
            "price": 850.00
        },
            "0004.png": {
                "name": "marrigold",
                "description": "Fragrant white flowers",
                "price": 699.99
            },
            "0005.png": {
                "name": "lotus",
                "description": "Romantic red roses",
                "price": 799.99
            },
            "0006.png": {
                "name": "Rose",
                "description": "Elegant white lilies",
                "price": 850.00
            },

            "0007.png": {
                "name": "randomflower",
                "description": "Fragrant white flowers",
                "price": 699.99
            },
            "0008.png": {
                "name": "sunflower",
                "description": "Romantic red roses",
                "price": 799.99
            },
            "0009.png": {
                "name": "happyflower",
                "description": "Elegant white lilies",
                "price": 850.00
            },
            "00010.png": {
                "name": "fortuneflower",
                "description": "Fragrant white flowers",
                "price": 699.99
            },
            "00011.png": {
                "name": "Dahlia",
                "description": "Romantic red roses",
                "price": 799.99
            },
            "00012.png": {
                "name": "Lavender",
                "description": "Elegant white lilies",
                "price": 850.00
            },
        # Add more mappings as needed...
    }

    response = s3.list_objects_v2(
        Bucket=settings.AWS_S3_BUCKET_NAME,
        Prefix=prefix
    )

    products = []

    for obj in response.get('Contents', []):
        key = obj['Key']
        filename = key.split('/')[-1]

        if not key.endswith('/') and filename in product_metadata:
            url = f"https://{settings.AWS_S3_BUCKET_NAME}.s3.{settings.AWS_REGION}.amazonaws.com/{key}"
            meta = product_metadata[filename]

            products.append({
                "name": meta["name"],
                "description": meta["description"],
                "price": meta["price"],
                "image_url": url
            })

    return products

