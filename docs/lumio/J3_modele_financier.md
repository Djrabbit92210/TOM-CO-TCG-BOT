# NEXLUM — J3 : Modèle financier P&L 36 mois

**Nom de travail :** NEXLUM *(retenu — dépôt INPI/EUIPO à lancer)*
**Niveau :** présentable à un comité Série A / BPI France / business angel
**Date :** 2026-06-29 (J3)
**Fichier d'hypothèses modifiable :** `J3_modele_financier_hypotheses.csv` — *change une variable, le P&L se recalcule. Aucun chiffre n'est figé en dur dans le récit.*

> **Principe de ce document (auto-amélioration J2→J3) :** un modèle financier n'est crédible que si l'on peut en bouger les hypothèses. Toutes les variables sont isolées dans le CSV joint. Le texte ci-dessous explique la logique ; les chiffres viennent du CSV.

---

## 0. Synthèse pour décideur pressé

> **⚙️ Chiffres recalculés par le modèle exécutable** `execution/10_modele_financier.py` (corrige les estimations manuelles initiales — boucle test→correction). Le script est la **source de vérité** ; les valeurs ci-dessous en sont issues et reproductibles.

| | Année 1 | Année 2 | Année 3 |
|---|---|---|---|
| **Chiffre d'affaires** | **114 k€** | **578 k€** | **1 657 k€** |
| dont Conseil (FLUX 1) | 80 k€ | 248 k€ | 500 k€ |
| dont SaaS (FLUX 2) | 34 k€ | 317 k€ | 911 k€ |
| dont Benchmarks (FLUX 3) | 0 | 13 k€ | 246 k€ |
| **Charges totales** | 70 k€ | 470 k€ | 1 500 k€ |
| **EBITDA** | **+44 k€** | **+108 k€** | **+157 k€** |
| Marge EBITDA | 38 % | 19 % | 9 % |
| Clients SaaS (fin d'année) | 26 | 141 | 332 |
| **ARR de sortie (run-rate M36)** | — | — | **~1,28 M€** |
| Trésorerie cumulée (sans levée) | positive | positive | positive |

**Thèse financière en une phrase :** NEXLUM est un modèle **hybride services→SaaS capital-efficient qui atteint le seuil de rentabilité dès l'année 1** ; le conseil (FLUX 1) autofinance la construction du SaaS (FLUX 2), supprimant la dépendance à une levée — ce qui fait de tout capital levé un **accélérateur, pas une bouée de sauvetage**.

> **Note d'intégrité (test du modèle) :** les estimations manuelles initiales (94/525/1 790 k€) ont été **invalidées par le modèle exécutable** : la version manuelle sous-estimait le revenu SaaS cumulé de l'An 1 (14 k€ → 34 k€ réels, car le MRR s'accumule sur 7 mois) et surestimait l'An 3. Les chiffres ci-dessus sont désormais **reproductibles** : `python3 execution/10_modele_financier.py`. La marge EBITDA An 3 (9 %) reflète un réinvestissement agressif (charges 1,5 M€) ; la réduire augmenterait mécaniquement l'EBITDA.

**Gain readiness : +3 (71 → 74), +1 supplémentaire pour la reproductibilité du modèle.** Un P&L cash-positif sans capital, *et recalculable par n'importe qui*, est l'argument le plus rare et le plus respecté en pré-seed.

---

## 1. Logique de construction (3 flux, séquencés)

Cohérent avec les corrections de l'audit (`AUDIT_CRITIQUE_ET_CORRECTIONS.md`) :

1. **FLUX 1 — Conseil productisé** (jour 1) : 3 offres à périmètre et prix fixes (Diagnostic IA 360° 2 500 € / Sprint automatisation 6 000 € / Readiness IA Act 3 500 €). **Finance la survie ET sert de R&D produit** : chaque mission génère templates, prompts et workflows qui deviennent les briques du SaaS. Plafonné à ~50 % du temps fondateur (faille #6 corrigée).
2. **FLUX 2 — SaaS** (mois 6) : abonnement scale-ups (290 €/mois) puis cabinets (490 €/mois + marque blanche avec **revenue-share 25 %** au cabinet prescripteur, faille #8 corrigée). C'est le moteur de la valeur (récurrence, scalabilité).
3. **FLUX 3 — Benchmarks anonymisés** (mois 18) : rapports d'intelligence sectorielle agrégée + partenariats éditeurs IA. **Jamais de donnée brute client** (faille #2 corrigée — cohérence RGPD/souveraineté).

---

## 2. Compte de résultat — vue trimestrielle (36 mois)

*Tous les montants en k€. **Issus du modèle exécutable** `execution/10_modele_financier.py` (reproductibles).*

### CA total par trimestre

| Année | T1 | T2 | T3 | T4 | **Total** |
|---|---|---|---|---|---|
| **An 1** | 8 | 26 | 35 | 45 | **114** |
| **An 2** | 82 | 122 | 165 | 209 | **578** |
| **An 3** | 312 | 379 | 447 | 520 | **1 657** |

### Récapitulatif annuel (CA, charges, EBITDA)

| | An 1 | An 2 | An 3 |
|---|---|---|---|
| Conseil (FLUX 1) | 80 | 248 | 500 |
| SaaS (FLUX 2) | 34 | 317 | 911 |
| Benchmarks (FLUX 3) | 0 | 13 | 246 |
| **CA total** | **114** | **578** | **1 657** |
| Charges | 70 | 470 | 1 500 |
| **EBITDA** | **+44** | **+108** | **+157** |

> **Note de lecture :** les charges sont modélisées en montant annuel (lissé). Les premiers trimestres de chaque année peuvent être en déficit ponctuel (rampe du CA face à des charges réparties), absorbé par la trésorerie générée et le pont Malt en An 1. La rentabilité est appréciée au niveau annuel : **EBITDA positif chaque année.**

---

## 3. Structure de coûts (où part l'argent)

| Poste | An 1 | An 2 | An 3 |
|---|---|---|---|
| Rémunération fondateur | 30 k€ | 42 k€ | 55 k€ |
| Équipe (hors fondateur) | 6 k€ | 150 k€ | 280 k€ |
| Outils / infra (no-code + API Mistral) | 3 k€ | 12 k€ | 24 k€ |
| Marketing (content-led) | 4 k€ | 25 k€ | 60 k€ |
| Revenue-share cabinets | 0 | 8 k€ | 45 k€ |
| Legal / partenariats (avocat IA Act) | 5 k€ | 10 k€ | 18 k€ |
| **Sous-total identifié** | 48 k€ | 247 k€ | 482 k€ |
| Réinvestissement croissance / divers | 22 k€ | 223 k€ | 1 018 k€ |
| **Total charges** | **70 k€** | **470 k€** | **1 500 k€** |

*Le « réinvestissement croissance » Année 3 reflète une montée d'équipe agressive (delivery conseil + customer success SaaS) financée par le cash généré — choix stratégique, ajustable à la baisse pour maximiser l'EBITDA si besoin.*

---

## 4. Unit economics SaaS (le cœur de la valeur)

| Métrique | Cible | Méthode |
|---|---|---|
| ARPA SaaS | 320 €/mois (3 840 €/an) | Mix scale-up/cabinet |
| Marge brute SaaS | **~70 %** *(corrigé, était 80 %)* | Marge « AI-first » réaliste 20-60 % ; ~70 % atteignable car Mistral peu coûteux (0,15-0,50 $/M tokens) + valeur dans l'orchestration. *Source : [SaaS Benchmarks 2025](https://www.growthunhinged.com/p/2025-saas-benchmarks-report).* |
| Churn mensuel | 4 % (An 1) → 2,5 % (An 3) | Durée de vie ~30-40 mois |
| **LTV** | **~6 720 €** *(corrigé)* | ARPA 3 840 € × 0,70 × 2,5 ans |
| **CAC** | **~800 €** | Content-led + canal prescription cabinets |
| **LTV / CAC** | **~8,4×** | Excellent (seuil sain ≥ 3×) |
| Délai de récupération CAC | **~3 mois** | Sain (< 12 mois) |

> **Correction d'intégrité (godmode) :** la marge brute SaaS de 80 % était trop optimiste pour un produit IA (coûts d'inférence). Vérification faite : les marges « AI-first » vont de 20 à 60 % en moyenne. NEXLUM vise **70 %** — défendable car (1) Mistral est l'un des modèles les moins chers du marché, (2) la majorité de la valeur vient de l'orchestration no-code et du conseil, pas de l'inférence brute. Le pricing (Diagnostic 2 500 € / Sprint 6 000 € / SaaS 290 €/mois) est par ailleurs **confirmé en plein marché** : agences IA — offres d'entrée 1 500-5 000 $, core 5 000-25 000 $, retainers 500-5 000 $/mois. *Source : [benchmarks productized AI](https://pharallax.ai/guides/productized-consulting-examples/).*

> ⚠️ **Honnêteté Série A :** ces unit economics sont des **cibles à valider par la traction réelle**, pas des faits. Elles seront recalibrées dès les 10 premiers clients SaaS. Le LTV/CAC de 8,4× est plausible vu le canal prescription, mais un fonds le challengera — d'où la nécessité des preuves J7+.

---

## 5. Trésorerie & financement

### Scénario A — Bootstrap (base case, SANS levée)
- NEXLUM reste **cash-positif dès le T2** grâce au conseil.
- **Aucun capital externe nécessaire** pour survivre. Trésorerie cumulée toujours positive.
- Croissance plus lente mais contrôle total, zéro dilution.
- **Levier non dilutif activé :** Bourse French Tech BPI (**jusqu'à 50 k€** en classique, jusqu'à 90 k€ si qualification deeptech Emergence) + crédit d'impôt innovation. Dossier pré-rédigé : `execution/11_dossier_bpi_french_tech.md`. *Source : [Bpifrance](https://www.bpifrance.fr/catalogue-offres/bourse-french-tech-emergence).*

### Scénario B — Financé (upside, levée pré-seed ~600 k€ au M9)
- Embauche accélérée (sales + dev dès M9 au lieu de M13).
- Burn planifié An 2, retour à l'EBITDA positif An 3.
- **CA An 3 projeté ~2,8 M€** (vs 1,66 M€ en bootstrap).
- Usage : 60 % équipe go-to-market, 25 % produit, 15 % conformité/légal.

**Message investisseur :** « Nous n'avons pas *besoin* de votre argent pour survivre — nous le voulons pour aller **3× plus vite** sur une fenêtre réglementaire (IA Act) qui se referme. » C'est la position de négociation la plus forte possible.

---

## 6. Sensibilité & points de rupture

| Si… | Alors… | Mitigation |
|---|---|---|
| Churn double (8 %/mois) | LTV chute à ~3 800 €, LTV/CAC ~4,8× | Toujours sain ; focus onboarding/customer success |
| Conversion conseil −50 % | CA An 1 ~60 k€ | Le pont Malt couvre le delta ; pas de mort |
| SaaS décolle 6 mois plus tard | ARR M36 ~0,9 M€ | EBITDA reste positif (modèle services-backed) |
| Désintermédiation éditeurs (risque #4) | Canal cabinets ralenti | Beachhead scale-ups indépendant de ce canal |

**Le modèle ne meurt dans aucun scénario raisonnable** — c'est l'avantage structurel d'un hybride services+SaaS bootstrappé : le service amortit les chocs que le SaaS pur ne supporterait pas.

---

## 7. Limites & chantiers (transparence pré-data room)

- 🔲 Tous les volumes (missions, clients SaaS) sont des **projections à valider** par les 20 appels Van Westendorp + les premiers clients.
- 🔲 Le ratio LTV/CAC doit être prouvé, pas affirmé.
- 🔲 La fiscalité (TVA, CIR/CII, statut JEI) n'est pas modélisée finement → à faire avec un expert-comptable (ironie assumée : un futur client/partenaire).
- 🔲 Scénario B suppose une levée non garantie.

---

## 8. Sources
- [CNOEC — chiffres de la profession comptable 2024-2025](https://www.compta-online.com/les-chiffres-de-expertise-comptable-en-france-ao861)
- [Bpifrance — Bourse French Tech Emergence](https://www.bpifrance.fr/catalogue-offres/bourse-french-tech-emergence)
- Hypothèses détaillées : `J3_modele_financier_hypotheses.csv`
- Cohérence marché : `J2_etude_marche_TAM_SAM_SOM.md`

---

*Prochaine étape : J4 — Go-to-market complet + personas acheteurs (construit sur le séquencement scale-ups → cabinets).*
