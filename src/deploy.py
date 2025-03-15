import sagemaker
from sagemaker.huggingface import HuggingFaceModel
import boto3
import json
import time
from dotenv import load_dotenv
import os

# import environment varialbes
load_dotenv()

AWS_ACESS_KEY_ID = os.getenv('AWS_ACESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
ROLE_ARN = os.getenv('ROLE_ARN')

# Configuration
AWS_REGION = 'us-east-1'  # Your AWS region
ROLE_ARN = ROLE_ARN  # Your role ARN
MODEL_ID = 'OriolPalacios/DeepSeek-R1-Clarity-AI-Agent'  # Your model with LoRA adapter
BASE_MODEL_ID = 'unsloth/DeepSeek-R1-Distill-Llama-8B'  # Base model your adapter was trained on
ENDPOINT_NAME = 'deepseek-r1-clarity-ai-agent-llm-endpoint'
INSTANCE_TYPE = 'ml.g5.xlarge'  # Instance type
HF_TOKEN = None  # Your HF token if using gated models

# Initialize SageMaker session
boto_session = boto3.Session(
    aws_access_key_id=AWS_ACESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name=AWS_REGION
)
sagemaker_session = sagemaker.Session(boto_session=boto_session)

# Configure the Hugging Face model
model_config = {
    'model_data': None,
    'role': ROLE_ARN,
    'transformers_version': '4.28.1',
    'pytorch_version': '2.0.1',
    'py_version': 'py310',
    'model_id': MODEL_ID,
    'model_kwargs': {
        'temperature': 0.7,
        'max_length': 512,
        'quantize': 'int8'  # For better performance
    }
}

# Add HF token if provided
if HF_TOKEN:
    model_config['huggingface_hub_token'] = HF_TOKEN

# Create the Hugging Face model
huggingface_model = HuggingFaceModel(**model_config)

# Deploy the model to a SageMaker endpoint
print(f"Deploying model {MODEL_ID} to endpoint {ENDPOINT_NAME}...")
print(f"This may take 10-15 minutes...")

start_time = time.time()
predictor = huggingface_model.deploy(
    initial_instance_count=1,
    instance_type=INSTANCE_TYPE,
    endpoint_name=ENDPOINT_NAME
)
deployment_time = time.time() - start_time

print(f"Model deployed to endpoint: {ENDPOINT_NAME}")
print(f"Deployment completed in {deployment_time/60:.2f} minutes")

# Test the endpoint with a sample prompt
test_payload = {
    "inputs": "What is machine learning?",
    "parameters": {
        "max_new_tokens": 100,
        "temperature": 0.7
    }
}

print("\nTesting the endpoint with a sample prompt...")
response = predictor.predict(test_payload)
print("\nSample response:")
print(json.dumps(response, indent=2))

print("\nEndpoint is ready for use!")
print(f"Endpoint name: {ENDPOINT_NAME}")
print(f"Region: {AWS_REGION}")