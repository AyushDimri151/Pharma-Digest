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
    # 1. Elegant Header Wrapper (Economic Times Style Background)
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
      <meta charset="UTF-8">
      <meta name="viewport" content="width=device-width, initial-scale=1.0">
    </head>
    <body style="margin: 0; padding: 0; background-color: #111111; font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; -webkit-font-smoothing: antialiased; width: 100% !important;">
      <table border="0" cellpadding="0" cellspacing="0" width="100%" style="background-color: #111111; padding: 40px 10px;">
        <tr>
          <td align="center" valign="top">
            <table border="0" cellpadding="0" cellspacing="0" width="100%" style="max-width: 600px; background-color: #1a1a1a; border-radius: 4px; overflow: hidden;">
              <tr>
                <td align="left" style="background-color: #111111; padding: 25px 20px; border-bottom: 1px solid #2d2d2d;">
                  <h1 style="color: #ffffff; margin: 0; font-size: 22px; font-weight: 700; letter-spacing: -0.5px; line-height: 1.2; text-transform: uppercase;">
                    Daily Pharma Intelligence
                  </h1>
                  <p style="color: #888888; margin: 5px 0 0 0; font-size: 13px; font-weight: 400;">
                    Tailored market tracking & sector snapshots
                  </p>
                </td>
              </tr>
              <tr>
                <td style="padding: 20px 20px 10px 20px;">
    """
    
    article_counter = 1

    # 2. Dynamic Unified Article Loop
    for source_name, url in RSS_FEEDS.items():
        feed = feedparser.parse(url)
        articles_from_source = 0
        
        for entry in feed.entries:
            # Keep a ceiling per source to maintain diversity
            if articles_from_source >= 4:
                break
                
            title = entry.title
            link = entry.link
            summary = entry.get('summary', '').strip()
            
            # Clean HTML tags if present in summary
            if "<" in summary and ">" in summary:
                summary = re.sub('<[^<]+?>', '', summary)

            search_text = f"{title} {summary}".lower()
            is_relevant = any(keyword in search_text for keyword in FILTER_KEYWORDS)
            
            if is_relevant:
                # Count the words in the summary
                word_count = len(summary.split())
                
                # ENFORCE MINIMUM 60 WORDS: If it's too short, pad it out with context
                if word_count < 60:
                    padding_text = (
                        f" This tracking update highlights critical shifts within the pharmaceutical sector, "
                        f"specifically impacting industry sectors such as Life Sciences, Pharmaceutical Manufacturers, "
                        f"and US Government Affairs. This strategic intelligence briefing details ongoing market operational "
                        f"milestones regarding the primary deployment of: {title}. Further investigation and commercial landscape "
                        f"evaluation are highly recommended for consulting partnerships monitoring this specific therapeutic space."
                    )
                    summary = summary + padding_text
                
                # Trim exceptionally long summaries so they stay clean (caps around ~100 words max)
                words = summary.split()
                if len(words) > 100:
                    clean_summary = " ".join(words[:100]) + "..."
                else:
                    clean_summary = summary
                
                # Format counter with leading zero for elegant look (01, 02, etc.)
                display_num = f"{article_counter:02d}"
                
                # Economic Times layout line item structure
                html_content += f"""
                <table border="0" cellpadding="0" cellspacing="0" width="100%" style="margin-bottom: 20px; border-bottom: 1px solid #2d2d2d; padding-bottom: 20px;">
                    <tr>
                        <td valign="top" style="width: 35px; font-size: 20px; font-weight: 700; color: #444444; font-family: Georgia, serif; line-height: 1;">
                            {display_num}
                        </td>
                        <td valign="top">
                            <a href="{link}" target="_blank" style="font-weight: 600; font-size: 16px; color: #ffffff; text-decoration: none; line-height: 1.4; display: block; margin-bottom: 6px;">
                                {title}
                            </a>
                            <p style="font-size: 13px; color: #9aa0a6; margin: 0; line-height: 1.5;">
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
        <div style="padding: 15px; border-left: 3px solid #dd6b20; background-color: #2c1a10; margin-bottom: 20px;">
            <p style="color: #f6ad55; font-size: 14px; margin: 0;">
                No industry updates matched your target tracking sectors today.
            </p>
        </div>
        """

    # 3. Footer Section
    html_content += """
                </td>
              </tr>
              <tr>
                <td style="background-color: #111111; padding: 25px 20px; border-top: 1px solid #2d2d2d; text-align: center;">
                  <p style="color: #666666; font-size: 11px; line-height: 1.5; margin: 0 0 5px 0;">
                    This automated intelligence brief is built specifically for your executive partners using your core matching engine.
                  </p>
                  <p style="color: #444444; font-size: 11px; margin: 0;">
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