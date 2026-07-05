import os
import feedparser
import resend

# Debugging: This will help you see if keys are actually loading in GitHub Actions
api_key = os.getenv("RESEND_API_KEY")
if not api_key:
    print("ERROR: RESEND_API_KEY is not set!")

# 1. Configuration
RSS_FEEDS = {
    "Fierce Pharma": "https://www.fiercepharma.com/rss.xml",
    "FDA Press": "https://www.fda.gov/about-fda/contact-fda/stay-informed/rss-feeds/press-releases/rss.xml",
    "Endpoints News": "https://endpts.com/feed/"
}

# 2. Your Tailored Consulting Keywords (Cleaned up for efficient text matching)
FILTER_KEYWORDS = [
    # Topics
    "market trend", "pricing", "shortage", "forecast",
    "merger", "acquisition", "m&a", "partner", "deal", "buyout", "collaboration",
    "ai ", "artificial intelligence", "digital health", "telehealth", "machine learning",
    "approval", "fda", "regulatory", "clearance", "clinical trial", "phase",
    
    # Industry Sectors
    "hospital", "provider", "consulting", "life sciences", "biotech",
    "technology", "manufacturer", "government", "policy", "legislation", "medicare"
]

def generate_digest():
    # 1. Elegant Header Wrapper
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
      <meta charset="UTF-8">
      <meta name="viewport" content="width=device-width, initial-scale=1.0">
    </head>
    <body style="margin: 0; padding: 0; background-color: #f4f6f8; font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; -webkit-font-smoothing: antialiased; width: 100% !important;">
      <table border="0" cellpadding="0" cellspacing="0" width="100%" style="background-color: #f4f6f8; padding: 40px 10px;">
        <tr>
          <td align="center" valign="top">
            <table border="0" cellpadding="0" cellspacing="0" width="100%" style="max-width: 600px; background-color: #ffffff; border-radius: 8px; box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05); overflow: hidden;">
              <tr>
                <td align="center" style="background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%); padding: 35px 40px;">
                  <h1 style="color: #ffffff; margin: 0; font-size: 24px; font-weight: 600; letter-spacing: -0.5px; line-height: 1.2;">
                    Daily Pharma Intelligence Digest
                  </h1>
                  <p style="color: #e0e6ed; margin: 8px 0 0 0; font-size: 14px; font-weight: 300;">
                    Tailored market tracking & sector snapshots
                  </p>
                </td>
              </tr>
              <tr>
                <td style="padding: 40px 40px 30px 40px;">
    """
    
    total_articles_found = 0

    # 2. Dynamic Article Processing Loop
    for source_name, url in RSS_FEEDS.items():
        feed = feedparser.parse(url)
        source_html = ""
        articles_from_source = 0
        
        for entry in feed.entries:
            if articles_from_source >= 4:
                break
                
            title = entry.title
            link = entry.link
            summary = entry.get('summary', 'No summary available.')
            
            search_text = f"{title} {summary}".lower()
            is_relevant = any(keyword in search_text for keyword in FILTER_KEYWORDS)
            
            if is_relevant:
                clean_summary = summary[:200] + "..." if len(summary) > 200 else summary
                
                # Upgraded modern styling for individual article entries
                source_html += f"""
                <div style="margin-bottom: 24px; border-bottom: 1px solid #f0f4f8; padding-bottom: 16px;">
                    <a href="{link}" target="_blank" style="font-weight: 600; font-size: 16px; color: #1e3c72; text-decoration: none; line-height: 1.4; display: block;">
                        {title}
                    </a>
                    <p style="font-size: 14px; color: #4a5568; margin: 8px 0 0 0; line-height: 1.6;">
                        {clean_summary}
                    </p>
                </div>
                """
                articles_from_source += 1
                total_articles_found += 1
        
        if articles_from_source > 0:
            # Modern Source Section Header Layout
            html_content += f"""
            <h3 style="color: #2a5298; font-size: 13px; font-weight: 700; text-transform: uppercase; letter-spacing: 1.2px; margin: 30px 0 15px 0; border-left: 3px solid #1e3c72; padding-left: 10px;">
                {source_name}
            </h3>
            """ + source_html
            
    if total_articles_found == 0:
        html_content += """
        <div style="padding: 20px; background-color: #fffaf0; border-left: 4px solid #dd6b20; border-radius: 4px; margin-bottom: 20px;">
            <p style="color: #dd6b20; font-size: 14px; margin: 0; font-weight: 500;">
                No industry updates matched your target tracking sectors today.
            </p>
        </div>
        """

    # 3. Clean Professional Footer
    html_content += """
                </td>
              </tr>
              <tr>
                <td style="background-color: #fafbfe; padding: 30px 40px; border-top: 1px solid #edf2f7; text-align: center;">
                  <p style="color: #718096; font-size: 12px; line-height: 1.6; margin: 0 0 8px 0;">
                    This automated intelligence brief is built specifically for your executive partners using your core matching engine.
                  </p>
                  <p style="color: #a0aec0; font-size: 11px; margin: 0;">
                    © 2026 Automated Pharma Consulting Intel. All rights reserved.
                  </p>
                </td>
              </tr>
            </table>
          </td>
        </tr>
      </table>
    </body>
    </html>
    """
    return html_content

def send_email(content):
    resend.api_key = os.getenv("RESEND_API_KEY")
    
    params = {
        "from": "Pharma Digest <onboarding@resend.dev>", 
        "to": os.getenv("PARTNER_EMAILS").split(","),
        "subject": "Morning Pharma Intel Update",
        "html": content,
    }

    resend.Emails.send(params)
    print("Digest sent successfully.")

if __name__ == "__main__":
    digest_html = generate_digest()
    send_email(digest_html)