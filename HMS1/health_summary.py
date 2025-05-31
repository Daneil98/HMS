import json
import requests
from django.conf import settings
import logging
import re

logger = logging.getLogger(__name__)




def clean_api_response(text):
    # Remove markdown headers (###, ####) but keep their text
    text = re.sub(r'^#+\s*', '', text, flags=re.MULTILINE)
    
    # Remove bold/italic markers (**text** -> text)
    text = re.sub(r'\*\*([^\*]+)\*\*', r'\1', text)
    text = re.sub(r'\*([^\*]+)\*', r'\1', text)
    
    # Remove horizontal rules (---)
    text = re.sub(r'^---+\s*', '', text, flags=re.MULTILINE)
    
    # Remove bullet points (✔, •) but keep the text
    text = re.sub(r'^[✔•]\s*', '', text, flags=re.MULTILINE)
    
    # Trim excessive whitespace
    text = re.sub(r'\n\s*\n', '\n\n', text)  # Reduce multiple newlines
    return text.strip()


def format_vitals_data(vitals_queryset):
    """Convert vitals queryset to API-friendly format"""
    return [
        {
            'blood_pressure': vital.bp,
            'temperature': vital.temperature,
            'weight': vital.weight,
            'height': vital.height,
        }
        for vital in vitals_queryset
    ]

def get_vital_summary(vitals_queryset, model="deepseek/deepseek-chat-v3-0324:free"):
    """Get health summary from external API"""
    try:
        formatted_vitals = format_vitals_data(vitals_queryset)
        
        headers = {
            "Authorization": f"Bearer {settings.OPENROUTER_API_KEY}",
            "Content-Type": "application/json",
        }
        
        prompt = (
            "Give the standard health vitals for people with that height and weight:\n"
            "Analyze these patient vitals and provide:\n"
            "1. Health rating (1-10)\n"
            "2. Summary of key findings\n"
            "3. Recommendations\n\n"
            f"Vitals data: {json.dumps(formatted_vitals, indent=2)}"
        )
        
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            json={
                "model": model,
                "messages": [{"role": "user", "content": prompt}]
            },
            timeout=15
        )
        response.raise_for_status()
        api_response = response.json()
        
        return {
            'raw': api_response,
            'cleaned': clean_api_response(api_response['choices'][0]['message']['content']),
            'model': api_response['model'],
            'created': api_response['created']
        }
        
    
    except requests.exceptions.RequestException as e:
        logger.error(f"API request failed: {str(e)}")
        raise
    except Exception as e:
        logger.error(f"Error in get_vital_summary: {str(e)}")
        raise
