# TOM-CO-TCG-BOT (`main`)

Branche **légère** : page statique + build npm qui copie `public/index.html` vers `dist/`.

- **Application complète** : branche [`interface`](https://github.com/AnthonyNadjari/TOM-CO-TCG-BOT/tree/interface)
- **Prod de l’app** : [tom-co-tcg-bot.vercel.app](https://tom-co-tcg-bot.vercel.app) (déployée via GitHub Actions sur `interface`)

Cette config évite les déploiements Vercel « annulés » par une étape d’ignore et permet aux checks GitHub de passer.
