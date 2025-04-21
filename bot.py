import discord
from discord.ext import tasks
import feedparser
import json
import os
import logging
from datetime import datetime
import asyncio
from dotenv import load_dotenv
import re

# Configuration du logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('rss_bot.log'),
        logging.StreamHandler()
    ]
)

# Chargement des variables d'environnement
load_dotenv()

class RSSBot(discord.Client):
    def __init__(self):
        super().__init__(intents=discord.Intents.default())
        self.config = self.load_config()
        self.processed_entries = self.load_processed_entries()
        self.check_feeds.start()

    def load_config(self):
        try:
            with open('feeds_config.json', 'r') as f:
                return json.load(f)
        except Exception as e:
            logging.error(f"Erreur lors du chargement de la configuration: {e}")
            return {"rss_feeds": [], "check_interval": 300}

    def load_processed_entries(self):
        try:
            with open('processed_entries.json', 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {}

    def save_processed_entries(self):
        try:
            with open('processed_entries.json', 'w') as f:
                json.dump(self.processed_entries, f)
        except Exception as e:
            logging.error(f"Erreur lors de la sauvegarde des entrées traitées: {e}")

    def truncate_description(self, description, max_length=1024):
        """Tronque la description si elle dépasse la limite de Discord"""
        if len(description) > max_length:
            return description[:max_length-3] + "..."
        return description

    def clean_html(self, text):
        """Nettoie le HTML de la description"""
        if not text:
            return ""
        # Supprime les balises HTML
        clean = re.sub('<[^<]+?>', '', text)
        # Remplace les entités HTML
        clean = clean.replace('&nbsp;', ' ')
        clean = clean.replace('&amp;', '&')
        clean = clean.replace('&lt;', '<')
        clean = clean.replace('&gt;', '>')
        clean = clean.replace('&quot;', '"')
        return clean.strip()

    def extract_image_url(self, entry):
        """Extrait l'URL de l'image principale de l'entrée"""
        # Vérifie les balises media:content
        if hasattr(entry, 'media_content'):
            for media in entry.media_content:
                if media.get('type', '').startswith('image/'):
                    return media.get('url')
        
        # Vérifie les balises enclosure
        if hasattr(entry, 'enclosures'):
            for enclosure in entry.enclosures:
                if enclosure.get('type', '').startswith('image/'):
                    return enclosure.get('href')
        
        # Vérifie les balises image dans le contenu
        if hasattr(entry, 'content'):
            img_match = re.search(r'<img[^>]+src="([^">]+)"', entry.content[0].value)
            if img_match:
                return img_match.group(1)
        
        return None

    async def setup_hook(self):
        logging.info("Bot en cours de démarrage...")

    @tasks.loop(seconds=300)
    async def check_feeds(self):
        logging.info("Vérification des flux RSS...")
        for feed in self.config["rss_feeds"]:
            try:
                feed_data = feedparser.parse(feed["url"])
                channel = self.get_channel(feed["channel_id"])
                
                if not channel:
                    logging.error(f"Canal Discord introuvable: {feed['channel_id']}")
                    continue

                if feed["url"] not in self.processed_entries:
                    self.processed_entries[feed["url"]] = []

                for entry in feed_data.entries:
                    if entry.link not in self.processed_entries[feed["url"]]:
                        # Prépare la description
                        description = ""
                        if hasattr(entry, 'description'):
                            description = self.clean_html(entry.description)
                        elif hasattr(entry, 'summary'):
                            description = self.clean_html(entry.summary)
                        elif hasattr(entry, 'content'):
                            description = self.clean_html(entry.content[0].value)
                        
                        # Crée l'embed
                        embed = discord.Embed(
                            title=entry.title,
                            url=entry.link,
                            description=self.truncate_description(description),
                            color=discord.Color.blue()
                        )
                        
                        # Ajoute l'image si disponible
                        image_url = self.extract_image_url(entry)
                        if image_url:
                            embed.set_image(url=image_url)
                        
                        # Ajoute la date de publication
                        if hasattr(entry, 'published'):
                            try:
                                embed.timestamp = datetime.strptime(entry.published, "%a, %d %b %Y %H:%M:%S %z")
                            except ValueError:
                                try:
                                    embed.timestamp = datetime.strptime(entry.published, "%Y-%m-%dT%H:%M:%S%z")
                                except ValueError:
                                    logging.warning(f"Format de date non reconnu: {entry.published}")
                        
                        # Ajoute l'auteur si disponible
                        if hasattr(entry, 'author'):
                            embed.set_footer(text=f"Auteur: {entry.author}")
                        
                        await channel.send(embed=embed)
                        self.processed_entries[feed["url"]].append(entry.link)
                        self.save_processed_entries()

            except Exception as e:
                logging.error(f"Erreur lors du traitement du flux {feed['url']}: {e}")

    @check_feeds.before_loop
    async def before_check_feeds(self):
        await self.wait_until_ready()

    async def on_ready(self):
        logging.info(f'Bot connecté en tant que {self.user}')
        logging.info(f'Vérification des flux toutes les {self.config["check_interval"]} secondes')

    async def on_error(self, event, *args, **kwargs):
        logging.error(f"Erreur dans l'événement {event}: {args} {kwargs}")

def main():
    client = RSSBot()
    client.run(os.getenv('DISCORD_TOKEN'))

if __name__ == "__main__":
    main() 