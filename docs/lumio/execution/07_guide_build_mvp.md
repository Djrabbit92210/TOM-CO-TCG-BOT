# Guide de build MVP — exécutable au lancement (no-code, souverain)

**But :** un MVP démontrable et vendable, buildable par 1 personne, < 200 €/mois, **données en Europe**.
**Principe :** mono-modèle **Mistral** (souveraineté + coût), orchestration no-code, le « model-agnostic » est une roadmap (faille #5).

---

## 1. Stack technique recommandé (souverain-compatible)

| Brique | Outil recommandé | Alternative souveraine | Coût/mois |
|---|---|---|---|
| LLM | **Mistral La Plateforme** (Small 4 par défaut, Large 3 si besoin) | — (déjà européen) | usage (voir §3) |
| Orchestration / automatisation | **n8n** (open-source, auto-hébergeable en UE) | Make.com (UE possible) | 0-50 € |
| Formulaires / diagnostic | **Tally** ou Typeform | Tally (UE) | 0-29 € |
| Dashboard client | **Notion** | Baserow (open-source UE) | 0-20 € |
| Base de données | **Supabase** (hébergement UE possible) | — | 0-25 € |
| Site / landing | **Framer** ou Webflow | — | 0-30 € |
| **Total** | | | **0-180 €/mois** |

> **Choix souveraineté :** privilégier **n8n auto-hébergé + Supabase région UE + Mistral** = chaîne 100 % traitement européen, argument RGPD/souveraineté **réel** (pas marketing). C'est le différenciateur n°1 face à un stack Zapier+OpenAI.

---

## 2. Les 3 produits MVP (buildables en 30 jours)

### Produit 1 — Diagnostic IA 360° (offre SCAN)
- **Flux :** Tally (questionnaire 15 questions) → webhook n8n → prompt Mistral (analyse + scoring ROI + classification IA Act) → génération PDF → email automatique au prospect.
- **Livrable client :** rapport de 4-6 pages, 3 automatisations recommandées, niveau de risque IA Act.
- **Build :** 3-4 jours. **Vendable 2 500 €.**

### Produit 2 — Sprint d'automatisation (offre SHIP)
- **Bibliothèque de workflows n8n réutilisables**, ex :
  - Rédaction assistée (emails, comptes-rendus, courriers) via Mistral
  - Analyse documentaire (résumé/extraction de contrats, factures, rapports)
  - Reporting automatisé (synthèse de données → tableau de bord)
- **Build :** templates créés une fois, adaptés par client. **Vendable 6 000 €.**

### Produit 3 — Dashboard & abonnement (offre SCALE)
- **Flux :** Notion/Baserow + n8n maintiennent les workflows en production, suivi des usages et du ROI (heures gagnées).
- **Récurrence :** 290 €/mois (scale-up) / 490 €/mois (cabinet marque blanche).

---

## 3. Économie unitaire d'inférence (pourquoi la marge tient)

Coût Mistral réel (vérifié) : **Small 4 = 0,15 $/M input, 0,60 $/M output** ; Large 3 = 0,50/1,50 $.

**Exemple : un client SaaS génère ~2 M tokens/mois** (rédaction + analyse) en Small 4 :
- Coût ≈ (1 M × 0,15) + (1 M × 0,60) ≈ **0,75 $/mois** d'inférence.
- ARPA 290 € → **coût d'inférence < 0,3 % du revenu.**
- Même avec un usage 10× plus lourd ou Mistral Large : coût < 8 €/client/mois.

→ **La marge brute de 70 % est prudente** : la majorité du coût n'est pas l'IA mais l'hébergement, le support et l'amortissement du build. Mistral rend l'inférence quasi gratuite à l'échelle PME.

---

## 4. Roadmap technique (honnête)

| Phase | Quand | Quoi |
|---|---|---|
| MVP | Mois 0-1 | 3 produits no-code, Mistral mono-modèle |
| V1 | Mois 3-6 | Industrialisation workflows, dashboard usage/ROI |
| V2 | Mois 9-12 | Multi-tenant (marque blanche cabinets), Supabase |
| V3 | Mois 12+ | **Couche model-agnostic** (Claude/GPT en fallback) — *l'argument « indépendance GAFAM » devient réel ici, pas avant* |

---

## 5. Checklist de mise en production
- [ ] Compte Mistral La Plateforme (clé API, région UE)
- [ ] n8n auto-hébergé (VPS UE type Scaleway/OVH) ou Make UE
- [ ] Supabase projet région Europe
- [ ] Tally + Notion configurés
- [ ] 1 workflow de chaque type testé de bout en bout
- [ ] DPA (data processing agreement) signé avec chaque sous-traitant (RGPD — voir socle juridique)
- [ ] Démo enregistrée (vidéo 3 min) pour la prospection

---

## 6. Sources
- [Mistral pricing](https://mistral.ai/pricing/) · [SaaS Benchmarks 2025](https://www.growthunhinged.com/p/2025-saas-benchmarks-report)
- Choix de stack : n8n / Supabase / Scaleway / OVH (hébergeurs souverains UE)
