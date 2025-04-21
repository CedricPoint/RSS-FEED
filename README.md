# Bot Discord RSS

Un bot Discord qui surveille plusieurs flux RSS et publie les nouveaux articles dans des canaux spécifiques.

## Prérequis

- Python 3.8 ou supérieur
- Un token Discord (à obtenir sur le [Portail des développeurs Discord](https://discord.com/developers/applications))

## Installation

1. Clonez ce dépôt
2. Installez les dépendances :
```bash
pip install -r requirements.txt
```

3. Configurez le fichier `.env` :
```
DISCORD_TOKEN=votre_token_discord
```

4. Configurez les flux RSS dans `feeds_config.json` :
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

## Utilisation

Lancez le bot avec :
```bash
python bot.py
```

## Fonctionnalités

- Vérification périodique des flux RSS
- Publication des nouveaux articles dans les canaux Discord spécifiés
- Évite les doublons même après redémarrage
- Gestion des erreurs et logging
- Interface utilisateur Discord avec embeds

## Configuration systemd

Pour faire fonctionner le bot en permanence avec systemd, créez un fichier `/etc/systemd/system/discord-rss-bot.service` :

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

[Install]
WantedBy=multi-user.target
```

Puis :
```bash
sudo systemctl daemon-reload
sudo systemctl enable discord-rss-bot
sudo systemctl start discord-rss-bot
``` 