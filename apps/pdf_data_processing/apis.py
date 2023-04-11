
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework.decorators import authentication_classes
from rest_framework import status
from rest_framework.views import APIView
from . import services
from . import serializer as serializer_pdf
from . import models

#importar authentication_classes


from apps.users import authentication

@authentication_classes([authentication.CustomUserAuthentication])
class extract_data_pdf(APIView):
    # authentication_classes = (authentication.CustomUserAuthentication, )
    # permission_classes = (permissions.IsAuthenticated, )

    parser_classes = [MultiPartParser]

    def post(self, request, format=None):
        pdf_file = request.data.get('pdf_file')
        if not pdf_file:
            return Response({'error': 'PDF file is required.'}, status=400)
        
        #validar que el archivo es pdf y no virus con pyPDF2
        # mime_type = from_buffer(pdf_file.read(), mime=True)
        # if mime_type != 'application/pdf':
        #     return Response({'error': 'File is not a PDF.'}, status=400)
        
        #extraer datos del pdf y retornar TaxFiling
    
        try:
            tax_filing_extract = services.extract_data_from_pdf(pdf_file)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        serializer = serializer_pdf.TaxFilingSerializer(data=tax_filing_extract)
        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data
        services.instance = services.create_tax_filing(tax_filing_dc=data)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

class getDataProccess(APIView):
    # authentication_classes = (authentication.CustomUserAuthentication, )
    # permission_classes = (permissions.IsAuthenticated, )

    def get(self, request, format=None):
        #obtener todos los datos de la tabla
        data = models.TaxFiling.objects.all()
        serializer = serializer_pdf.TaxFilingSerializer(data, many=True)
        return Response(serializer.data)
