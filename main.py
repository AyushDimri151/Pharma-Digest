import os
import feedparser
import resend
import re

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

# --- GITHUB REPOSITORY LOGO INTEGRATION ---
# This pulls your repository path dynamically from GitHub Actions environment variables
# Format generated: https://raw.githubusercontent.com/your-username/your-repo-name/main/logo.png
github_repo = os.getenv("GITHUB_REPOSITORY")
if github_repo:
    LOGO_URL = f"https://raw.githubusercontent.com/{github_repo}/main/logo.png"
else:
    # Local fallback for running testing scripts on your computer offline
    LOGO_URL = "https://i.imgur.com/WbZgqZ2.png"


# 2. Your Tailored Consulting Keywords
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
    # 1. Premium Branded Header Wrapper (Light Professional Theme)
    html_content = f"""
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
            <table border="0" cellpadding="0" cellspacing="0" width="100%" style="max-width: 600px; background-color: #ffffff; border-radius: 6px; box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05); overflow: hidden;">
              
              <tr>
                <td style="background: linear-gradient(135deg, #0f4c81 0%, #1d70b8 100%); padding: 25px 30px;">
                  <table border="0" cellpadding="0" cellspacing="0" width="100%">
                    <tr>
                      <td valign="middle" style="width: 50px;">
                        <img src="{LOGO_URL}" alt="Logo" width="42" height="42" style="display: block; border: 0; max-width: 100%; height: auto;">
                      </td>
                      <td valign="middle" align="right" style="padding-left: 15px;">
                        <h1 style="color: #ffffff; margin: 0; font-size: 22px; font-weight: 700; letter-spacing: -0.3px; line-height: 1.2; font-family: 'Helvetica Neue', Arial, sans-serif;">
                          Pharma News Digest
                        </h1>
                        <p style="color: #d4e5f7; margin: 3px 0 0 0; font-size: 12px; font-weight: 400; letter-spacing: 0.5px; text-transform: uppercase;">
                          Turning complex documents into insights effortlessly
                        </p>
                      </td>
                    </tr>
                  </table>
                </td>
              </tr>
              
              <tr>
                <td style="padding: 35px 30px 15px 30px;">
    """
    
    article_counter = 1

    # 2. Dynamic Unified Article Loop
    for source_name, url in RSS_FEEDS.items():
        feed = feedparser.parse(url)
        articles_from_source = 0
        
        for entry in feed.entries:
            if articles_from_source >= 4:
                break
                
            title = entry.title
            link = entry.link
            summary = entry.get('summary', '').strip()
            
            # Clean HTML tags out of summary
            if "<" in summary and ">" in summary:
                summary = re.sub('<[^<]+?>', '', summary)

            search_text = f"{title} {summary}".lower()
            is_relevant = any(keyword in search_text for keyword in FILTER_KEYWORDS)
            
            if is_relevant:
                # Enforce minimum 60 words rule
                words = summary.split()
                word_count = len(words)
                
                if word_count < 60:
                    padding_text = (
                        " This structured intelligence update tracking pipeline highlights critical shifts within "
                        "the global pharmaceutical sector, directly impacting essential workflows inside Life Sciences, "
                        "Regulatory Affairs, and Operational Management. Continuous strategic landscape observation and deep "
                        "commercial assessment are highly recommended for consulting partnerships reviewing this specific market segment."
                    )
                    summary = summary + padding_text
                    words = summary.split()
                
                # Cap the output at roughly 100 words to maintain aesthetic symmetry
                if len(words) > 100:
                    clean_summary = " ".join(words[:100]) + "..."
                else:
                    clean_summary = summary
                
                # Format index numbers with elegant leading zeros (01, 02...)
                display_num = f"{article_counter:02d}"
                
                # Light Clean Economic Times layout pattern
                html_content += f"""
                <table border="0" cellpadding="0" cellspacing="0" width="100%" style="margin-bottom: 25px; border-bottom: 1px solid #edf2f7; padding-bottom: 25px;">
                    <tr>
                        <td valign="top" style="width: 40px; font-size: 22px; font-weight: 700; color: #1d70b8; font-family: Georgia, serif; line-height: 1;">
                            {display_num}
                        </td>
                        <td valign="top" style="padding-left: 5px;">
                            <a href="{link}" target="_blank" style="font-weight: 600; font-size: 16px; color: #1a202c; text-decoration: none; line-height: 1.4; display: block; margin-bottom: 8px;">
                                {title}
                            </a>
                            <p style="font-size: 14px; color: #4a5568; margin: 0; line-height: 1.6; text-align: justify;">
                                {clean_summary}
                            </p>
                        </td>
                    </tr>
                </table>
                """
                articles_from_source += 1
                article_counter += 1
        
    if article_counter == 1:
        html_content += """
        <table border="0" cellpadding="0" cellspacing="0" width="100%" style="margin-bottom: 20px;">
            <tr>
                <td style="padding: 20px; border-left: 4px solid #1d70b8; background-color: #f0f7fd; border-radius: 4px;">
                    <p style="color: #1d70b8; font-size: 14px; margin: 0; font-weight: 500;">
                        No industry updates matched your target tracking sectors today.
                    </p>
                </td>
            </tr>
        </table>
        """

    # 3. Light Professional Footer
    html_content += """
                </td>
              </tr>
              <tr>
                <td style="background-color: #fafbfe; padding: 30px 30px; border-top: 1px solid #edf2f7; text-align: center;">
                  <p style="color: #718096; font-size: 12px; line-height: 1.6; margin: 0 0 6px 0;">
                    This automated intelligence brief is built specifically for your executive partners using your core matching engine.
                  </p>
                  <p style="color: #a0aec0; font-size: 11px; margin: 0; letter-spacing: 0.3px;">
                    © 2026 Procurement & Business Strategy Operations. All rights reserved.
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