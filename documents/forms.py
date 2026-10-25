
from pathlib import Path

from django import forms


from django.contrib.auth import get_user_model

from .models import Document, DocumentPermission


class DocumentUploadForm(forms.ModelForm):
    MAX_FILE_SIZE = 10 * 1024 * 1024

    ALLOWED_EXTENSIONS = {
        ".pdf",
        ".doc",
        ".docx",
        ".png",
        ".jpg",
        ".jpeg",
    }

    class Meta:
        model = Document
        fields = [
            "title",
            "description",
            "file",
            "category",
        ]

    def clean_file(self):
        uploaded_file = self.cleaned_data.get("file")

        if not uploaded_file:
            raise forms.ValidationError("Please select a file.")

        extension = Path(uploaded_file.name).suffix.lower()

        if extension not in self.ALLOWED_EXTENSIONS:
            raise forms.ValidationError(
                "Unsupported file type. Upload a PDF, Word document, "
                "or PNG/JPG image."
            )

        if uploaded_file.size > self.MAX_FILE_SIZE:
            raise forms.ValidationError(
                "File size cannot exceed 10 MB."
            )

        return uploaded_file
    

User = get_user_model()

class DocumentPermissionForm(forms.ModelForm):
    class Meta:
        model = DocumentPermission
        fields = ["user", "permission_type"]


def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)

    self.fields["user"].queryset = User.objects.filter(
        is_active=True
    ).order_by("username")

    self.fields["user"].label = "Share with user"
    self.fields["permission_type"].label = "Permission type"
