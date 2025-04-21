import discord
from discord.ext import tasks
import feedparser
import json
import os
import logging
from datetime import datetime
import asyncio
from dotenv import load_dotenv

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
                        embed = discord.Embed(
                            title=entry.title,
                            url=entry.link,
                            description=entry.description if hasattr(entry, 'description') else "Pas de description disponible",
                            color=discord.Color.blue()
                        )
                        
                        if hasattr(entry, 'published'):
                            embed.timestamp = datetime.strptime(entry.published, "%a, %d %b %Y %H:%M:%S %z")
                        
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