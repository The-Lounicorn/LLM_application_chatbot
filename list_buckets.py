import ibm_boto3
from ibm_botocore.client import Config

# Credentials from your service key
api_key = "hD-m9XPGGvnBmvmNJA9NJ_C8B7Yl-rlWtrSp74jIyrg0"
resource_instance_id = "crn:v1:bluemix:public:cloud-object-storage:global:a/b533527cc2244930965907608f6688ae:ef2c2b96-30d3-4034-b62a-f107146ae8e5::"
endpoint_url = "https://s3.us-east.cloud-object-storage.appdomain.cloud"

# Create COS client
cos = ibm_boto3.client("s3",
    ibm_api_key_id=api_key,
    ibm_service_instance_id=resource_instance_id,
    config=Config(signature_version="oauth"),
    endpoint_url=endpoint_url
)

# List buckets
response = cos.list_buckets()
for bucket in response["Buckets"]:
    print("🪣 Bucket:", bucket["Name"])