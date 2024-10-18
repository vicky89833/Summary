# api/serializers.py
from rest_framework import serializers

class FileUploadSerializer(serializers.Serializer):
    file = serializers.FileField()

    class Meta:
        fields = ['file']
        
    def validate_file(self, value):
        """
        Check if the uploaded file is either an Excel or CSV file.
        """
        # Get the file name and extension
        file_name = value.name
        file_extension = file_name.split('.')[-1].lower()

        # Allowed file extensions for Excel and CSV
        allowed_extensions = ['csv', 'xls', 'xlsx']

        # Check if the file extension is in the allowed list
        if file_extension not in allowed_extensions:
            raise serializers.ValidationError("Only CSV, XLS, or XLSX files are allowed.")
        
        return value    
