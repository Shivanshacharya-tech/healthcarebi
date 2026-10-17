"""
VitalFlow Healthcare BI - AWS S3 Ingestion Script
Stages raw hospital operational datasets to AWS S3 data lake.

Requirements:
    pip install boto3

Configuration:
    Set AWS credentials via:
      1. AWS CLI (`aws configure`)
      2. Environment variables: AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_DEFAULT_REGION
"""

import os
import sys

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data", "raw")
DEFAULT_BUCKET = "vitalflow-healthcare-data-lake"
S3_PREFIX = "raw/healthcare/"

FILES_TO_UPLOAD = [
    "dim_date.csv",
    "dim_departments.csv",
    "dim_physicians.csv",
    "dim_patients.csv",
    "fact_ed_encounters.csv",
    "fact_inpatient_stays.csv"
]

def upload_files_to_s3(bucket_name=DEFAULT_BUCKET, region_name="us-east-1"):
    try:
        import boto3
        from botocore.exceptions import NoCredentialsError, ClientError
    except ImportError:
        print("[!] boto3 is not installed. To upload to AWS, run: pip install boto3")
        return False

    print(f"[*] Initializing AWS S3 client for region: {region_name}...")
    s3_client = boto3.client("s3", region_name=region_name)

    # Check / Create bucket if needed
    try:
        s3_client.head_bucket(Bucket=bucket_name)
        print(f"[✓] Bucket '{bucket_name}' verified.")
    except ClientError as e:
        error_code = e.response.get("Error", {}).get("Code")
        if error_code in ["404", "NoSuchBucket"]:
            print(f"[*] Bucket '{bucket_name}' not found. Attempting creation...")
            try:
                if region_name == "us-east-1":
                    s3_client.create_bucket(Bucket=bucket_name)
                else:
                    s3_client.create_bucket(
                        Bucket=bucket_name,
                        CreateBucketConfiguration={"LocationConstraint": region_name}
                    )
                print(f"[✓] Bucket '{bucket_name}' created successfully.")
            except Exception as ce:
                print(f"[!] Could not create bucket: {ce}")
                return False
        else:
            print(f"[!] Access error or credentials issue: {e}")
            return False
    except NoCredentialsError:
        print("[!] AWS credentials not found. Run 'aws configure' or set AWS_ACCESS_KEY_ID & AWS_SECRET_ACCESS_KEY.")
        return False

    # Upload files
    success_count = 0
    for filename in FILES_TO_UPLOAD:
        local_path = os.path.join(DATA_DIR, filename)
        s3_key = f"{S3_PREFIX}{filename}"

        if not os.path.exists(local_path):
            print(f"[!] Local file missing: {local_path}")
            continue

        file_size_mb = os.path.getsize(local_path) / (1024 * 1024)
        print(f"[*] Uploading {filename} ({file_size_mb:.2f} MB) -> s3://{bucket_name}/{s3_key}...")
        try:
            s3_client.upload_file(local_path, bucket_name, s3_key)
            print(f"    [✓] {filename} uploaded successfully.")
            success_count += 1
        except Exception as ue:
            print(f"    [✗] Failed to upload {filename}: {ue}")

    print(f"\n[DONE] Successfully uploaded {success_count}/{len(FILES_TO_UPLOAD)} files to AWS S3.")
    return True

if __name__ == "__main__":
    bucket = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_BUCKET
    region = sys.argv[2] if len(sys.argv) > 2 else "us-east-1"
    print(f"=== VitalFlow Healthcare AWS S3 Uploader ===")
    print(f"Target Bucket: {bucket}")
    print(f"Target Region: {region}\n")
    upload_files_to_s3(bucket, region)
