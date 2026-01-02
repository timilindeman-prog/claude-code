"""
AI Analyzer Module
Använder Claude AI för att analysera insamlad data
"""

import anthropic
import os
from typing import Dict, List
import json


class AIAnalyzer:
    """Analyserar data med hjälp av Claude AI"""

    def __init__(self, api_key: str = None, depth: str = "standard"):
        self.api_key = api_key or os.getenv("ANTHROPIC_API_KEY")
        self.depth = depth
        self.client = anthropic.Anthropic(api_key=self.api_key)

    def analyze_data(
        self,
        data: Dict[str, List[Dict]],
        include_recommendations: bool = True,
        include_trends: bool = True
    ) -> Dict:
        """
        Analyserar insamlad data och skapar en omfattande rapport

        Args:
            data: Dictionary med ämnen och tillhörande artiklar
            include_recommendations: Om rekommendationer ska inkluderas
            include_trends: Om trendanalys ska inkluderas

        Returns:
            Dictionary med analysresultat
        """
        print("Startar AI-analys av insamlad data...")

        analysis_results = {
            "executive_summary": "",
            "topic_analyses": {},
            "cross_topic_insights": "",
            "trends": [] if include_trends else None,
            "recommendations": [] if include_recommendations else None
        }

        # Analysera varje ämne
        for topic, articles in data.items():
            print(f"Analyserar: {topic}")
            topic_analysis = self._analyze_topic(topic, articles)
            analysis_results["topic_analyses"][topic] = topic_analysis

        # Skapa övergripande sammanfattning
        print("Skapar övergripande sammanfattning...")
        analysis_results["executive_summary"] = self._create_executive_summary(
            analysis_results["topic_analyses"]
        )

        # Hitta kopplingar mellan ämnen
        print("Analyserar kopplingar mellan ämnen...")
        analysis_results["cross_topic_insights"] = self._analyze_cross_topic_insights(
            analysis_results["topic_analyses"]
        )

        # Identifiera trender
        if include_trends:
            print("Identifierar trender...")
            analysis_results["trends"] = self._identify_trends(
                analysis_results["topic_analyses"]
            )

        # Skapa rekommendationer
        if include_recommendations:
            print("Skapar rekommendationer...")
            analysis_results["recommendations"] = self._create_recommendations(
                analysis_results["topic_analyses"]
            )

        return analysis_results

    def _analyze_topic(self, topic: str, articles: List[Dict]) -> Dict:
        """Analyserar ett specifikt ämne"""

        # Förbered artikeldata för analys
        articles_text = "\n\n".join([
            f"Titel: {art['title']}\n"
            f"Källa: {art['source']}\n"
            f"Datum: {art['date']}\n"
            f"Sammanfattning: {art['snippet']}"
            for art in articles
        ])

        prompt = f"""
Analysera följande information om "{topic}" baserat på dessa artiklar och källor:

{articles_text}

Ge en djupgående analys som inkluderar:
1. Huvudsakliga utvecklingar och nyheter
2. Viktiga aktörer och deras agerande
3. Potentiella konsekvenser och implikationer
4. Kort- och långsiktiga perspektiv

Svara på svenska med en strukturerad och insiktsfull analys.
"""

        try:
            message = self.client.messages.create(
                model="claude-sonnet-4-5-20250929",
                max_tokens=2000,
                messages=[{
                    "role": "user",
                    "content": prompt
                }]
            )

            analysis_text = message.content[0].text

            return {
                "topic": topic,
                "analysis": analysis_text,
                "article_count": len(articles),
                "sources": [art["source"] for art in articles]
            }

        except Exception as e:
            print(f"Fel vid analys av {topic}: {e}")
            return {
                "topic": topic,
                "analysis": f"Analys kunde inte genomföras. Fel: {str(e)}",
                "article_count": len(articles),
                "sources": []
            }

    def _create_executive_summary(self, topic_analyses: Dict) -> str:
        """Skapar en övergripande sammanfattning"""

        topics_summary = "\n\n".join([
            f"**{topic}**:\n{analysis['analysis'][:300]}..."
            for topic, analysis in topic_analyses.items()
        ])

        prompt = f"""
Baserat på följande ämnesanalyser, skapa en kortfattad övergripande sammanfattning
(executive summary) på svenska som fångar de viktigaste insikterna och utvecklingarna:

{topics_summary}

Sammanfattningen ska vara koncis (200-300 ord) och ge läsaren en snabb överblick
över de mest betydelsefulla förändringarna och trenderna.
"""

        try:
            message = self.client.messages.create(
                model="claude-sonnet-4-5-20250929",
                max_tokens=1000,
                messages=[{
                    "role": "user",
                    "content": prompt
                }]
            )

            return message.content[0].text

        except Exception as e:
            return f"Kunde inte skapa sammanfattning. Fel: {str(e)}"

    def _analyze_cross_topic_insights(self, topic_analyses: Dict) -> str:
        """Analyserar kopplingar och samband mellan olika ämnen"""

        topics_text = "\n\n".join([
            f"{topic}: {analysis['analysis']}"
            for topic, analysis in topic_analyses.items()
        ])

        prompt = f"""
Analysera följande ämnen och identifiera intressanta kopplingar, samband och
synergier mellan dem:

{topics_text}

Fokusera på:
- Överlappande trender
- Orsak-verkan samband mellan olika områden
- Potentiella synergier eller konflikter
- Systemiska insikter

Svara på svenska.
"""

        try:
            message = self.client.messages.create(
                model="claude-sonnet-4-5-20250929",
                max_tokens=1500,
                messages=[{
                    "role": "user",
                    "content": prompt
                }]
            )

            return message.content[0].text

        except Exception as e:
            return f"Kunde inte analysera kopplingar. Fel: {str(e)}"

    def _identify_trends(self, topic_analyses: Dict) -> List[str]:
        """Identifierar viktiga trender"""

        topics_text = "\n\n".join([
            f"{topic}: {analysis['analysis']}"
            for topic, analysis in topic_analyses.items()
        ])

        prompt = f"""
Baserat på följande analyser, identifiera de 5-7 viktigaste trenderna
som framträder:

{topics_text}

Lista varje trend som en koncis punkt (1-2 meningar per trend).
Svara på svenska.
"""

        try:
            message = self.client.messages.create(
                model="claude-sonnet-4-5-20250929",
                max_tokens=1000,
                messages=[{
                    "role": "user",
                    "content": prompt
                }]
            )

            trends_text = message.content[0].text
            # Dela upp i lista
            trends = [t.strip() for t in trends_text.split('\n') if t.strip() and not t.strip().startswith('#')]

            return trends

        except Exception as e:
            return [f"Kunde inte identifiera trender. Fel: {str(e)}"]

    def _create_recommendations(self, topic_analyses: Dict) -> List[str]:
        """Skapar handlingsrekommendationer"""

        topics_text = "\n\n".join([
            f"{topic}: {analysis['analysis']}"
            for topic, analysis in topic_analyses.items()
        ])

        prompt = f"""
Baserat på dessa analyser, ge 5-7 konkreta rekommendationer för hur man kan
agera på dessa insikter:

{topics_text}

Varje rekommendation ska vara:
- Konkret och handlingsbar
- Relevant för de identifierade trenderna
- Framåtblickande

Svara på svenska.
"""

        try:
            message = self.client.messages.create(
                model="claude-sonnet-4-5-20250929",
                max_tokens=1000,
                messages=[{
                    "role": "user",
                    "content": prompt
                }]
            )

            recommendations_text = message.content[0].text
            # Dela upp i lista
            recommendations = [r.strip() for r in recommendations_text.split('\n') if r.strip() and not r.strip().startswith('#')]

            return recommendations

        except Exception as e:
            return [f"Kunde inte skapa rekommendationer. Fel: {str(e)}"]
