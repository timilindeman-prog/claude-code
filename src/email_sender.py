"""
Email Sender Module
Skickar e-post med PDF-rapporter
"""

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from datetime import datetime
import os


class EmailSender:
    """Skickar e-post med bifogade PDF-rapporter"""

    def __init__(
        self,
        smtp_server: str,
        smtp_port: int,
        email_from: str,
        email_password: str
    ):
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.email_from = email_from
        self.email_password = email_password

    def send_report(
        self,
        email_to: str,
        pdf_path: str,
        subject: str = None
    ) -> bool:
        """
        Skickar PDF-rapport via e-post

        Args:
            email_to: Mottagarens e-postadress
            pdf_path: Sökväg till PDF-filen
            subject: E-postens ämnesrad (valfritt)

        Returns:
            True om e-posten skickades framgångsrikt, annars False
        """
        if subject is None:
            current_month = datetime.now().strftime("%B %Y")
            # Översätt månadsnamn
            month_translations = {
                "January": "Januari", "February": "Februari", "March": "Mars",
                "April": "April", "May": "Maj", "June": "Juni",
                "July": "Juli", "August": "Augusti", "September": "September",
                "October": "Oktober", "November": "November", "December": "December"
            }
            for eng, swe in month_translations.items():
                current_month = current_month.replace(eng, swe)

            subject = f"Månatlig Omvärldsanalys - {current_month}"

        print(f"Skickar e-post till {email_to}...")

        # Skapa e-postmeddelande
        msg = MIMEMultipart()
        msg['From'] = self.email_from
        msg['To'] = email_to
        msg['Subject'] = subject

        # E-postens brödtext
        body = self._create_email_body()
        msg.attach(MIMEText(body, 'html'))

        # Bifoga PDF
        try:
            with open(pdf_path, 'rb') as f:
                pdf_attachment = MIMEApplication(f.read(), _subtype='pdf')
                pdf_attachment.add_header(
                    'Content-Disposition',
                    'attachment',
                    filename=os.path.basename(pdf_path)
                )
                msg.attach(pdf_attachment)
        except FileNotFoundError:
            print(f"Fel: PDF-filen hittades inte: {pdf_path}")
            return False

        # Skicka e-post
        try:
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.email_from, self.email_password)
                server.send_message(msg)

            print(f"E-post skickad framgångsrikt till {email_to}")
            return True

        except Exception as e:
            print(f"Fel vid e-postsändning: {e}")
            return False

    def _create_email_body(self) -> str:
        """Skapar HTML-innehåll för e-postens brödtext"""

        current_date = datetime.now().strftime("%d %B %Y")

        # Översätt månadsnamn
        month_translations = {
            "January": "januari", "February": "februari", "March": "mars",
            "April": "april", "May": "maj", "June": "juni",
            "July": "juli", "August": "augusti", "September": "september",
            "October": "oktober", "November": "november", "December": "december"
        }
        for eng, swe in month_translations.items():
            current_date = current_date.replace(eng, swe)

        return f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        body {{
            font-family: Arial, sans-serif;
            line-height: 1.6;
            color: #333;
        }}
        .container {{
            max-width: 600px;
            margin: 0 auto;
            padding: 20px;
        }}
        .header {{
            background-color: #1a5490;
            color: white;
            padding: 20px;
            text-align: center;
            border-radius: 8px 8px 0 0;
        }}
        .content {{
            background-color: #f9f9f9;
            padding: 30px;
            border: 1px solid #ddd;
        }}
        .footer {{
            background-color: #f0f0f0;
            padding: 15px;
            text-align: center;
            font-size: 12px;
            color: #666;
            border-radius: 0 0 8px 8px;
        }}
        .highlight {{
            background-color: #fff3cd;
            padding: 15px;
            border-left: 4px solid #ffc107;
            margin: 20px 0;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>Månatlig Omvärldsanalys</h1>
            <p>{current_date}</p>
        </div>

        <div class="content">
            <h2>Din omvärldsanalys är klar!</h2>

            <p>Din automatiska omvärldsanalys för denna månad har genererats och finns bifogad som PDF.</p>

            <div class="highlight">
                <strong>Vad innehåller rapporten?</strong>
                <ul>
                    <li>Övergripande sammanfattning av viktiga utvecklingar</li>
                    <li>Djupgående analyser av dina valda ämnesområden</li>
                    <li>Identifierade trender och mönster</li>
                    <li>Konkreta rekommendationer</li>
                    <li>Övergripande insikter och samband mellan olika områden</li>
                </ul>
            </div>

            <p>Analysen är skapad med hjälp av AI-driven teknologi som samlar in, analyserar och
            sammanställer information från olika källor för att ge dig en omfattande bild av
            utvecklingen inom dina intresseområden.</p>

            <p><strong>Öppna den bifogade PDF-filen för att läsa hela rapporten.</strong></p>
        </div>

        <div class="footer">
            <p>Detta är ett automatiskt genererat meddelande från ditt omvärldsanalyssystem.</p>
            <p>Rapporten genererades {datetime.now().strftime("%Y-%m-%d kl. %H:%M")}</p>
        </div>
    </div>
</body>
</html>
"""
