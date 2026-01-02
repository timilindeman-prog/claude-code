"""
Data Collector Module
Samlar in data från olika källor för omvärldsanalys
"""

import requests
from bs4 import BeautifulSoup
from typing import List, Dict
import time


class DataCollector:
    """Samlar in data från webben baserat på angivna ämnen"""

    def __init__(self, topics: List[str], max_results: int = 10, language: str = "sv"):
        self.topics = topics
        self.max_results = max_results
        self.language = language

    def collect_data(self) -> Dict[str, List[Dict]]:
        """
        Samlar in data för alla ämnen

        Returns:
            Dictionary med ämne som nyckel och lista av artiklar som värde
        """
        all_data = {}

        for topic in self.topics:
            print(f"Samlar in data för: {topic}")
            articles = self._search_topic(topic)
            all_data[topic] = articles
            time.sleep(1)  # Vara artig mot servrar

        return all_data

    def _search_topic(self, topic: str) -> List[Dict]:
        """
        Söker efter artiklar om ett specifikt ämne

        Args:
            topic: Ämnet att söka efter

        Returns:
            Lista med artikeldata
        """
        articles = []

        # Simulerad sökning - i produktion skulle detta använda riktiga API:er
        # som Google News API, NewsAPI, eller specifika svenska nyhetskällor

        # Exempel på svenska nyhetskällor att scrapa
        sources = [
            {
                "title": f"Senaste utvecklingen inom {topic}",
                "url": f"https://example.com/{topic.lower().replace(' ', '-')}",
                "snippet": f"Omfattande rapport om aktuella trender och utveckling inom {topic}. "
                          f"Experter menar att detta område kommer att vara avgörande framöver.",
                "date": "2025-01-02",
                "source": "Exempel Tidning"
            },
            {
                "title": f"Analys: Hur {topic} påverkar framtiden",
                "url": f"https://example.com/analys-{topic.lower().replace(' ', '-')}",
                "snippet": f"En djupgående analys av hur {topic} utvecklas och vilka konsekvenser "
                          f"detta kan få för samhället och näringslivet.",
                "date": "2025-01-01",
                "source": "Tech News Sverige"
            },
            {
                "title": f"Experternas syn på {topic}",
                "url": f"https://example.com/expert-{topic.lower().replace(' ', '-')}",
                "snippet": f"Ledande experter inom {topic} ger sina perspektiv på aktuell utveckling "
                          f"och vad vi kan förvänta oss framöver.",
                "date": "2024-12-30",
                "source": "Bransch Magasinet"
            }
        ]

        # Lägg till artiklar upp till max_results
        articles.extend(sources[:self.max_results])

        return articles

    def search_web(self, query: str) -> List[Dict]:
        """
        Söker på webben efter en specifik fråga

        Args:
            query: Sökfråga

        Returns:
            Lista med sökresultat
        """
        # I produktion: implementera riktig webbsökning via API
        # För nu returnerar vi exempel-data
        return self._search_topic(query)
