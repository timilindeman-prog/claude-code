#!/usr/bin/env python3
"""
Automatisk Omvärldsanalys
Huvudskript som orkestrerar hela analysprocessen
"""

import os
import sys
import yaml
import argparse
from datetime import datetime
from dotenv import load_dotenv

from src.data_collector import DataCollector
from src.analyzer import AIAnalyzer
from src.pdf_generator import PDFGenerator
from src.email_sender import EmailSender
from src.scheduler import AnalysisScheduler


def load_config(config_path: str = "config.yaml") -> dict:
    """Läser in konfigurationsfil"""
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        print(f"Fel: Konfigurationsfil '{config_path}' hittades inte")
        sys.exit(1)
    except yaml.YAMLError as e:
        print(f"Fel: Kunde inte läsa konfigurationsfil: {e}")
        sys.exit(1)


def run_analysis():
    """Huvudfunktion som kör hela analysprocessen"""
    print("=" * 80)
    print("AUTOMATISK OMVÄRLDSANALYS")
    print("=" * 80)
    print(f"Startad: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()

    # Ladda miljövariabler
    load_dotenv()

    # Ladda konfiguration
    config = load_config()

    # 1. DATAINSAMLING
    print("[1/5] DATAINSAMLING")
    print("-" * 80)

    collector = DataCollector(
        topics=config['topics'],
        max_results=config['search']['max_results_per_topic'],
        language=config['search']['language']
    )

    data = collector.collect_data()
    print(f"✓ Samlat in data för {len(data)} ämnen")
    print()

    # 2. AI-ANALYS
    print("[2/5] AI-ANALYS")
    print("-" * 80)

    analyzer = AIAnalyzer(
        api_key=os.getenv('ANTHROPIC_API_KEY'),
        depth=config['analysis']['depth']
    )

    analysis_results = analyzer.analyze_data(
        data=data,
        include_recommendations=config['analysis']['include_recommendations'],
        include_trends=config['analysis']['include_trends']
    )
    print("✓ Analys genomförd")
    print()

    # 3. PDF-GENERERING
    print("[3/5] PDF-GENERERING")
    print("-" * 80)

    pdf_generator = PDFGenerator(
        title=config['pdf']['title'],
        language=config['pdf']['language']
    )

    timestamp = datetime.now().strftime("%Y-%m-%d")
    pdf_path = f"omvarldsanalys_{timestamp}.pdf"

    pdf_path = pdf_generator.generate_report(
        analysis_data=analysis_results,
        output_path=pdf_path
    )
    print(f"✓ PDF skapad: {pdf_path}")
    print()

    # 4. E-POSTSÄNDNING
    print("[4/5] E-POSTSÄNDNING")
    print("-" * 80)

    email_sender = EmailSender(
        smtp_server=os.getenv('SMTP_SERVER'),
        smtp_port=int(os.getenv('SMTP_PORT', 587)),
        email_from=os.getenv('EMAIL_FROM'),
        email_password=os.getenv('EMAIL_PASSWORD')
    )

    success = email_sender.send_report(
        email_to=os.getenv('EMAIL_TO'),
        pdf_path=pdf_path
    )

    if success:
        print("✓ E-post skickad")
    else:
        print("✗ E-post kunde inte skickas")
    print()

    # 5. SLUTFÖRT
    print("[5/5] SLUTFÖRT")
    print("-" * 80)
    print(f"Omvärldsanalys genomförd: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"PDF-rapport: {pdf_path}")
    print("=" * 80)

    return success


def main():
    """Huvudfunktion med argument-hantering"""
    parser = argparse.ArgumentParser(
        description='Automatisk Omvärldsanalys - AI-driven månatlig rapport'
    )

    parser.add_argument(
        '--daemon',
        action='store_true',
        help='Kör som daemon med schemalagd körning'
    )

    parser.add_argument(
        '--once',
        action='store_true',
        help='Kör analys en gång och avsluta'
    )

    parser.add_argument(
        '--config',
        default='config.yaml',
        help='Sökväg till konfigurationsfil (standard: config.yaml)'
    )

    args = parser.parse_args()

    # Kontrollera att .env finns
    if not os.path.exists('.env'):
        print("VARNING: .env-fil saknas!")
        print("Kopiera .env.example till .env och fyll i dina uppgifter:")
        print("  cp .env.example .env")
        print()

        if not args.daemon:
            response = input("Vill du fortsätta ändå? (ja/nej): ")
            if response.lower() not in ['ja', 'j', 'yes', 'y']:
                sys.exit(1)

    if args.daemon:
        # Kör som daemon med schemaläggning
        print("Startar i daemon-läge...")
        scheduler = AnalysisScheduler(
            analysis_func=run_analysis,
            cron_schedule="0 9 1 * *"
        )
        scheduler.start()
    elif args.once:
        # Kör en gång
        run_analysis()
    else:
        # Interaktivt läge
        print("Välj körläge:")
        print("1. Kör analys nu (en gång)")
        print("2. Starta schemalagd körning (daemon)")
        print("3. Avsluta")
        print()

        choice = input("Välj (1-3): ").strip()

        if choice == '1':
            run_analysis()
        elif choice == '2':
            print("\nStartar schemalagd körning...")
            print("Analysen kommer att köras automatiskt första dagen i varje månad kl 09:00")
            print("Tryck Ctrl+C för att avsluta")
            print()

            scheduler = AnalysisScheduler(
                analysis_func=run_analysis,
                cron_schedule="0 9 1 * *"
            )
            try:
                scheduler.start()
            except KeyboardInterrupt:
                print("\nScheduler avslutad")
        else:
            print("Avslutar...")


if __name__ == "__main__":
    main()
