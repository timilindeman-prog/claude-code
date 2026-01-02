#!/usr/bin/env python3
"""
Webbgränssnitt för Omvärldsanalyssystemet
Flask-baserad webbapplikation
"""

from flask import Flask, render_template, request, jsonify, send_file, redirect, url_for
import os
import sys
import yaml
import json
from datetime import datetime
from pathlib import Path
import threading
from dotenv import load_dotenv

# Lägg till parent directory i path för att kunna importera moduler
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.data_collector import DataCollector
from src.analyzer import AIAnalyzer
from src.pdf_generator import PDFGenerator
from src.email_sender import EmailSender

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-change-this'
app.config['UPLOAD_FOLDER'] = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Global status
analysis_status = {
    'running': False,
    'progress': 0,
    'message': 'Redo att starta',
    'current_pdf': None,
    'history': []
}

load_dotenv(os.path.join(app.config['UPLOAD_FOLDER'], '.env'))


def load_config():
    """Läser konfigurationsfil"""
    config_path = os.path.join(app.config['UPLOAD_FOLDER'], 'config.yaml')
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        return None


def save_config(config):
    """Sparar konfiguration"""
    config_path = os.path.join(app.config['UPLOAD_FOLDER'], 'config.yaml')
    with open(config_path, 'w', encoding='utf-8') as f:
        yaml.dump(config, f, allow_unicode=True, default_flow_style=False)


def update_status(message, progress):
    """Uppdaterar analysstatus"""
    analysis_status['message'] = message
    analysis_status['progress'] = progress


def run_analysis_background():
    """Kör analys i bakgrunden"""
    try:
        analysis_status['running'] = True
        update_status('Startar analys...', 0)

        # Ladda konfiguration
        config = load_config()

        # Datainsamling
        update_status('Samlar in data...', 20)
        collector = DataCollector(
            topics=config['topics'],
            max_results=config['search']['max_results_per_topic'],
            language=config['search']['language']
        )
        data = collector.collect_data()

        # AI-analys
        update_status('Kör AI-analys...', 40)
        analyzer = AIAnalyzer(
            api_key=os.getenv('ANTHROPIC_API_KEY'),
            depth=config['analysis']['depth']
        )
        analysis_results = analyzer.analyze_data(
            data=data,
            include_recommendations=config['analysis']['include_recommendations'],
            include_trends=config['analysis']['include_trends']
        )

        # PDF-generering
        update_status('Genererar PDF...', 70)
        pdf_generator = PDFGenerator(
            title=config['pdf']['title'],
            language=config['pdf']['language']
        )

        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        pdf_filename = f"omvarldsanalys_{timestamp}.pdf"
        pdf_path = os.path.join(app.config['UPLOAD_FOLDER'], pdf_filename)

        pdf_generator.generate_report(
            analysis_data=analysis_results,
            output_path=pdf_path
        )

        # E-post
        update_status('Skickar e-post...', 90)
        if os.getenv('EMAIL_TO') and os.getenv('SMTP_SERVER'):
            email_sender = EmailSender(
                smtp_server=os.getenv('SMTP_SERVER'),
                smtp_port=int(os.getenv('SMTP_PORT', 587)),
                email_from=os.getenv('EMAIL_FROM'),
                email_password=os.getenv('EMAIL_PASSWORD')
            )
            email_sender.send_report(
                email_to=os.getenv('EMAIL_TO'),
                pdf_path=pdf_path
            )

        # Klart
        update_status('Analys slutförd!', 100)
        analysis_status['current_pdf'] = pdf_filename

        # Lägg till i historik
        analysis_status['history'].insert(0, {
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'pdf': pdf_filename,
            'topics': len(config['topics'])
        })

        # Behåll max 10 i historik
        analysis_status['history'] = analysis_status['history'][:10]

    except Exception as e:
        update_status(f'Fel: {str(e)}', 0)
    finally:
        analysis_status['running'] = False


@app.route('/')
def index():
    """Startsida"""
    config = load_config()
    return render_template('index.html', config=config, status=analysis_status)


@app.route('/config')
def config_page():
    """Konfigurationssida"""
    config = load_config()
    env_status = {
        'anthropic_key': bool(os.getenv('ANTHROPIC_API_KEY')),
        'email_configured': bool(os.getenv('EMAIL_TO'))
    }
    return render_template('config.html', config=config, env_status=env_status)


@app.route('/api/config', methods=['GET', 'POST'])
def api_config():
    """API för konfiguration"""
    if request.method == 'POST':
        config = request.json
        save_config(config)
        return jsonify({'success': True})
    else:
        config = load_config()
        return jsonify(config)


@app.route('/api/start-analysis', methods=['POST'])
def start_analysis():
    """Starta analys"""
    if analysis_status['running']:
        return jsonify({'error': 'Analys körs redan'}), 400

    # Starta i bakgrundstråd
    thread = threading.Thread(target=run_analysis_background)
    thread.daemon = True
    thread.start()

    return jsonify({'success': True})


@app.route('/api/status')
def get_status():
    """Hämta analysstatus"""
    return jsonify(analysis_status)


@app.route('/api/download/<filename>')
def download_pdf(filename):
    """Ladda ner PDF"""
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    if os.path.exists(filepath):
        return send_file(filepath, as_attachment=True)
    return jsonify({'error': 'Fil hittades inte'}), 404


@app.route('/api/reports')
def list_reports():
    """Lista alla PDF-rapporter"""
    reports_dir = app.config['UPLOAD_FOLDER']
    pdf_files = [f for f in os.listdir(reports_dir) if f.endswith('.pdf')]

    reports = []
    for pdf in sorted(pdf_files, reverse=True):
        filepath = os.path.join(reports_dir, pdf)
        stat = os.stat(filepath)
        reports.append({
            'filename': pdf,
            'size': stat.st_size,
            'created': datetime.fromtimestamp(stat.st_mtime).strftime('%Y-%m-%d %H:%M:%S')
        })

    return jsonify(reports)


if __name__ == '__main__':
    print("\n" + "="*80)
    print("🌐 OMVÄRLDSANALYS - WEBBGRÄNSSNITT")
    print("="*80)
    print(f"\n📍 Öppna: http://localhost:5000")
    print("\n💡 Tips:")
    print("  - Konfigurera ämnen och inställningar via webbgränssnittet")
    print("  - Starta analyser med ett knapptryck")
    print("  - Ladda ner genererade PDF-rapporter")
    print(f"\n⏹  Tryck Ctrl+C för att stoppa\n")
    print("="*80 + "\n")

    app.run(debug=True, host='0.0.0.0', port=5000)
