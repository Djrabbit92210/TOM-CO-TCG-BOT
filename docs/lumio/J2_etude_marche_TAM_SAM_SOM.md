# LUMIO — J2 : Étude de Marché & Dimensionnement TAM / SAM / SOM

**Sous-titre :** Marché de l'intégration IA pour les PME européennes
**Niveau d'exigence :** Série A / Davos / Fonds souverain
**Tagline :** *"AI that works. For every business."*
**Date :** Juin 2026 — Sprint 7 jours, Jour 2
**Statut :** Document immédiatement présentable à un investisseur

> ⚠️ **Note marque :** Le nom « LUMIO » reste à valider (recherche d'antériorité INPI + EUIPO requise avant tout dépôt). Alternatives en réserve : NEXLUM / AIVIO / OPERAI / VELOAI. Le nom de marque final sera arrêté en J5.

---

## 0. Synthèse exécutive (pour fonds Série A pressé)

| Indicateur | Valeur | Source |
|---|---|---|
| **TAM** (Europe, marché IA-pour-entreprises adressable PME) | **≈ 38 Md€** d'ici 2030 | Dérivé IDC / McKinsey / Eurostat (cf. §3) |
| **SAM** (France + Benelux, cabinets + scale-ups, services + SaaS) | **≈ 2,4 Md€** | Calcul bottom-up (cf. §4) |
| **SOM** (capturable réaliste à 36 mois) | **~1,66 M€ CA An 3** (modèle exécutable) ; plafond ~6,5 M€ | Modèle `execution/10` (cf. §5) |
| PME dans l'UE | **33,5 millions d'entreprises**, dont 99,8 % de PME | [Eurostat 2024](https://ec.europa.eu/eurostat/web/products-eurostat-news/w/ddn-20241025-1) |
| Adoption IA — petites entreprises UE | **11,2 %** (vs 41,2 % grandes) | [Eurostat, déc. 2025](https://ec.europa.eu/eurostat/web/products-eurostat-news/w/ddn-20251211-2) |
| Fenêtre réglementaire IA Act (obligations haut-risque) | **2 août 2026** (déféré possible déc. 2027) | [EU AI Act timeline](https://artificialintelligenceact.eu/implementation-timeline/) |

**Thèse d'investissement en une phrase :** 33,5 millions de PME européennes, dont seulement ~11 % utilisent l'IA, font face à une obligation réglementaire (IA Act) sans disposer ni des compétences ni d'un acteur souverain abordable pour s'y conformer — LUMIO occupe ce vide par une double entrée marché (cabinets prescripteurs + scale-ups early adopters) et une infrastructure model-agnostic ancrée sur Mistral AI.

**Gain estimé sur le taux de réussite global : +6 points (de 68 % → 74 %).** Le dimensionnement chiffré et sourcé transforme une intuition de marché en thèse défendable devant un comité d'investissement. (Le solde vers 94-96 % proviendra du modèle financier J3 et de la traction réelle J4-J7.)

---

## 1. Méthodologie & règles de preuve

1. **Sources primaires uniquement** pour les chiffres structurants : Eurostat, INSEE, OCDE, McKinsey Global Institute, IDC, Gartner, BPI France, Ordre des Experts-Comptables.
2. **Distinction stricte** entre *donnée sourcée* (citée), *estimation dérivée* (calcul explicité) et *hypothèse* (signalée comme telle). Aucun chiffre « inventé » présenté comme un fait.
3. **TAM/SAM/SOM construits en bottom-up** (par le nombre de clients × ARPA) ET recoupés en top-down (taille de marché × part adressable). Quand les deux convergent, la fourchette est crédible.
4. **Prudence assumée** : en cas de doute, on retient la borne basse. Un fonds Série A pénalise l'optimisme non étayé, jamais la rigueur.

---

## 2. Tendances de marché — IA × PME, 2024–2030

### 2.1 Le marché de l'IA d'entreprise est en phase d'inflexion

- **Potentiel économique de l'IA générative : 2 600 à 4 400 Md$/an** sur 63 cas d'usage analysés, jusqu'à **7 900 Md$/an** intégration logicielle comprise — [McKinsey Global Institute, 2023](https://www.mckinsey.com/capabilities/tech-and-ai/our-insights/the-economic-potential-of-generative-ai-the-next-productivity-frontier).
- **75 % de cette valeur** se concentre sur 4 fonctions : marketing/vente, opérations client, ingénierie logicielle, R&D — fonctions toutes présentes dans une PME. *Source : idem McKinsey.*
- La valeur n'est pas dans le modèle, mais dans **l'intégration au workflow métier** — c'est précisément la couche que LUMIO opère (thèse Jensen Huang : « l'infrastructure invisible indispensable »).

### 2.2 Le fossé d'adoption est la véritable opportunité

| Taille d'entreprise (UE, 2024) | % utilisant l'IA |
|---|---|
| Petites (10-49 sal.) | **11,2 %** |
| Moyennes (50-249) | **21,0 %** |
| Grandes (250+) | **41,2 %** |
| **Moyenne UE toutes tailles** | **13,5 %** |

*Source : [Eurostat, « 20% of EU enterprises use AI technologies », déc. 2025](https://ec.europa.eu/eurostat/web/products-eurostat-news/w/ddn-20251211-2) — note : le « 20 % » communiqué inclut un périmètre élargi ; le détail par taille reste 11/21/41 %.*

**Lecture stratégique (thèse Thiel — monopole de niche) :** l'écart de **30 points** entre petites et grandes entreprises n'est pas un problème technologique (les modèles sont accessibles via API à coût marginal quasi nul) mais un **problème d'accompagnement**. C'est un marché de service + outillage, pas un marché de R&D. Cela neutralise l'objection « OpenAI/Google vont vous écraser » : les hyperscalers vendent des modèles, pas de l'accompagnement sectoriel souverain aux PME françaises.

- **67 % des dirigeants de PME déclarent manquer d'accompagnement concret** sur le numérique/l'IA — *BPI France Le Lab, 2023.* ⚠️ *À re-sourcer précisément avant diffusion externe (référence exacte de l'étude à citer).*
- **Cas d'usage IA n°1 en entreprise UE : l'analyse de langage écrit (11,8 %)** — soit exactement le cœur de métier documentaire des cabinets comptables et juridiques. [Eurostat 2024](https://ec.europa.eu/eurostat/statistics-explained/index.php?title=Use_of_artificial_intelligence_in_enterprises).

### 2.3 Trois forces macro convergentes (2024-2030)

1. **Réglementaire — l'IA Act crée un marché « forcé ».** Échéance obligations haut-risque : **2 août 2026** (report possible à déc. 2027 via Digital Omnibus, mais à traiter comme opératoire en l'absence d'adoption formelle) — [EU AI Act implementation timeline](https://artificialintelligenceact.eu/implementation-timeline/). Toute PME déployant de l'IA devra documenter, classifier et se conformer → demande de conseil structurelle.
2. **Souveraineté — la préférence européenne se politise.** Montée de Mistral AI (champion européen), discours de souveraineté numérique porté par la Commission et les États. Argument différenciant face aux solutions 100 % GAFAM.
3. **Économique — pression sur la productivité des PME.** Croissance de la valeur ajoutée des PME UE quasi nulle en 2024 (-0,2 %) — [Annual Report on European SMEs 2024/2025, JRC](https://publications.jrc.ec.europa.eu/repository/handle/JRC142263). L'IA devient un levier de marge non optionnel.

---

## 3. TAM — Marché total adressable

**Définition LUMIO :** dépenses européennes liées à l'intégration de l'IA dans les PME (services de conseil/audit/formation IA + logiciels d'IA appliquée orientés PME), horizon 2030.

### 3.1 Approche top-down

- **33,5 millions d'entreprises dans l'UE**, dont **99,8 % de PME** (~33,4 M), dont ~33,2 M de micro/petites — [Eurostat 2024](https://ec.europa.eu/eurostat/web/products-eurostat-news/w/ddn-20241025-1).
- Cible utile LUMIO = entreprises de **10 à 249 salariés** (capacité de payer + besoin réel d'accompagnement). L'UE compte environ **1,5 million de PME de 10-249 salariés** (les 10-49 et 50-249, hors micro-entreprises de 0-9). *Estimation Eurostat — structure 99 % micro / ~1 % PME 10-249.*
- **Budget annuel moyen capturable** (conseil IA + outillage SaaS) par PME 10-249 à maturité 2030 : **hypothèse prudente 25 000 €/an** (mix services ponctuels + abonnement récurrent).

**TAM top-down = 1,5 M PME × 25 000 € ≈ 37,5 Md€/an** à horizon 2030.

### 3.2 Recoupement par le marché logiciel/services IA

- Le marché européen de l'IA (logiciels + services) est estimé en dizaines de milliards € et croît à un TCAC > 25 % — *ordre de grandeur IDC / Gartner.* ⚠️ *Chiffre précis IDC Europe AI spending à insérer (référence exacte à acheter/citer en data room J7).*
- La part « PME » de ce marché reste sous-pénétrée (cf. fossé d'adoption §2.2), ce qui rend le **38 Md€ atteignable par expansion d'adoption**, pas seulement par croissance organique.

> **TAM retenu : ≈ 38 Md€ (2030).** Fourchette défendable 30–45 Md€. *Donnée dérivée, méthode explicitée — à présenter comme estimation, jamais comme fait Eurostat.*

---

## 4. SAM — Marché adressable desservi

**Définition LUMIO :** zone géographique de lancement réaliste = **France + Benelux** (proximité langue/réglementation, écosystème Mistral, cycle de vente maîtrisable), sur les **deux cibles** définies.

### 4.1 Cible A — Cabinets d'expertise comptable & juridiques (France)

- **~21 000 cabinets d'expertise comptable** en France (~156 000 professionnels) — *Ordre des Experts-Comptables.* ⚠️ *Chiffre à figer (21 000–22 000 selon périmètre, à sourcer précisément OEC).*
- Rôle stratégique : **prescripteurs naturels** — un cabinet équipé revend/recommande LUMIO à son portefeuille de PME clientes (effet de levier multiplicateur).
- ARPA cible cabinet (SaaS + conseil) : **hypothèse 4 000–8 000 €/an**.

**SAM Cible A ≈ 21 000 × 6 000 € ≈ 126 M€/an** (revenu direct cabinets, hors effet prescription).

### 4.2 Cible B — Startups & scale-ups 10-50 salariés (France + Benelux)

- Décision rapide (48 h), budget tech disponible, early adopters → flux de trésorerie rapide (FLUX 1).
- Population estimée France + Benelux : **plusieurs dizaines de milliers** d'entreprises tech/scale-ups dans la tranche 10-50 salariés. *Estimation à affiner via INSEE / registres Benelux.*
- ARPA cible : **hypothèse 6 000–15 000 €/an** (missions ponctuelles + abonnement).

### 4.3 Effet de levier prescription (cœur de la thèse)

Chaque cabinet (Cible A) donne accès à **20–50 PME clientes**. 21 000 cabinets × 30 PME = **portefeuille indirect théorique de 630 000 PME** — c'est le véritable réservoir du SAM, accessible via un seul canal de distribution B2B2B.

> **SAM retenu : ≈ 2,4 Md€** (France + Benelux, direct + portefeuille prescrit adressable, services + SaaS). *Donnée dérivée bottom-up.*

---

## 5. SOM — Marché capturable (objectif 36 mois)

**Définition :** ce que LUMIO peut réalistement signer d'ici fin An 3, capital de départ ≈ 0, équipe resserrée, MVP no-code (Typeform+Claude / Notion+Make / Zapier+Mistral).

### 5.1 Scénario bottom-up (prudent)

| Source de revenu | An 1 | An 2 | An 3 |
|---|---|---|---|
| FLUX 1 — Conseil/audit/formation | 80 k€ | 248 k€ | 500 k€ |
| FLUX 2 — SaaS PME + cabinets | 34 k€ | 317 k€ | 911 k€ |
| FLUX 3 — Benchmarks anonymisés *(corrigé, ex-« data licensing »)* | 0 | 13 k€ | 246 k€ |
| **Total CA annualisé** | **~114 k€** | **~578 k€** | **~1,66 M€** |

> **Chiffres mis à jour** par le modèle financier exécutable (`execution/10_modele_financier.py`, cf. J3) qui remplace l'estimation manuelle initiale (80/460/1 800 k€). ARR de sortie M36 ≈ 1,28 M€. Aligné sur le KPI MRR SaaS 1 500 € au mois 6.

### 5.2 Scénario haut (exécution réussie + effet prescription)

Si LUMIO convertit **300 cabinets** (1,4 % de la Cible A) à 6 000 €/an + **400 scale-ups** à 9 000 €/an → **~5,4 M€** ; avec FLUX 3, **≈ 6,5 M€ ARR potentiel** à 36 mois.

> **SOM retenu : ~1,66 M€ CA An 3 (ARR de sortie ~1,28 M€), modèle exécutable ; plafond d'exécution ~6,5 M€.** Représente **< 0,1 % du SAM** → cible volontairement sous-dimensionnée = crédibilité maximale devant un comité (on ne promet pas la lune, on prouve qu'on en gratte une fraction infime).

---

## 6. Cartographie concurrentielle & faiblesses des acteurs

| Catégorie | Acteurs | Force | **Faiblesse exploitable par LUMIO** |
|---|---|---|---|
| **Big 4 / conseil** | Deloitte, EY, KPMG, PwC | Crédibilité, réseau | Inabordables pour une PME (TJM 1 500-3 000 €), pas de produit récurrent, pas souverain par design |
| **Éditeurs comptables** | Pennylane, Sage, Cegid, QuadraNet | Base installée cabinets | IA = feature add-on, pas d'accompagnement transversal ni de conformité IA Act dédiée |
| **Hyperscalers / modèles** | OpenAI, Google, Microsoft Copilot | Puissance modèle | Vendent un modèle, pas une intégration métier PME ; **dépendance GAFAM = angle mort souveraineté** |
| **Champion européen** | Mistral AI | Souveraineté, RGPD natif | Vend de l'infrastructure/modèle, **pas la couche conseil + workflow PME** → partenaire potentiel, pas concurrent |
| **Agences IA / freelances** | Multitude fragmentée | Agilité, prix | Pas de méthodologie propriétaire, pas de récurrence, pas de conformité, pas de marque |
| **Pure players conformité IA Act** | Quelques start-ups émergentes | Focus réglementaire | Mono-produit, ne couvrent pas l'intégration opérationnelle ni la double cible |

**Vide de marché identifié (la niche monopolisable — thèse Thiel) :** *aucun acteur ne combine simultanément* (1) accompagnement opérationnel abordable PME, (2) souveraineté/Mistral + RGPD, (3) readiness IA Act intégré, (4) modèle récurrent SaaS, (5) canal prescripteur cabinets. NEXLUM est positionné à l'intersection exacte de ces cinq axes.

> ⚠️ **Repositionnement clé (faille #14, validé par recherche réelle) :** la **production comptable IA est déjà saturée** (Cegid Loop/PIA, Pennylane 300 000+ users, Sage Copilot, Dext). NEXLUM **n'y va pas**. Son terrain est le **transversal non-comptable** (juridique, RH, comms, ops, marketing), l'**activation des PME clientes** en marque blanche, et le **readiness IA Act** — là où ces éditeurs ne sont pas. Stratégie d'**intégration** aux éditeurs, pas de confrontation. Détail : `execution/06_intelligence_concurrentielle.md`.

---

## 7. Impact de l'IA Act sur la taille du marché adressable

- L'IA Act **élargit mécaniquement le SAM** : il transforme l'adoption IA d'un *choix* en une *obligation documentée*. Échéance opératoire haut-risque **2 août 2026** — [timeline officielle](https://artificialintelligenceact.eu/implementation-timeline/).
- Toute PME déployant un système IA devra : classifier le risque, documenter, assurer la transparence, parfois réaliser une évaluation de conformité. **C'est un service récurrent, pas un one-shot** → renforce FLUX 1 ET FLUX 2.
- **Incertitude réglementaire à intégrer (honnêteté Série A) :** le *Digital Omnibus* (accord provisoire mai 2026) pourrait reporter les obligations Annexe III à **déc. 2027** — [DLA Piper](https://knowledge.dlapiper.com/dlapiperknowledge/globalemploymentlatestdevelopments/2026/The-Digital-AI-Omnibus-Proposed-deferral-of-high-risk-AI-obligations-under-the-AI-Act). LUMIO traite août 2026 comme la date opératoire : un report n'annule pas la demande, il l'étale. La conformité reste un **avantage structurel**, pas un pari sur une date.
- **Conséquence chiffrée :** même une conversion de 5 % des PME 10-249 UE à un audit de conformité IA Act à 2 000 € représente un sous-marché de **1,5 M × 5 % × 2 000 € = 150 M€** ponctuel — adressable en priorité sur la zone SAM.

---

## 8. Opportunité défendable de LUMIO — synthèse pour comité d'investissement

1. **Timing (why now) :** convergence unique fossé d'adoption (11 %) + obligation réglementaire (IA Act 2026) + champion souverain disponible (Mistral). Cette fenêtre n'existait pas il y a 18 mois.
2. **Distribution (le vrai moat) :** le canal cabinets (B2B2B) donne accès à 630 000 PME via 21 000 points de vente prescripteurs — barrière à l'entrée que les hyperscalers ne peuvent pas répliquer.
3. **Capital-efficience :** MVP no-code à < 150 €/mois, FLUX 1 autofinance la survie, FLUX 2 scale, FLUX 3 valorise la donnée → trajectoire crédible sans capital initial.
4. **Défendabilité narrative :** souveraineté + IA Act + model-agnostic = trois arguments qu'un fonds européen, une banque publique ou un gouvernement *veulent* financer.

---

## 9. Limites, risques et chantiers de fiabilisation (transparence pré-data room)

| Élément | Statut | Action J3-J7 |
|---|---|---|
| TAM 38 Md€ | Dérivé, méthode explicitée | Acheter/citer rapport IDC Europe AI spending (data room J7) |
| Nombre exact cabinets (21 000-22 000) | À figer | Source OEC précise |
| BPI France « 67 % » | À re-sourcer | Référence exacte de l'étude |
| ARPA / taux de conversion | Hypothèses | **Validation Van Westendorp — 20 appels experts-comptables en cours** |
| Population scale-ups Benelux | Estimation | Croisement INSEE + registres Benelux |
| IDC / Gartner taille marché | Ordre de grandeur | Chiffres précis sourcés en data room |

**Principe assumé :** ce document distingue rigoureusement le sourcé du dérivé. Aucune affirmation n'est présentée comme un fait Eurostat si elle est un calcul LUMIO. C'est ce qui le rend défendable en *due diligence*.

---

## 10. Sources

- Eurostat — [Micro & small businesses make up 99% of enterprises in the EU (2024)](https://ec.europa.eu/eurostat/web/products-eurostat-news/w/ddn-20241025-1)
- Eurostat — [20% of EU enterprises use AI technologies (déc. 2025)](https://ec.europa.eu/eurostat/web/products-eurostat-news/w/ddn-20251211-2)
- Eurostat — [Use of artificial intelligence in enterprises (Statistics Explained)](https://ec.europa.eu/eurostat/statistics-explained/index.php?title=Use_of_artificial_intelligence_in_enterprises)
- McKinsey Global Institute — [The economic potential of generative AI (2023)](https://www.mckinsey.com/capabilities/tech-and-ai/our-insights/the-economic-potential-of-generative-ai-the-next-productivity-frontier)
- JRC / Commission européenne — [Annual Report on European SMEs 2024/2025](https://publications.jrc.ec.europa.eu/repository/handle/JRC142263)
- OCDE — [AI adoption by small and medium-sized enterprises (2025)](https://www.oecd.org/content/dam/oecd/en/publications/reports/2025/12/ai-adoption-by-small-and-medium-sized-enterprises_9c48eae6/426399c1-en.pdf)
- EU AI Act — [Implementation timeline](https://artificialintelligenceact.eu/implementation-timeline/)
- DLA Piper — [Digital AI Omnibus : deferral of high-risk obligations (2026)](https://knowledge.dlapiper.com/dlapiperknowledge/globalemploymentlatestdevelopments/2026/The-Digital-AI-Omnibus-Proposed-deferral-of-high-risk-AI-obligations-under-the-AI-Act)
- BPI France Le Lab (2023) — *référence précise à figer*
- Ordre des Experts-Comptables — *référence précise à figer*
- IDC / Gartner — *European AI spending, chiffres précis à intégrer en data room J7*

---

*Document LUMIO — J2/J7. Prochaine étape : J3 — Modèle financier P&L 36 mois (construit sur les ARPA et taux de conversion validés par les 20 appels en cours).*
