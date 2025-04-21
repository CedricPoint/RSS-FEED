# 🤖 Bot Discord RSS

Un bot Discord puissant qui surveille plusieurs flux RSS et publie automatiquement les nouveaux articles dans des canaux spécifiques. Parfait pour suivre l'actualité, les blogs, ou tout autre contenu RSS.

## ✨ Fonctionnalités

- 🔄 Vérification périodique des flux RSS (configurable)
- 📢 Publication automatique dans les canaux Discord dédiés
- 🖼️ Support des images (extraction depuis les flux RSS)
- 📝 Nettoyage automatique du HTML
- 📅 Affichage des dates de publication
- 👤 Affichage des auteurs
- 🔒 Évite les doublons même après redémarrage
- 📊 Logging complet des activités
- 🛡️ Gestion robuste des erreurs

## 📋 Prérequis

- Python 3.8 ou supérieur
- Un serveur Discord
- Un token de bot Discord (à obtenir sur le [Portail des développeurs Discord](https://discord.com/developers/applications))
- Les permissions suivantes pour le bot :
  - `View Channels`
  - `Send Messages`
  - `Embed Links`
  - `Attach Files`

## 🚀 Installation

1. **Clonez le dépôt** :
```bash
git clone https://github.com/votre-utilisateur/discord-rss-bot.git
cd discord-rss-bot
```

2. **Installez les dépendances** :
```bash
pip install -r requirements.txt
```

3. **Configurez le token Discord** :
Créez un fichier `.env` à la racine du projet :
```env
DISCORD_TOKEN=votre_token_discord
```

4. **Configurez les flux RSS** :
Modifiez le fichier `feeds_config.json` :
```json
{
  "rss_feeds": [
    {
      "url": "https://exemple.com/rss.xml",
      "channel_id": 123456789012345678
    }
  ],
  "check_interval": 300
}
```

## ⚙️ Configuration

### Structure de `feeds_config.json`

```json
{
  "rss_feeds": [
    {
      "url": "URL_DU_FLUX_RSS",
      "channel_id": ID_DU_CANAL_DISCORD
    }
  ],
  "check_interval": 300
}
```

- `url` : L'URL du flux RSS à surveiller
- `channel_id` : L'ID du canal Discord où publier les articles
- `check_interval` : Intervalle de vérification en secondes (par défaut : 300)

### Format des messages

Les articles sont publiés sous forme d'embeds Discord avec :
- Titre de l'article
- Lien vers l'article
- Description (nettoyée du HTML)
- Image principale (si disponible)
- Date de publication
- Nom de l'auteur (si disponible)

## 🏃‍♂️ Lancement

### Mode développement

```bash
python bot.py
```

### Production avec systemd

1. Créez le fichier de service :
```bash
sudo nano /etc/systemd/system/discord-rss-bot.service
```

2. Ajoutez la configuration suivante :
```ini
[Unit]
Description=Bot Discord RSS
After=network.target

[Service]
Type=simple
User=votre_utilisateur
WorkingDirectory=/chemin/vers/votre/bot
ExecStart=/usr/bin/python3 bot.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

3. Activez et démarrez le service :
```bash
sudo systemctl daemon-reload
sudo systemctl enable discord-rss-bot
sudo systemctl start discord-rss-bot
```

## 📝 Logs

Les logs sont enregistrés dans `rss_bot.log` avec le format suivant :
```
2024-01-01 12:00:00 - INFO - Bot en cours de démarrage...
2024-01-01 12:00:01 - INFO - Bot connecté en tant que BotName#1234
2024-01-01 12:00:01 - INFO - Vérification des flux toutes les 300 secondes
```

## 🛠️ Maintenance

### Vérification du statut

```bash
sudo systemctl status discord-rss-bot
```

### Redémarrage

```bash
sudo systemctl restart discord-rss-bot
```

### Arrêt

```bash
sudo systemctl stop discord-rss-bot
```

## 🔍 Dépannage

### Problèmes courants

1. **Le bot ne démarre pas**
   - Vérifiez le token Discord
   - Vérifiez les permissions du bot
   - Consultez les logs

2. **Les articles ne sont pas publiés**
   - Vérifiez les IDs des canaux
   - Vérifiez les URLs des flux RSS
   - Vérifiez les permissions du bot dans les canaux

3. **Erreurs de parsing**
   - Vérifiez le format des dates dans les flux RSS
   - Vérifiez la structure des flux RSS

## 📚 Ressources utiles

- [Documentation Discord.py](https://discordpy.readthedocs.io/)
- [Documentation Feedparser](https://pythonhosted.org/feedparser/)
- [Guide de création de bot Discord](https://discordpy.readthedocs.io/en/stable/discord.html)

## 🤝 Contribution

Les contributions sont les bienvenues ! N'hésitez pas à :
1. Fork le projet
2. Créer une branche (`git checkout -b feature/AmazingFeature`)
3. Commit vos changements (`git commit -m 'Add some AmazingFeature'`)
4. Push vers la branche (`git push origin feature/AmazingFeature`)
5. Ouvrir une Pull Request

## 🙏 Remerciements

- [discord.py](https://github.com/Rapptz/discord.py) - La bibliothèque Discord pour Python
- [feedparser](https://github.com/kurtmckee/feedparser) - Le parseur RSS/Atom
- [python-dotenv](https://github.com/theskumar/python-dotenv) - Gestion des variables d'environnement 