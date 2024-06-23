import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.shortcuts import get_object_or_404
from reportbot.models import Report
import spacy

# Load the SpaCy model
nlp = spacy.load("en_core_web_sm")

@csrf_exempt
@require_POST
def get_report(request):
    try:
        data = json.loads(request.body.decode('utf-8'))
        user_message = data.get('message', '')
        
        # Simple NLP to extract report name
        doc = nlp(user_message)
        report_name = None
        print(report_name)
        print(doc)
        print(type(doc))
        for token in doc:
    # Check if token text matches "report" and its dependency is 'nsubj'
            if token.text.lower() == "report":
        # Check children of 'report' for potential modifiers like 'amod' or 'compound'
                for child in token.children:
                    if child.dep_ == 'amod' or child.dep_ == 'compound':
                        report_name = child.text
                        break  # Exit inner loop once a modifier is found
        # If no modifier is found, default to 'report' itself
                if report_name is None:
                    report_name = token.text
                break 
        print(report_name)
        if not report_name:
            print("hi")
            return JsonResponse({'error': 'Report name not found in message.'}, status=400)
        
        # Find report in database
        report = get_object_or_404(Report, report_name__iexact=report_name.strip())
        
        return JsonResponse({'report_url': report.report_url})
    
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON data.'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
