from django import forms 
from .models import TextReader

class TextReaderForm(forms.ModelForm):
    class Meta:
        model = TextReader
        fields = ['file']
        
    def clean_file(self):
        uploaded_file = self.cleaned_data['file']
        if not uploaded_file.name.endswith('.txt'):
            raise forms.ValidationError('Only .txt files are allowed.')
        if uploaded_file.size > 2 * 1024 * 1024:  # 2MB limit
            raise forms.ValidationError('File size cannot exceed 2MB.')
        return uploaded_file