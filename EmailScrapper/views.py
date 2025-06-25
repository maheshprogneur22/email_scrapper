import pandas as pd
import io
from django.shortcuts import render
from django.http import HttpResponse
from .scraper import scrape_emails_from_url_list

def home(request):
    if request.method == 'POST' and request.FILES.get('file'):
        df = pd.read_excel(request.FILES['file'])
        # urls = df.iloc[:, 0].dropna().tolist()
        urls = df.iloc[:10, 0].dropna().tolist()

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