import pandas as pd
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.mail import EmailMessage
from django.conf import settings
import os
from .serializers import FileUploadSerializer
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from io import StringIO
from django.shortcuts import render

def indexView(request):
    return render(request, 'index.html')
    

class FileUploadView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = FileUploadSerializer(data=request.data)
        if serializer.is_valid():
            
            uploaded_file = request.FILES['file']
            file_path = default_storage.save(uploaded_file.name, ContentFile(uploaded_file.read()))

            
            try:
                processed_data, csv_file_content, statistics = self.process_file(file_path)
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

            
            self.send_csv_via_email(csv_file_content, statistics)

            
            default_storage.delete(file_path)
            
            response_data = {
                "statistics": statistics,
                "processed_data": processed_data
                
            }
            print(processed_data)
            print("response is sent")
            return Response(response_data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def process_file(self, file_path):
        
        
        _, file_extension = os.path.splitext(file_path)

        if file_extension == '.csv':
            df = pd.read_csv(file_path)
        elif file_extension in ['.xls', '.xlsx']:
            df = pd.read_excel(file_path)
        else:
            raise ValueError("Unsupported file format. Please upload an Excel or CSV file.")

        
        required_columns = ['Cust State', 'Cust Pin', 'DPD']
        if not all(column in df.columns for column in required_columns):
            raise ValueError("The file is missing required columns: Cust State, Cust Pin, or DPD.")

        df = df.drop(['Date', 'ACCNO'], axis=1)
        df = df.sort_values(by=['Cust State', 'DPD'], ascending=[True, True])
        num_rows = len(df)
        mean_dpd = df['DPD'].mean()
        min_dpd = df['DPD'].min()
        max_dpd = df['DPD'].max()
        variance_dpd = df['DPD'].var()
        std_dev_dpd = df['DPD'].std()
        # Create a statistics dictionary to return and use in email
        statistics = {
            "num_rows": num_rows,
            "mean_dpd": mean_dpd,
            "min_dpd": min_dpd,
            "max_dpd": max_dpd,
            "variance_dpd": variance_dpd,
            "std_dev_dpd": std_dev_dpd
        }
        
        
        
        # Convert DataFrame to a CSV format for the email attachment
        csv_buffer = StringIO()
        df.to_csv(csv_buffer, index=False)
        csv_content = csv_buffer.getvalue()

        # Convert DataFrame to a dictionary for the response
        response_data = df.to_dict(orient='records')

        return response_data, csv_content,  statistics

    def send_csv_via_email(self, csv_content, statistics, recipient_email="vicky.jnv898@gmail.com"):
        """
        Sends the sorted CSV as an attachment via email.
        """
        subject = "Python Assignment - Your Name"
        email_body = (
            "Please find the processed data attached as a CSV file.\n\n"
            "Statistics for Data:\n"
            f"Number of Entries: {statistics['num_rows']}\n"
            f"Mean DPD: {statistics['mean_dpd']:.2f}\n"
            f"Min DPD: {statistics['min_dpd']}\n"
            f"Max DPD: {statistics['max_dpd']}\n"
            f"Variance of DPD: {statistics['variance_dpd']:.2f}\n"
            f"Standard Deviation of DPD: {statistics['std_dev_dpd']:.2f}\n"
        )
        email = EmailMessage(
            subject=subject,
            body=email_body,
            from_email=settings.EMAIL_HOST_USER,
            to=[recipient_email]
        )

        # Attach the CSV file to the email
        email.attach('Processed_data.csv', csv_content, 'text/csv')

        # Send the email
        email.send()
