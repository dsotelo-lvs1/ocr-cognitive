import os
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
from msrest.authentication import CognitiveServicesCredentials
import time

# Set up the service key and endpoint
subscription_key = "CONGNITIVE_SERVICES_KEY"
endpoint = "COGNITIVE_SERVICES_URL"

# Authenticate the client
computervision_client = ComputerVisionClient(
    endpoint, CognitiveServicesCredentials(subscription_key)
)

# Function to perform OCR on an image
def perform_ocr(image_path):
    with open(image_path, "rb") as image_stream:
        ocr_result = computervision_client.read_in_stream(image_stream, raw=True)
        operation_location = ocr_result.headers["Operation-Location"]
        operation_id = operation_location.split("/")[-1]

        # Wait for the operation to complete
        while True:
            result = computervision_client.get_read_result(operation_id)
            if result.status not in ['notStarted', 'running']:
                break
            time.sleep(1)

        # Print the OCR results
        if result.status == OperationStatusCodes.succeeded:
            for page in result.analyze_result.read_results:
                for line in page.lines:
                    print(line.text)
        else:
            print("OCR failed.")

# Function to perform OCR on a PDF
def perform_ocr_on_pdf(pdf_path):
    with open(pdf_path, "rb") as pdf_stream:
        ocr_result = computervision_client.read_in_stream(pdf_stream, raw=True)
        operation_location = ocr_result.headers["Operation-Location"]
        operation_id = operation_location.split("/")[-1]

        # Wait for the operation to complete
        while True:
            result = computervision_client.get_read_result(operation_id)
            if result.status not in ['notStarted', 'running']:
                break
            time.sleep(1)

        # Print the OCR results
        if result.status == OperationStatusCodes.succeeded:
            for page in result.analyze_result.read_results:
                for line in page.lines:
                    print(line.text)
        else:
            print("OCR failed.")


# Path to the image file
#image_path = "sample.jpg"

# Perform OCR on the image
# perform_ocr(image_path)

# Perform OCR on the PDF
perform_ocr("Fabric.pdf")
