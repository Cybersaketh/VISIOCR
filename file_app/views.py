from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import FileUploadSerializer

from utilities.ocr import extract_text_from_image, extract_aadhaar_details, extract_pan_details, detect_card_type


class FileUploadView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = FileUploadSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            # Perform OCR on uploaded image
            image_path = './'+serializer.data['file']
            extracted_text = extract_text_from_image(image_path)
            # print(extracted_text)
            card_type = detect_card_type(extracted_text)
            print(card_type)

            if card_type == "aadhaar":
                print("Detected Aadhaar Card")
                details = extract_aadhaar_details(extracted_text)
            elif card_type == "pan":
                print("Detected PAN Card")
                details = extract_pan_details(extracted_text)
            else:
                details = {"Error": "Could not determine card type"}
            return Response({'message': 'File uploaded successfully', 'details': details}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)