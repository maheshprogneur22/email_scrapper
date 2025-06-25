# import pandas as pd
# import io
# from django.shortcuts import render
# from django.http import HttpResponse
# from .scraper import scrape_emails_from_url_list
#
# def home(request):
#     if request.method == 'POST' and request.FILES.get('file'):
#         df = pd.read_excel(request.FILES['file'])
#         urls = df.iloc[:, 0].dropna().tolist()
#
#         results = scrape_emails_from_url_list(urls)
#
#         output = io.BytesIO()
#         df_out = pd.DataFrame(results)
#         df_out.to_excel(output, index=False)
#         output.seek(0)
#
#         response = HttpResponse(
#             output,
#             content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
#         )
#         response['Content-Disposition'] = 'attachment; filename="scraped_emails.xlsx"'
#         return response
#
#     return render(request, 'index.html')


import pandas as pd
import io
import threading
from django.shortcuts import render
from django.http import HttpResponse
from .scraper import scrape_emails_from_url_list

# Store scraped data and status in global variables (for demo)
scrape_results = None
scrape_in_progress = False

def run_scraper_in_background(urls):
    global scrape_results, scrape_in_progress
    scrape_in_progress = True
    try:
        scrape_results = scrape_emails_from_url_list(urls)
    except Exception as e:
        scrape_results = [{'url': 'Error', 'emails': str(e)}]
    scrape_in_progress = False

def home(request):
    global scrape_results, scrape_in_progress

    if request.method == 'POST' and request.FILES.get('file'):
        df = pd.read_excel(request.FILES['file'])
        # urls = df.iloc[:, 0].dropna().tolist()
        urls = df.iloc[:10, 0].dropna().tolist()
        # Start background scraping
        scrape_results = None
        threading.Thread(target=run_scraper_in_background, args=(urls,), daemon=True).start()

        return render(request, 'index.html', {'message': "✅ Scraping started! Refresh to check progress."})

    if scrape_results and not scrape_in_progress:
        # Serve the result file if available
        output = io.BytesIO()
        df_out = pd.DataFrame(scrape_results)
        df_out.to_excel(output, index=False)
        output.seek(0)
        response = HttpResponse(
            output,
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = 'attachment; filename="scraped_emails.xlsx"'
        scrape_results = None  # Reset after serving
        return response

    return render(request, 'index.html', {
        'message': "⏳ Scraping in progress..." if scrape_in_progress else None
    })
