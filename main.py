import os
import feedparser
import resend

# This looks for the library locally, but won't crash on GitHub if it's missing

# The rest of your script follows...

# Debugging: This will help you see if keys are actually loading in GitHub Actions
api_key = os.getenv("RESEND_API_KEY")
if not api_key:
    print("ERROR: RESEND_API_KEY is not set!")

# 1. Configuration
RSS_FEEDS = {
    "Fierce Pharma": "https://www.fiercepharma.com/rss/pharma",
    "FDA Press": "https://www.fda.gov/about-fda/contact-fda/stay-informed/rss-feeds/press-releases/rss.xml",
    "Endpoints News": "https://endpts.com/feed/"
}

def generate_digest():
    html_content = """
    <div style="font-family: Arial, sans-serif; max-width: 600px; margin: auto; border: 1px solid #eee; padding: 20px;">
        <h2 style="color: #2c3e50; border-bottom: 2px solid #3498db;">Daily Pharma Intelligence Digest</h2>
        <p style="color: #7f8c8d;">Summarized updates for the partnership.</p>
    """
    
    for source_name, url in RSS_FEEDS.items():
        feed = feedparser.parse(url)
        html_content += f"<h3 style='color: #2980b9; margin-top: 25px;'>{source_name}</h3>"
        
        # Take the top 3 items
        for entry in feed.entries[:3]:
            title = entry.title
            link = entry.link
            summary = entry.get('summary', 'No summary available.')[:200] + "..."
            
            html_content += f"""
            <div style="margin-bottom: 15px;">
                <a href="{link}" style="font-weight: bold; color: #34495e; text-decoration: none;">{title}</a>
                <p style="font-size: 14px; color: #34495e; margin: 5px 0;">{summary}</p>
            </div>
            """
            
    html_content += """
        <hr style="border: 0; border-top: 1px solid #eee; margin-top: 20px;">
        <p style="font-size: 12px; color: #bdc3c7; text-align: center;">Automated Pharma Consulting Intel</p>
    </div>
    """
    return html_content

def send_email(content):
    resend.api_key = os.getenv("RESEND_API_KEY")
    
    params = {
        "from": "Pharma Digest <onboarding@resend.dev>", # Update this once you verify your domain
        "to": os.getenv("PARTNER_EMAILS").split(","),
        "subject": "Morning Pharma Intel Update",
        "html": content,
    }


    resend.Emails.send(params)
    print("Digest sent successfully.")

if __name__ == "__main__":
    digest_html = generate_digest()
    send_email(digest_html)