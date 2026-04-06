# TOM-CO-TCG-BOT (`main`)

## Front statique (Vercel)

Branche **légère** : page statique + build npm qui copie `public/index.html` vers `dist/`.

- **Application complète** : branche [`interface`](https://github.com/AnthonyNadjari/TOM-CO-TCG-BOT/tree/interface)
- **Prod de l’app** : [tom-co-tcg-bot.vercel.app](https://tom-co-tcg-bot.vercel.app) (déployée via GitHub Actions sur `interface`)

Cette config évite les déploiements Vercel « annulés » par une étape d’ignore et permet aux checks GitHub de passer.

## Backend Python (squelette)

Arborescence cible pour l’orchestrateur, les bots, les scrapers, les adaptateurs par site, l’exécution Playwright, les comptes, le paiement, l’infra et la sécurité. Le paquet est défini dans `pyproject.toml` ; les modules sont importables depuis la racine du dépôt (`PYTHONPATH=.` ou `pip install -e .`).

```
orchestrator/   # bot_manager, scheduler, config_parser, state_manager
bots/           # base_bot, worker, session_manager, strategy
scrapers/       # base, api, browser, keyword_engine
sites/          # base (SiteAdapter), pokemon_center/, amazon/, …
execution/      # buyer, playwright_driver, cart, checkout
accounts/       # account_manager, generators, cookie_store
payment/        # vcc_manager, payment_session, providers/
infra/          # proxy_manager, ip_allocator, rate_limiter, server_config
security/       # captcha_solver, fingerprint, humanizer
config/         # settings.yaml, sites.yaml, limits.yaml
utils/          # logger, retry, metrics
tests/
```

L’interface FastAPI / serveur peut vivre dans une autre branche ou un autre dépôt ; ce squelette est prêt à être branché dessus via `orchestrator/config_parser.py` et l’API.

### Tests

```bash
pip install -e ".[dev]"
pytest
```
