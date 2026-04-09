#!/bin/bash

# Script pour lancer Google Chrome sur Mac avec le port de débogage pour le bot.
# Dépendance : Google Chrome doit être installé dans /Applications.

echo "🚀 Préparation du lancement de Chrome en mode 'Fantôme'..."

# On utilise un dossier de profil dédié pour ne pas interférer avec votre navigation perso
# mais tout en restant dans un "vrai" Chrome.
PROFILE_DIR="$HOME/Library/Application Support/Google/Chrome/BotProfile_Clean"
mkdir -p "$PROFILE_DIR"

# Port de débogage standard
PORT=9222

echo "ℹ️  Profil : $PROFILE_DIR"
echo "ℹ️  Port : $PORT"

# Fermer les instances Chrome qui pourraient bloquer si nécessaire ? 
# Non, on va juste lancer une nouvelle instance avec un profil séparé.

"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
  --remote-debugging-port=$PORT \
  --user-data-dir="$PROFILE_DIR" \
  --no-proxy-server \
  --disable-features=IsolateOrigins,site-per-process \
  --no-first-run \
  --no-default-browser-check \
  "https://www.fnac.com" &

echo "✅ Chrome est lancé ! Veuillez résoudre les captchas ou vous connecter si nécessaire dans la fenêtre qui vient de s'ouvrir."
echo "👉 Une fois que vous voyez la page Fnac normalement, vous pouvez lancer 'python3 main.py' dans un autre terminal."
