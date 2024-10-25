from django.shortcuts import render

# Create your views here.

from django.shortcuts import render
from .forms import FileUploadForm
from django.core.files.storage import FileSystemStorage
import pandas as pd

def upload_file(request):
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = request.FILES['file']
            fs = FileSystemStorage()
            filename = fs.save(uploaded_file.name, uploaded_file)
            file_url = fs.url(filename)

            # Process the file (Excel or CSV)
            if uploaded_file.name.endswith('.csv'):
                data = pd.read_csv(fs.path(filename))
            elif uploaded_file.name.endswith(('.xls', '.xlsx')):
                data = pd.read_excel(fs.path(filename))
            else:
                return render(request, 'fileuploads/error.html', {'error': 'File format not supported'})

            # Extract specific columns
            extracted_data = data[['Date', 'ACCNO', 'Cust State', 'Cust Pin', 'DPD']]

            return render(request, 'fileuploads/success.html', {'file_url': file_url, 'data': extracted_data.head()})

    else:
        form = FileUploadForm()
    return render(request, 'fileuploads/upload.html', {'form': form})
