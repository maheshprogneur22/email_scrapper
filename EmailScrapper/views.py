import io
import os
import pandas as pd
from django.conf import settings
from django.shortcuts import render
from django.http import HttpResponse
from .scraper import scrape_emails_from_url_list

def home(request):
    if request.method == 'POST' and request.FILES.get('file'):
        file = request.FILES['file']
        file_name = file.name

        # Save the uploaded file to MEDIA_ROOT
        file_path = os.path.join(settings.MEDIA_ROOT, file_name)
        with open(file_path, 'wb') as destination:
            for chunk in file.chunks():
                destination.write(chunk)

        # Now read the file and process it
        df = pd.read_excel(file_path)
        urls = df.iloc[:, 0].dropna().tolist()

        results = scrape_emails_from_url_list(urls)

        output = io.BytesIO()
        df_out = pd.DataFrame(results)
        df_out.to_excel(output, index=False)
        output.seek(0)

        response = HttpResponse(
            output,
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = 'attachment; filename="scraped_emails.xlsx"'
        return response

    return render(request, 'index.html')
