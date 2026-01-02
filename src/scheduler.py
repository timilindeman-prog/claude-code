"""
Scheduler Module
Hanterar schemalagd körning av omvärldsanalys
"""

import schedule
import time
from datetime import datetime
import logging


class AnalysisScheduler:
    """Schemalägger och kör omvärldsanalyser"""

    def __init__(self, analysis_func, cron_schedule: str = "0 9 1 * *"):
        """
        Initierar scheduler

        Args:
            analysis_func: Funktionen som ska köras (själva analysen)
            cron_schedule: Cron-liknande schema (t.ex. "0 9 1 * *" för första dagen i månaden kl 09:00)
        """
        self.analysis_func = analysis_func
        self.cron_schedule = cron_schedule

        # Konfigurera logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('analysis_scheduler.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)

    def run_scheduled(self):
        """Kör analysen enligt schema"""
        self.logger.info("Startar schemalagd körning av omvärldsanalys...")

        try:
            self.analysis_func()
            self.logger.info("Analys genomförd framgångsrikt")
        except Exception as e:
            self.logger.error(f"Fel vid schemalagd analys: {e}", exc_info=True)

    def start(self):
        """Startar schedulern och kör kontinuerligt"""
        self.logger.info(f"Scheduler startad. Kör enligt schema: {self.cron_schedule}")

        # Schemalägga för första dagen i månaden kl 09:00
        schedule.every().day.at("09:00").do(self._check_and_run)

        # Kör första gången direkt om det är första dagen i månaden
        if datetime.now().day == 1:
            self.logger.info("Första dagen i månaden - kör analys nu")
            self.run_scheduled()

        # Kontinuerlig loop
        while True:
            schedule.run_pending()
            time.sleep(60)  # Kolla varje minut

    def _check_and_run(self):
        """Kollar om det är dags att köra (första dagen i månaden)"""
        if datetime.now().day == 1:
            self.run_scheduled()

    def run_once(self):
        """Kör analysen en gång (utan schemaläggning)"""
        self.logger.info("Kör analys en gång (manuellt)")
        self.run_scheduled()


def create_systemd_service() -> str:
    """
    Skapar en systemd service-fil för automatisk körning

    Returns:
        Innehållet för en .service-fil
    """
    import sys
    import os

    service_content = f"""[Unit]
Description=Automatisk Omvärldsanalys
After=network.target

[Service]
Type=simple
User={os.getenv('USER', 'user')}
WorkingDirectory={os.getcwd()}
ExecStart={sys.executable} main.py --daemon
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
"""
    return service_content


def create_cron_job() -> str:
    """
    Skapar ett cron-jobb för månatlig körning

    Returns:
        Cron-syntax för månatlig körning
    """
    import sys
    import os

    cron_line = f"0 9 1 * * cd {os.getcwd()} && {sys.executable} main.py >> analysis.log 2>&1"

    return cron_line
