#!/usr/bin/env python3
"""
Demo/Test-skript för att verifiera att systemet fungerar
Kör utan riktiga API-nycklar för att testa arkitekturen
"""

import os
import sys
from datetime import datetime

# Simulera att vi har miljövariabler
os.environ['ANTHROPIC_API_KEY'] = 'test-key-demo'
os.environ['SMTP_SERVER'] = 'smtp.example.com'
os.environ['SMTP_PORT'] = '587'
os.environ['EMAIL_FROM'] = 'test@example.com'
os.environ['EMAIL_PASSWORD'] = 'test-password'
os.environ['EMAIL_TO'] = 'recipient@example.com'

from src.data_collector import DataCollector
from src.analyzer import AIAnalyzer
from src.pdf_generator import PDFGenerator


def test_data_collector():
    """Testa datainsamling"""
    print("=" * 80)
    print("TEST 1: DATA COLLECTOR")
    print("=" * 80)

    topics = [
        "Artificiell intelligens",
        "Hållbarhet och klimat",
        "Svensk ekonomi"
    ]

    collector = DataCollector(topics=topics, max_results=3)
    data = collector.collect_data()

    print(f"✓ Samlat data för {len(data)} ämnen")
    for topic, articles in data.items():
        print(f"  - {topic}: {len(articles)} artiklar")

    print("\nExempel på artikel:")
    first_topic = list(data.keys())[0]
    first_article = data[first_topic][0]
    print(f"  Titel: {first_article['title']}")
    print(f"  Källa: {first_article['source']}")
    print(f"  Datum: {first_article['date']}")

    return data


def test_analyzer_structure(data):
    """Testa analysstruktur (utan riktigt API-anrop)"""
    print("\n" + "=" * 80)
    print("TEST 2: ANALYZER STRUCTURE")
    print("=" * 80)

    # Skapa mockad analysdata
    mock_analysis = {
        "executive_summary": "Detta är en sammanfattning av de viktigaste trenderna inom AI, "
                           "hållbarhet och ekonomi för denna månad. AI-utvecklingen accelererar, "
                           "särskilt inom generativa modeller. Hållbarhetsfokus ökar i näringslivet. "
                           "Svensk ekonomi visar tecken på stabilisering.",
        "topic_analyses": {},
        "cross_topic_insights": "Intressanta kopplingar framträder mellan AI och hållbarhet, "
                               "där AI-teknologi används för att optimera energiförbrukning och "
                               "klimatmodellering. Ekonomin påverkas av både AI-innovation och "
                               "grön omställning.",
        "trends": [
            "▸ AI-modeller blir mer energieffektiva och tillgängliga",
            "▸ Ökad användning av AI för klimatanalys och hållbarhetsarbete",
            "▸ Företag investerar mer i grön teknologi",
            "▸ Digitalisering accelererar i offentlig sektor",
            "▸ Fokus på lokal energiproduktion och självförsörjning"
        ],
        "recommendations": [
            "✓ Utvärdera hur AI kan användas för att förbättra din organisations hållbarhetsarbete",
            "✓ Investera i utbildning inom AI och maskinlärning för personalen",
            "✓ Analysera möjligheter till energieffektivisering med ny teknologi",
            "✓ Följ utvecklingen av AI-regleringar och anpassa er verksamhet",
            "✓ Överväg partnerskap med greentech-företag"
        ]
    }

    # Skapa analyser för varje ämne
    for topic, articles in data.items():
        mock_analysis["topic_analyses"][topic] = {
            "topic": topic,
            "analysis": f"""Utvecklingen inom {topic} visar flera intressanta aspekter.

Huvudsakliga utvecklingar:
Under den senaste månaden har vi sett betydande framsteg inom området. Nya initiativ har lanserats och befintliga projekt har utvecklats vidare.

Viktiga aktörer:
Både etablerade aktörer och nya innovatörer driver utvecklingen framåt. Samarbeten mellan akademi, näringsliv och offentlig sektor intensifieras.

Konsekvenser och implikationer:
Förändringarna inom {topic} kommer att ha långsiktig påverkan på samhället. Det är viktigt att följa utvecklingen noga och anpassa strategier därefter.

Framtidsperspektiv:
På kort sikt förväntas ytterligare innovation, medan långsiktigt kan vi se strukturella förändringar i hur vi arbetar med dessa frågor.""",
            "article_count": len(articles),
            "sources": [art["source"] for art in articles]
        }

    print("✓ Analysstruktur skapad")
    print(f"  - Executive summary: {len(mock_analysis['executive_summary'])} tecken")
    print(f"  - Ämnesanalyser: {len(mock_analysis['topic_analyses'])} st")
    print(f"  - Trender: {len(mock_analysis['trends'])} st")
    print(f"  - Rekommendationer: {len(mock_analysis['recommendations'])} st")

    return mock_analysis


def test_pdf_generator(analysis_data):
    """Testa PDF-generering"""
    print("\n" + "=" * 80)
    print("TEST 3: PDF GENERATOR")
    print("=" * 80)

    pdf_generator = PDFGenerator(
        title="Test Omvärldsanalys",
        language="sv"
    )

    try:
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        pdf_path = f"test_rapport_{timestamp}.pdf"

        result_path = pdf_generator.generate_report(
            analysis_data=analysis_data,
            output_path=pdf_path
        )

        # Kontrollera att filen skapades
        if os.path.exists(result_path):
            file_size = os.path.getsize(result_path)
            print(f"✓ PDF genererad: {result_path}")
            print(f"  - Filstorlek: {file_size:,} bytes ({file_size/1024:.1f} KB)")
            return result_path
        else:
            print("✗ PDF-fil hittades inte")
            return None

    except Exception as e:
        print(f"✗ Fel vid PDF-generering: {e}")
        print("\nOBS: WeasyPrint kan kräva systembibliotek.")
        print("För Linux: sudo apt-get install python3-cffi libcairo2 libpango-1.0-0")
        return None


def test_import_modules():
    """Testa att alla moduler kan importeras"""
    print("\n" + "=" * 80)
    print("TEST 0: MODULE IMPORTS")
    print("=" * 80)

    modules = [
        ('DataCollector', 'src.data_collector'),
        ('AIAnalyzer', 'src.analyzer'),
        ('PDFGenerator', 'src.pdf_generator'),
        ('EmailSender', 'src.email_sender'),
        ('AnalysisScheduler', 'src.scheduler')
    ]

    all_ok = True
    for class_name, module_path in modules:
        try:
            module = __import__(module_path, fromlist=[class_name])
            getattr(module, class_name)
            print(f"✓ {class_name} från {module_path}")
        except Exception as e:
            print(f"✗ {class_name} från {module_path}: {e}")
            all_ok = False

    return all_ok


def main():
    """Kör alla tester"""
    print("\n")
    print("╔" + "=" * 78 + "╗")
    print("║" + " " * 20 + "OMVÄRLDSANALYS - SYSTEMTEST" + " " * 30 + "║")
    print("╚" + "=" * 78 + "╝")
    print()

    # Test 0: Importera moduler
    if not test_import_modules():
        print("\n✗ Vissa moduler kunde inte importeras. Avbryter.")
        return False

    # Test 1: Datainsamling
    try:
        data = test_data_collector()
    except Exception as e:
        print(f"\n✗ Datainsamling misslyckades: {e}")
        return False

    # Test 2: Analys (mockad)
    try:
        analysis = test_analyzer_structure(data)
    except Exception as e:
        print(f"\n✗ Analysstruktur misslyckades: {e}")
        return False

    # Test 3: PDF-generering
    try:
        pdf_path = test_pdf_generator(analysis)
    except Exception as e:
        print(f"\n✗ PDF-generering misslyckades: {e}")
        pdf_path = None

    # Sammanfattning
    print("\n" + "=" * 80)
    print("TESTSAMMANFATTNING")
    print("=" * 80)
    print("✓ Modulimport: OK")
    print("✓ Datainsamling: OK")
    print("✓ Analysstruktur: OK")
    print(f"{'✓' if pdf_path else '✗'} PDF-generering: {'OK' if pdf_path else 'MISSLYCKADES'}")
    print("=" * 80)

    if pdf_path:
        print(f"\n🎉 Alla tester godkända! Genererad PDF: {pdf_path}")
        print("\nNOTE: Detta är en demo med simulerad data.")
        print("För riktig användning, konfigurera .env med riktiga API-nycklar.")
    else:
        print("\n⚠️  Systemet fungerar, men PDF-generering kräver ytterligare beroenden.")
        print("Installera: pip install weasyprint")
        print("Samt systembibliotek (se ovan)")

    return True


if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\nTest avbrutet av användare")
        sys.exit(1)
    except Exception as e:
        print(f"\n✗ Oväntat fel: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
