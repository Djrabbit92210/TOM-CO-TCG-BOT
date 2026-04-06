# TOM-CO-TCG-BOT

## Branches

**`main`** — point d’ancrage minimal (page statique légère + squelette Python backend). Ce n’est pas l’app produit.

**`interface`** — **TCG Scalper Pro** : appli développée et déployée depuis cette branche.

| | Lien |
|---|------|
| **App en production** | [tom-co-tcg-bot.vercel.app](https://tom-co-tcg-bot.vercel.app) |
| **Code (interface)** | [GitHub — branche `interface`](https://github.com/AnthonyNadjari/TOM-CO-TCG-BOT/tree/interface) |

### Déploiement Vercel

- Un workflow GitHub Actions sur **`interface`** déploie en production à chaque push : [`.github/workflows/vercel-deploy-interface.yml`](https://github.com/AnthonyNadjari/TOM-CO-TCG-BOT/blob/interface/.github/workflows/vercel-deploy-interface.yml) (secrets `VERCEL_TOKEN`, `VERCEL_ORG_ID`, `VERCEL_PROJECT_ID`).
- **Builds Git ignorés pour `main`** : le projet Vercel est configuré avec une *Ignored Build Step* qui saute les déploiements déclenchés par des commits sur **`main`** (la prod n’est plus écrasée par la landing minimale). Les mises à jour prod viennent du workflow sur **`interface`**.
- Optionnel : dans **Project → Settings → Environments**, vous pouvez aussi définir la **Production branch** sur **`interface`** pour l’aligner avec le flux réel.

---

## Backend Python (sur `main`)

Squelette : orchestrateur, bots, scrapers, adaptateurs par site, exécution Playwright, comptes, paiement, infra, sécurité. Paquet : `pyproject.toml` (`pip install -e .` ou `PYTHONPATH=.`).

```
orchestrator/   # bot_manager, scheduler, config_parser, state_manager
bots/           # base_bot, worker, session_manager, strategy
scrapers/       # base, api, browser, keyword_engine, product_match
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

### Tests

```bash
pip install -e ".[dev]"
pytest
```
