import boto3
from sagemaker import image_uris
from time import gmtime, strftime

# Specify your AWS Region
aws_region = '<aws_region>'  # Replace with your AWS region

# Create a low-level SageMaker service client
sagemaker_client = boto3.client('sagemaker', region_name=aws_region)

# SageMaker IAM role ARN
sagemaker_role = "arn:aws:iam::<account>:role/*"  # Replace <account> with your AWS account ID

# S3 bucket and model details
s3_bucket = '<your-bucket-name>'  # Replace with your S3 bucket name
bucket_prefix = 'saved_models'
model_s3_key = f"{bucket_prefix}/demo-xgboost-model.tar.gz"
model_url = f"s3://{s3_bucket}/{model_s3_key}"

# Specify an AWS container image
container = image_uris.retrieve(region=aws_region, framework='xgboost', version='0.90-1')

# Model name
model_name = '<The_name_of_the_model>'  # Replace with your model name

# Create model with environment variables for asynchronous inference
create_model_response = sagemaker_client.create_model(
    ModelName=model_name,
    ExecutionRoleArn=sagemaker_role,
    PrimaryContainer={
        'Image': container,
        'ModelDataUrl': model_url,
        'Environment': {
            'TS_MAX_REQUEST_SIZE': '100000000',
            'TS_MAX_RESPONSE_SIZE': '100000000',
            'TS_DEFAULT_RESPONSE_TIMEOUT': '1000'
        },
    }
)

print(f"Model created: {create_model_response['ModelArn']}")

# Create an endpoint config
endpoint_config_name = f"XGBoostEndpointConfig-{strftime('%Y-%m-%d-%H-%M-%S', gmtime())}"

create_endpoint_config_response = sagemaker_client.create_endpoint_config(
    EndpointConfigName=endpoint_config_name,
    ProductionVariants=[
        {
            "VariantName": "variant1",
            "ModelName": model_name, 
            "InstanceType": "ml.m5.xlarge",
            "InitialInstanceCount": 1
        }
    ],
    AsyncInferenceConfig={
        "OutputConfig": {
            "S3OutputPath": f"s3://{s3_bucket}/{bucket_prefix}/output",
            "NotificationConfig": {
                "SuccessTopic": "arn:aws:sns:aws-region:account-id:topic-name",  # Replace with your SNS topic ARN
                "ErrorTopic": "arn:aws:sns:aws-region:account-id:topic-name",  # Replace with your SNS topic ARN
            }
        },
        "ClientConfig": {
            "MaxConcurrentInvocationsPerInstance": 4
        }
    }
)

print(f"Endpoint Config created: {create_endpoint_config_response['EndpointConfigArn']}")

# Create the endpoint
endpoint_name = '<endpoint-name>'  # Replace with your endpoint name

create_endpoint_response = sagemaker_client.create_endpoint(
    EndpointName=endpoint_name, 
    EndpointConfigName=endpoint_config_name
)

print(f"Endpoint created: {create_endpoint_response['EndpointArn']}")
