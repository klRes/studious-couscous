from django import forms

class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=200)
    image = forms.FileField()
    
    pdf_file = forms.FileField()
    pdf_file.widget.attrs.update({'class': 'form-control-file'})
    image.widget.attrs.update({'class': 'form-control-file'})