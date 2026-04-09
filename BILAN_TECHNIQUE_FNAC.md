# 📘 Bilan Technique : Automatisation Fnac (Ghost Mode)

Ce document résume les travaux effectués pour stabiliser le bot Fnac contre les protections Akamai et les erreurs de session.

## 1. 🚀 Ce que fait le code aujourd'hui
Le bot est désormais capable de gérer tout le tunnel d'achat de manière autonome :
- **Recherche** intelligente des produits (évite les faux positifs comme les livres sponsorisés).
- **Navigation forcée** vers la page produit (PDP) pour ancrer la session.
- **Ajout au panier visuel** : Le bot clique sur le bouton jaune comme un humain.
- **Checkout automatique** : Il franchit les étapes du panier et de la livraison par clics physiques.
- **Arrêt au Paiement** : Il s'arrête net sur la page de paiement pour vous laisser valider manuellement (sécurité).

## 2. 🛠️ Comment ça fonctionne (Technique)

### Architecture "Ghost Mode" (CDP)
Le bot ne lance pas un navigateur "robotique" classique. Il se connecte à une instance de **Chrome déjà ouverte** (via le port 9222).
- **Avantage** : La Fnac voit votre compte connecté et votre historique réel, ce qui réduit drastiquement les risques de blocage.
- **Profil** : Utilisation du dossier spécial `BotProfile_Clean` pour une session isolée.

### Stratégie "Human-Like" (Clics Physiques)
Nous avons abandonné les requêtes API invisibles (qui causaient l'erreur 404 Lego).
- **Playwright** est utilisé pour chercher les boutons réels dans la page et cliquer dessus.
- **Pop-in Detection** : Le bot attend l'apparition visuelle de la confirmation d'ajout avant de continuer.

### Furtivité et Réseau
- **Stealth JS** : Le bot injecte du code pour masquer sa nature automatisée.
- **IP Résidentielle** : Optimisé pour fonctionner avec le partage de connexion iPhone (Mode Avion pour changer d'IP).

## 3. 🏁 Procédure de lancement stable
1. **IP** : Reset via Mode Avion sur iPhone.
2. **Chrome** : Lancer `./launch_fnac_chrome.sh` dans le Terminal 1.
3. **Login** : Se connecter manuellement sur Fnac.com dans la fenêtre ouverte.
4. **Bot** : Lancer `python3 main.py` dans le Terminal 2.

---
*Document généré le 09/04/2026 pour le projet TOM-CO-TCG-BOT.*
