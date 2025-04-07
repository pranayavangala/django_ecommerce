import boto3
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Test AWS S3 connectivity and list files'

    def handle(self, *args, **kwargs):
        try:
           """ s3 = boto3.client(
                's3',
                aws_access_key_id='AKIAVRUVRMXJ324MOBGS',
                aws_secret_access_key='Y8xgHPvqpC1x5/NzhZ3PMYxFIt54kq2yM38ViI4b',
                region_name='us-east-1'  # ✅ Update to your actual region
            )

            bucket_name = 'product999'  # ✅ Replace with your actual bucket
            response = s3.list_objects_v2(Bucket=bucket_name)

            self.stdout.write(self.style.SUCCESS("✅ Successfully connected to AWS S3"))
            self.stdout.write("Files in bucket:")
            for obj in response.get('Contents', []):
                self.stdout.write(f"- {obj['Key']}")"""

        except Exception as e:
            self.stdout.write(self.style.ERROR(f"❌ Failed to connect to S3: {str(e)}"))