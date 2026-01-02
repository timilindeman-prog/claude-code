"""
PDF Generator Module
Skapar snygga PDF-rapporter från analysdata
"""

from weasyprint import HTML, CSS
from datetime import datetime
from typing import Dict
import os


class PDFGenerator:
    """Genererar professionella PDF-rapporter"""

    def __init__(self, title: str = "Omvärldsanalys", language: str = "sv"):
        self.title = title
        self.language = language

    def generate_report(
        self,
        analysis_data: Dict,
        output_path: str = None
    ) -> str:
        """
        Genererar en PDF-rapport från analysdata

        Args:
            analysis_data: Analysresultat från AIAnalyzer
            output_path: Sökväg där PDF ska sparas

        Returns:
            Sökväg till den genererade PDF-filen
        """
        if output_path is None:
            timestamp = datetime.now().strftime("%Y-%m-%d")
            output_path = f"omvärldsanalys_{timestamp}.pdf"

        print(f"Genererar PDF-rapport: {output_path}")

        # Skapa HTML-innehåll
        html_content = self._create_html(analysis_data)

        # Generera PDF
        HTML(string=html_content).write_pdf(
            output_path,
            stylesheets=[CSS(string=self._get_css())]
        )

        print(f"PDF-rapport skapad: {output_path}")
        return output_path

    def _create_html(self, analysis_data: Dict) -> str:
        """Skapar HTML-innehåll för rapporten"""

        current_date = datetime.now().strftime("%B %Y")

        # Översätt månadsnamn till svenska
        month_translations = {
            "January": "Januari", "February": "Februari", "March": "Mars",
            "April": "April", "May": "Maj", "June": "Juni",
            "July": "Juli", "August": "Augusti", "September": "September",
            "October": "Oktober", "November": "November", "December": "December"
        }

        for eng, swe in month_translations.items():
            current_date = current_date.replace(eng, swe)

        html = f"""
<!DOCTYPE html>
<html lang="{self.language}">
<head>
    <meta charset="UTF-8">
    <title>{self.title}</title>
</head>
<body>
    <div class="cover-page">
        <h1>{self.title}</h1>
        <p class="date">{current_date}</p>
        <div class="cover-footer">
            <p>Automatisk AI-driven omvärldsanalys</p>
        </div>
    </div>

    <div class="content">
        <div class="section">
            <h2>Sammanfattning</h2>
            <p class="executive-summary">{analysis_data.get('executive_summary', 'Ingen sammanfattning tillgänglig.')}</p>
        </div>

        <div class="section">
            <h2>Ämnesanalyser</h2>
            {self._create_topic_sections(analysis_data.get('topic_analyses', {}))}
        </div>

        {self._create_cross_topic_section(analysis_data.get('cross_topic_insights'))}

        {self._create_trends_section(analysis_data.get('trends'))}

        {self._create_recommendations_section(analysis_data.get('recommendations'))}
    </div>

    <div class="footer">
        <p>Genererad {datetime.now().strftime("%Y-%m-%d %H:%M")}</p>
    </div>
</body>
</html>
"""
        return html

    def _create_topic_sections(self, topic_analyses: Dict) -> str:
        """Skapar HTML för ämnesanalyser"""
        sections = []

        for topic, analysis in topic_analyses.items():
            analysis_text = analysis.get('analysis', 'Ingen analys tillgänglig.')
            article_count = analysis.get('article_count', 0)
            sources = analysis.get('sources', [])

            # Formatera analystext med paragrafer
            paragraphs = analysis_text.split('\n\n')
            formatted_text = ''.join([f'<p>{p.strip()}</p>' for p in paragraphs if p.strip()])

            section = f"""
            <div class="topic-section">
                <h3>{topic}</h3>
                <p class="meta">Baserat på {article_count} källor</p>
                {formatted_text}
            </div>
            """
            sections.append(section)

        return '\n'.join(sections)

    def _create_cross_topic_section(self, insights: str) -> str:
        """Skapar sektion för övergripande insikter"""
        if not insights:
            return ""

        paragraphs = insights.split('\n\n')
        formatted_text = ''.join([f'<p>{p.strip()}</p>' for p in paragraphs if p.strip()])

        return f"""
        <div class="section">
            <h2>Övergripande insikter och samband</h2>
            {formatted_text}
        </div>
        """

    def _create_trends_section(self, trends: list) -> str:
        """Skapar sektion för trender"""
        if not trends:
            return ""

        trends_html = '\n'.join([f'<li>{trend}</li>' for trend in trends if trend.strip()])

        return f"""
        <div class="section">
            <h2>Identifierade trender</h2>
            <ul class="trends-list">
                {trends_html}
            </ul>
        </div>
        """

    def _create_recommendations_section(self, recommendations: list) -> str:
        """Skapar sektion för rekommendationer"""
        if not recommendations:
            return ""

        recs_html = '\n'.join([f'<li>{rec}</li>' for rec in recommendations if rec.strip()])

        return f"""
        <div class="section recommendations">
            <h2>Rekommendationer</h2>
            <ul class="recommendations-list">
                {recs_html}
            </ul>
        </div>
        """

    def _get_css(self) -> str:
        """Returnerar CSS för PDF-rapporten"""
        return """
        @page {
            size: A4;
            margin: 2cm;
            @bottom-center {
                content: counter(page);
            }
        }

        body {
            font-family: 'Helvetica', 'Arial', sans-serif;
            line-height: 1.6;
            color: #333;
        }

        .cover-page {
            text-align: center;
            padding-top: 8cm;
            page-break-after: always;
        }

        .cover-page h1 {
            font-size: 48px;
            color: #1a5490;
            margin-bottom: 0.5cm;
            font-weight: bold;
        }

        .cover-page .date {
            font-size: 24px;
            color: #666;
            margin-top: 1cm;
        }

        .cover-page .cover-footer {
            position: absolute;
            bottom: 3cm;
            left: 2cm;
            right: 2cm;
            text-align: center;
            color: #999;
        }

        .content {
            page-break-before: always;
        }

        .section {
            margin-bottom: 2cm;
            page-break-inside: avoid;
        }

        h2 {
            color: #1a5490;
            font-size: 24px;
            margin-top: 1.5cm;
            margin-bottom: 0.5cm;
            border-bottom: 2px solid #1a5490;
            padding-bottom: 0.2cm;
        }

        h3 {
            color: #2874a6;
            font-size: 18px;
            margin-top: 1cm;
            margin-bottom: 0.3cm;
        }

        .executive-summary {
            background-color: #f0f7ff;
            padding: 1cm;
            border-left: 4px solid #1a5490;
            font-size: 14px;
            margin-bottom: 1cm;
        }

        .topic-section {
            margin-bottom: 1.5cm;
            page-break-inside: avoid;
        }

        .meta {
            color: #666;
            font-size: 12px;
            font-style: italic;
            margin-bottom: 0.5cm;
        }

        p {
            margin-bottom: 0.5cm;
            text-align: justify;
        }

        .trends-list, .recommendations-list {
            list-style-type: none;
            padding-left: 0;
        }

        .trends-list li, .recommendations-list li {
            margin-bottom: 0.5cm;
            padding-left: 1cm;
            position: relative;
        }

        .trends-list li:before {
            content: "▸";
            color: #1a5490;
            font-weight: bold;
            position: absolute;
            left: 0;
        }

        .recommendations-list li:before {
            content: "✓";
            color: #27ae60;
            font-weight: bold;
            position: absolute;
            left: 0;
        }

        .recommendations {
            background-color: #f9fff9;
            padding: 0.8cm;
            border-radius: 8px;
        }

        .footer {
            margin-top: 2cm;
            text-align: center;
            color: #999;
            font-size: 10px;
            border-top: 1px solid #ddd;
            padding-top: 0.5cm;
        }
        """
