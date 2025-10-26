# alert_sender.py (Logic used by the Matching Daemon)

import os
from resend import Resend
from typing import List, Dict, Any

# NOTE: The Resend API key would be loaded from a secret management service (e.g., Supabase or environment variables)
RESEND_API_KEY = os.getenv("RESEND_API_KEY") # Ensure this key is set in your .env/secrets

def format_jobs_for_email(top_jobs: List[Dict[str, Any]]) -> str:
    """Formats the top 3 jobs and their scores into HTML for the email body."""
    
    html_content = "<h2>Your Personalized Job Alerts Are Ready!</h2>"
    
    for job in top_jobs:
        html_content += f"""
        <div style="border: 1px solid #ddd; padding: 15px; margin-bottom: 20px; border-radius: 8px;">
            <h3 style="color: #007bff; margin-top: 0;">{job['title']} at {job['company_name']}</h3>
            <p style="font-weight: bold;">Match Score: {job['match_score']}%</p>
            <p><b>Why It's a Fit:</b> {job['perfect_fit_reason']}</p>
            <p><a href="{job['source_url']}" style="background-color: #28a745; color: white; padding: 10px 15px; text-decoration: none; border-radius: 5px;">Apply Now</a></p>
        </div>
        """
    return html_content

def send_job_alert_email(recipient_email: str, top_jobs: List[Dict[str, Any]]) -> bool:
    """Sends the job alert using the Resend Python SDK."""
    
    if not RESEND_API_KEY:
        print("Resend API Key is missing. Email skipped.")
        return False

    try:
        resend_client = Resend(api_key=RESEND_API_KEY)
        
        email_html = format_jobs_for_email(top_jobs)
        
        # Resend API call
        resend_client.emails.send({
            'from': 'alerts@yourdomain.com', # Use a verified sender domain here
            'to': recipient_email,
            'subject': f"🎯 Your Top 3 Personalized Job Matches from PortfolioAI!",
            'html': email_html
        })
        
        print(f"Successfully sent job alert to {recipient_email}")
        return True
    
    except Exception as e:
        print(f"Resend email failure: {e}")
        return False