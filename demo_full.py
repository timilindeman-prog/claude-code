#!/usr/bin/env python3
"""
Fullständig Demo av Omvärldsanalyssystemet
Kör hela flödet med mockad AI-analys
"""

import os
import sys
import yaml
from datetime import datetime
from dotenv import load_dotenv

from src.data_collector import DataCollector
from src.pdf_generator import PDFGenerator


class MockAIAnalyzer:
    """Mockad AI-analyzer för demo-syfte"""

    def __init__(self, api_key=None, depth="standard"):
        self.depth = depth
        print(f"[DEMO MODE] Använder mockad AI-analys (depth: {depth})")

    def analyze_data(self, data, include_recommendations=True, include_trends=True):
        """Skapar mockad analysdata"""
        print("\n🤖 AI-ANALYS (Demo-läge med simulerad AI)")
        print("-" * 80)

        analysis_results = {
            "executive_summary": "",
            "topic_analyses": {},
            "cross_topic_insights": "",
            "trends": [] if include_trends else None,
            "recommendations": [] if include_recommendations else None
        }

        # Analysera varje ämne med mockad data
        for topic, articles in data.items():
            print(f"  Analyserar: {topic}...")
            analysis_results["topic_analyses"][topic] = self._mock_topic_analysis(topic, articles)

        # Skapa mockad sammanfattning
        print("  Skapar sammanfattning...")
        analysis_results["executive_summary"] = self._mock_executive_summary(data)

        # Mockade kopplingar
        print("  Analyserar kopplingar mellan ämnen...")
        analysis_results["cross_topic_insights"] = self._mock_cross_topic_insights(data)

        # Mockade trender
        if include_trends:
            print("  Identifierar trender...")
            analysis_results["trends"] = self._mock_trends(data)

        # Mockade rekommendationer
        if include_recommendations:
            print("  Genererar rekommendationer...")
            analysis_results["recommendations"] = self._mock_recommendations(data)

        print("✓ AI-analys slutförd (mockad)")
        return analysis_results

    def _mock_topic_analysis(self, topic, articles):
        """Genererar mockad analys för ett ämne"""
        analysis_text = f"""Utvecklingen inom {topic} under den senaste månaden visar flera avgörande trender som påverkar både näringslivet och samhället i stort.

**Huvudsakliga utvecklingar**

Den senaste månaden har präglats av betydande framsteg inom {topic}. Nya innovationer har introducerats och befintliga lösningar har vidareutvecklats. Särskilt intressant är den ökade takten i utvecklingen, där flera parallella initiativ nu börjar ge synliga resultat.

**Viktiga aktörer och drivkrafter**

Både etablerade företag och nya startups driver utvecklingen framåt. Vi ser också ett ökat samarbete mellan olika sektorer - akademi, näringsliv och offentlig sektor arbetar allt mer integrerat. Detta skapar en dynamisk miljö där innovation kan blomstra.

**Konsekvenser och implikationer**

Förändringarna inom {topic} får långtgående konsekvenser. På kort sikt ser vi direkta effekter på hur organisationer arbetar och vilka möjligheter som öppnas. På längre sikt kan vi förvänta oss mer fundamentala förändringar i samhällsstrukturer och arbetssätt.

**Framtidsperspektiv**

Prognoserna pekar mot fortsatt acceleration inom området. De närmaste månaderna förväntas ge oss fler genombrott, samtidigt som de långsiktiga implikationerna av dagens utveckling gradvis blir tydligare. Det är kritiskt att följa utvecklingen noga och anpassa strategier kontinuerligt."""

        return {
            "topic": topic,
            "analysis": analysis_text,
            "article_count": len(articles),
            "sources": list(set([art["source"] for art in articles]))
        }

    def _mock_executive_summary(self, data):
        """Skapar mockad sammanfattning"""
        topics_str = ", ".join(list(data.keys())[:-1]) + f" och {list(data.keys())[-1]}"

        return f"""Denna månads omvärldsanalys täcker utvecklingen inom {topics_str}.

Övergripande ser vi en period av intensiv innovation och förändring. Flera långsiktiga trender accelererar nu samtidigt, vilket skapar både möjligheter och utmaningar. Särskilt tydligt är hur olika utvecklingsområden påverkar och förstärker varandra.

Nyckelinsikter inkluderar ökad digitalisering, fokus på hållbarhet och effektivitet, samt nya samarbetsformer mellan olika sektorer. Organisationer som kan navigera dessa förändringar och anpassa sig snabbt kommer att ha betydande fördelar.

Rekommendationerna i denna rapport fokuserar på konkreta åtgärder för att positionera sig väl inför kommande utveckling."""

    def _mock_cross_topic_insights(self, data):
        """Skapar mockade övergripande insikter"""
        topics = list(data.keys())

        return f"""En djupare analys av sambanden mellan de olika ämnesområdena avslöjar flera intressanta kopplingar och synergier.

**Konvergerande trender**

Vi ser hur utvecklingen inom {topics[0]} direkt påverkar och möjliggör framsteg inom {topics[1] if len(topics) > 1 else 'relaterade områden'}. Detta skapar en positiv förstärkningseffekt där innovation inom ett område driver utveckling inom andra.

**Systemiska samband**

De undersökta områdena är inte isolerade fenomen utan delar av ett större system. Förändringar på ett område får ofta oväntade effekter på andra. Detta understryker vikten av ett holistiskt perspektiv när man analyserar och agerar på omvärldsutveckling.

**Strategiska implikationer**

För organisationer innebär dessa kopplingar både möjligheter och komplexitet. De som kan identifiera och utnyttja synergier mellan olika utvecklingsområden kan skapa unika konkurransfördelar. Samtidigt kräver den ökade komplexiteten mer sofistikerade analysverktyg och strategier.

**Framväxande ekosystem**

Vi ser början på nya ekosystem där aktörer från olika sektorer samarbetar på innovativa sätt. Detta öppnar för nya affärsmodeller och samarbetsformer som kan förändra hela branscher."""

    def _mock_trends(self, data):
        """Genererar mockade trender"""
        topics = list(data.keys())

        base_trends = [
            f"Accelererande innovation inom {topics[0]} med fokus på praktiska tillämpningar och skalbarhet",
            f"Ökad integration mellan {topics[0]} och hållbarhetsfrågor, där teknik används för att adressera klimatutmaningar",
            "Organisationer investerar allt mer i digital transformation och kompetenshöjning för att hänga med i utvecklingen",
            "Nya samarbetsmodeller mellan offentlig och privat sektor driver innovation och skapar samhällsnytta",
            "Fokus skiftar från enbart teknisk innovation till helhetslösningar som inkluderar sociala och miljömässiga aspekter",
            "Regulatory framework utvecklas för att hantera nya teknologier på ett ansvarsfullt sätt",
            "Demokratisering av avancerad teknologi gör att fler aktörer kan delta i innovationsprocessen"
        ]

        return base_trends[:7]

    def _mock_recommendations(self, data):
        """Skapar mockade rekommendationer"""
        topics = list(data.keys())

        recommendations = [
            f"Investera i kontinuerlig kompetensutveckling inom {topics[0]} för att säkerställa att organisationen håller sig uppdaterad",
            "Utveckla en tydlig strategi för hur nya teknologier och trender kan integreras i verksamheten på ett hållbart sätt",
            "Etablera partnerskap och samarbeten med aktörer i framkant för att få tidig tillgång till ny kunskap och innovation",
            "Sätt upp mätbara mål för hur organisationen ska arbeta med identifierade trender och följ upp regelbundet",
            "Skapa tvärfunktionella team som kan arbeta med komplexitet och kopplingar mellan olika utvecklingsområden",
            "Allokera resurser för experiment och pilotprojekt som kan testa nya koncept i liten skala",
            "Utveckla en proaktiv omvärldsbevakning som kontinuerligt fångar upp nya trender och möjligheter"
        ]

        return recommendations[:7]


class MockEmailSender:
    """Mockad e-postsändare för demo"""

    def __init__(self, smtp_server, smtp_port, email_from, email_password):
        self.email_from = email_from
        self.smtp_server = smtp_server
        print(f"\n[DEMO MODE] E-postsändning simuleras (från: {email_from})")

    def send_report(self, email_to, pdf_path, subject=None):
        """Simulerar e-postsändning"""
        print(f"\n📧 E-POST (Demo-läge - simulerad sändning)")
        print("-" * 80)
        print(f"  Från: {self.email_from}")
        print(f"  Till: {email_to}")
        print(f"  Ämne: {subject or 'Månatlig Omvärldsanalys'}")
        print(f"  Bilaga: {pdf_path}")
        print(f"  Status: ✓ Skulle ha skickats (demo-läge)")
        return True


def load_config(config_path: str = "config.yaml") -> dict:
    """Läser in konfigurationsfil"""
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        print(f"Fel: Konfigurationsfil '{config_path}' hittades inte")
        sys.exit(1)


def run_full_demo():
    """Kör fullständig demo av hela systemet"""
    print("╔" + "=" * 78 + "╗")
    print("║" + " " * 15 + "FULLSTÄNDIG DEMO - OMVÄRLDSANALYSSYSTEM" + " " * 23 + "║")
    print("╚" + "=" * 78 + "╝")
    print()
    print("Detta är en komplett genomgång av hela analysprocessen med mockad AI.")
    print("Alla steg körs förutom riktig AI-analys och e-postsändning.")
    print()
    print(f"Startad: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 80)
    print()

    # Ladda miljövariabler
    load_dotenv()

    # Ladda konfiguration
    config = load_config()

    # STEG 1: DATAINSAMLING
    print("📊 [STEG 1/5] DATAINSAMLING")
    print("-" * 80)

    collector = DataCollector(
        topics=config['topics'],
        max_results=config['search']['max_results_per_topic'],
        language=config['search']['language']
    )

    data = collector.collect_data()
    total_articles = sum(len(articles) for articles in data.values())
    print(f"\n✓ Datainsamling slutförd")
    print(f"  - Ämnen: {len(data)}")
    print(f"  - Totalt artiklar: {total_articles}")

    # STEG 2: AI-ANALYS (MOCKAD)
    print("\n🤖 [STEG 2/5] AI-ANALYS")
    print("-" * 80)

    analyzer = MockAIAnalyzer(
        api_key=os.getenv('ANTHROPIC_API_KEY'),
        depth=config['analysis']['depth']
    )

    analysis_results = analyzer.analyze_data(
        data=data,
        include_recommendations=config['analysis']['include_recommendations'],
        include_trends=config['analysis']['include_trends']
    )

    # STEG 3: PDF-GENERERING
    print("\n📄 [STEG 3/5] PDF-GENERERING")
    print("-" * 80)

    pdf_generator = PDFGenerator(
        title=config['pdf']['title'],
        language=config['pdf']['language']
    )

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    pdf_path = f"omvarldsanalys_demo_{timestamp}.pdf"

    pdf_path = pdf_generator.generate_report(
        analysis_data=analysis_results,
        output_path=pdf_path
    )

    if os.path.exists(pdf_path):
        file_size = os.path.getsize(pdf_path)
        print(f"\n✓ PDF-generering slutförd")
        print(f"  - Fil: {pdf_path}")
        print(f"  - Storlek: {file_size:,} bytes ({file_size/1024:.1f} KB)")

    # STEG 4: E-POSTSÄNDNING (MOCKAD)
    print("\n📧 [STEG 4/5] E-POSTSÄNDNING")
    print("-" * 80)

    email_sender = MockEmailSender(
        smtp_server=os.getenv('SMTP_SERVER'),
        smtp_port=int(os.getenv('SMTP_PORT', 587)),
        email_from=os.getenv('EMAIL_FROM'),
        email_password=os.getenv('EMAIL_PASSWORD')
    )

    success = email_sender.send_report(
        email_to=os.getenv('EMAIL_TO'),
        pdf_path=pdf_path
    )

    # STEG 5: SAMMANFATTNING
    print("\n✅ [STEG 5/5] SAMMANFATTNING")
    print("=" * 80)
    print()
    print("🎉 Fullständig demo genomförd!")
    print()
    print("Resultat:")
    print(f"  ✓ Datainsamling: {len(data)} ämnen, {total_articles} artiklar")
    print(f"  ✓ AI-Analys: {len(analysis_results['topic_analyses'])} ämnesanalyser")
    print(f"  ✓ Trender: {len(analysis_results['trends'])} identifierade")
    print(f"  ✓ Rekommendationer: {len(analysis_results['recommendations'])} skapade")
    print(f"  ✓ PDF genererad: {pdf_path}")
    print(f"  ✓ E-post simulerad till: {os.getenv('EMAIL_TO')}")
    print()
    print("=" * 80)
    print()
    print("💡 Nästa steg:")
    print("   1. Granska den genererade PDF:en")
    print("   2. Anpassa config.yaml efter dina behov")
    print("   3. Lägg till riktig ANTHROPIC_API_KEY i .env")
    print("   4. Kör 'python main.py --once' för riktig analys")
    print()
    print("=" * 80)

    return pdf_path


if __name__ == "__main__":
    try:
        pdf_path = run_full_demo()
        print(f"\n✅ Demo slutförd! PDF: {pdf_path}")
        sys.exit(0)
    except KeyboardInterrupt:
        print("\n\n⚠️  Demo avbruten av användare")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Fel uppstod: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
