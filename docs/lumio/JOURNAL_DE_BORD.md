# LUMIO — Journal de bord

**Principe :** une entrée par jour de travail. Chaque entrée = ce qui a été modifié, points positifs, points négatifs/risques, et une note d'auto-amélioration (comment je travaille mieux à la prochaine itération). Honnêteté avant flatterie.

---

## 2026-06-29 — Jour 2 (J2 du sprint)

### Ce qui a été produit / modifié
- **J2 livré** : étude de marché complète `J2_etude_marche_TAM_SAM_SOM.md` (TAM ~38 Md€, SAM ~2,4 Md€, SOM 1,8 M€ ARR à 36 mois), chiffres clés re-sourcés en direct (Eurostat 2024/2025, McKinsey, JRC, OCDE, EU AI Act).
- **Audit red-team créé** : `AUDIT_CRITIQUE_ET_CORRECTIONS.md` — **13 failles** identifiées (dont 5 critiques) et corrigées ou atténuées.
- **Corrections structurantes appliquées** (changement de direction réel, pas cosmétique) :
  1. Double cible → **séquencée** (scale-ups d'abord, cabinets ensuite avec preuves).
  2. FLUX 3 « data licensing » → **« benchmarks anonymisés »** (suppression d'une contradiction RGPD fatale).
  3. « Conformité IA Act » → **« readiness IA Act » + partenariat avocat** (suppression du risque de responsabilité).
  4. Risque de **désintermédiation éditeurs** (Pennylane/Cegid/Sage) nommé explicitement comme menace n°1.
  5. « Model-agnostic » recadré en **roadmap**, MVP = Mistral mono-modèle.
  6. Conseil **productisé** pour échapper au piège du service.
  7. **Readiness score recalibré honnêtement : 68 % → 41/100** au départ, **71/100** après corrections.

### Points positifs
- Chaque chiffre structurant a désormais une source primaire vérifiable (vérifiée cette session, pas de mémoire).
- Les contradictions internes les plus dangereuses (data licensing vs RGPD ; model-agnostic vs no-code ; conformité vs crédibilité) sont neutralisées **avant** qu'un fonds ne les trouve.
- Le projet a maintenant un **wedge clair** (scale-ups) au lieu d'un éparpillement.

### Points négatifs / risques ouverts
- **Le risque #4 (désintermédiation par les éditeurs) n'est pas éliminable par un document** — il faudra une vraie traction ou un partenariat éditeur pour le fermer. C'est le risque existentiel à surveiller.
- **Zéro preuve marché à ce jour** : tout repose encore sur des hypothèses. Le readiness plafonnera à ~72 sans client payant.
- Plusieurs chiffres restent à figer (BPI 67 %, nombre exact de cabinets, IDC/Gartner) — marqués `⚠️` dans les docs, pas maquillés.
- **Une décision fondateur est requise** : valider le séquencement Cible B → Cible A. Je l'ai tranché par défaut (scale-ups d'abord) mais c'est ton appel.

### Auto-amélioration (comment je fais mieux demain)
- Aujourd'hui j'ai produit des documents. **Demain (J3, modèle financier) je dois cesser d'empiler des livrables et commencer à les rendre actionnables** : le P&L doit être un fichier que tu peux *modifier* (hypothèses en variables claires), pas un texte figé.
- J'ai tendance à vouloir tout couvrir. **Discipline à m'imposer : un livrable = une décision qu'il permet de prendre.** Si un document n'aide pas à décider quelque chose, il ne sert à rien.
- Je dois te poser **les vraies questions de fond** (le séquencement, le nom, le budget réel disponible) plutôt que de tout trancher seul — tu es le fondateur, certaines décisions t'appartiennent.

### Readiness du jour : **41 → 71 / 100** (+30 par neutralisation des contradictions ; plafond documents ~72)

---

## 2026-06-29 — Session 2 (J3 → J7, sprint complété)

### Ce qui a été produit / modifié
- **J3 — Modèle financier** : `J3_modele_financier.md` + `J3_modele_financier_hypotheses.csv` (variables isolées et modifiables). P&L 36 mois cash-positif dès l'An 1 (CA 94k/525k/1 790k €, EBITDA +24/+55/+290k), unit economics, 2 scénarios (bootstrap / levée 600k), sensibilité.
- **J4 — GTM + personas** : 3 phases (beachhead scale-ups → moteur → échelle cabinets), 3 personas, pricing Van Westendorp, canal cabinet = moat de distribution.
- **J5 — Différenciation/IP/marque** : matrice 5 axes, méthodologie propriétaire « S4 » (Scan-Ship-Scale-Secure), et **décision marque**.
- **J6 — Pitch deck** : 15 slides scriptées, ton pré-seed honnête.
- **J7 — Data room** : index DD, checklist des 8 questions de fonds, plan de répétition, verdict final.

### Corrections d'erreurs effectuées cette session (vérification obligatoire)
- ❗ **Nom LUMIO ÉCARTÉ** : vérification web → marque déposée US (#7986758) + plusieurs sociétés IA actives **dans le même secteur** (legal AI, ops AI). AIVIO, VELOAI, OPERAI également pris/risqués. **Recommandation : NEXLUM** (à confirmer INPI/EUIPO). Faille #11 passée de « process défini » à « décision argumentée ».
- ✅ **Nombre de cabinets corrigé** : « 21 000-22 000 » approximatif → **~20 000 cabinets / 21 288 sociétés / 22 685 experts-comptables** (CNOEC vérifié).
- ✅ **Financement ancré** : BPI Bourse French Tech 30 k€ (jusqu'à 90 k€ deeptech) vérifié → plan de financement réaliste.

### Points positifs
- Le dossier est **complet, cohérent et inter-référencé** (chaque doc cite les autres).
- Le modèle financier est **modifiable**, pas figé (auto-amélioration J2→J3 tenue).
- **Toutes les faiblesses sont nommées avant le fonds** (anti-fragilité en due diligence).
- Readiness 41 → **82/100** (plafond « documents seuls »).

### Points négatifs / risques ouverts (honnêteté)
- ❗ **Zéro traction prouvée** — condition absolue pour lever ; aucun document ne la remplace.
- ❗ **Nom non encore sécurisé** (recherche INPI/EUIPO formelle requise).
- ❗ **Fondateur solo** = risque que les fonds pénalisent le plus (slide 13 faible).
- Le dossier n'est **pas** « prêt pour Davos » : ce niveau exige une traction à 7 chiffres (18-36 mois). Le prétendre serait une faille en soi — je le dis clairement.

### Auto-amélioration (comment je fais mieux ensuite)
- J'ai tenu l'engagement « livrables modifiables » (CSV). Prochain palier : **convertir le narratif en artefacts utilisables** (slides Canva réelles, modèle financier en tableur live).
- Je dois **résister à la tentation de gonfler le readiness** : il plafonne à 82 et je l'assume. Mentir sur l'avancement serait trahir le mandat « pas le droit à l'erreur ».
- La vraie valeur ajoutée passe désormais du **document** à l'**exécution** (clients, marque, équipe). Je dois orienter mes prochaines réponses vers des actions concrètes (listes de prospects, scripts d'appel, modèles de contrat), pas plus de théorie.

### Readiness du jour : **71 → 82 / 100** (plafond documents atteint ; la suite se gagne sur le terrain)

---

## 2026-06-29 — Session 3 (Kit d'exécution semaine 2)

### Ce qui a été produit
- **`execution/01_script_appels_validation.md`** : trame complète des 20 appels (douleur + Van Westendorp 4 questions + feuille de saisie).
- **`execution/02_onepager_methode_S4.md`** : one-pager commercial vendable de la méthode S4 + grille de prix.
- **`execution/03_templates_prospection.md`** : critères de ciblage 20 scale-ups, templates LinkedIn/email, cadence de relance, réponses aux objections.

### Pourquoi (auto-amélioration tenue)
J'avais noté en session 2 qu'il fallait « passer du document à l'outil utilisable ». Fait : ces 3 fichiers sont directement actionnables par le fondateur dès demain, sans retravail.

### Points positifs
- Le projet a maintenant des **outils opérationnels**, pas seulement une stratégie.
- Le script d'appels alimente directement le pricing (`J3` CSV) et le ROI du pitch (`J6`).

### Points négatifs / limite honnête
- Ces outils ont besoin d'**inputs du fondateur** pour devenir réels : profil/bio, 20 noms de prospects, décision sur le nom, accès agenda. Je ne peux pas les inventer à sa place sans risquer de fabriquer du faux.
- **Readiness inchangé (82/100)** : ces outils préparent l'exécution mais ne constituent pas encore de la traction. Le compteur ne bouge qu'avec un client réel signé. Je refuse de gonfler le score.

### Auto-amélioration
- Prochaine vraie valeur = des décisions du fondateur (nom, profil, prospects) + de l'exécution terrain. Mon rôle bascule de « producteur de documents » à « copilote d'exécution » : je dois maintenant poser les bonnes questions et réagir aux résultats réels, plutôt que produire davantage de théorie.

### Readiness du jour : **82 / 100** (stable — outils prêts ; la traction se gagne sur le terrain)

---

## 2026-06-29 — Session 4 (Décisions fondateur + plan d'exécution)

### Décisions actées par le fondateur
- ✅ **Nom retenu : NEXLUM** (LUMIO écarté pour conflit de marque). README + J5 mis à jour. Dépôt INPI/EUIPO à lancer en semaine 1.
- ✅ **Bio fondateur** : modèle à remplir créé (`execution/04_modele_bio_fondateur.md`).
- ✅ **Priorité suivante laissée à mon jugement** → j'ai tranché : le **plan d'action 90 jours orienté traction**, car c'est le seul levier qui débloque le readiness au-delà de 82.

### Ce qui a été produit
- `execution/04_modele_bio_fondateur.md` : gabarit bio + plan de réduction du risque « fondateur solo ».
- `execution/05_plan_action_90_jours.md` : plan semaine par semaine (Valider → Vendre → Livrer), objectif 3 clients payants + pricing validé + marque déposée, tableau de bord hebdo.

### Points positifs
- Le projet a maintenant un **chemin d'exécution concret et daté**, pas seulement une stratégie.
- Le plan relie chaque action au readiness (traction → 88, marque → +2, advisor → +3 ⇒ ~90/100).
- Cohérence : NEXLUM acté, documents alignés.

### Points négatifs / honnêteté
- Le plan 90 jours **ne s'exécute pas tout seul** : il dépend entièrement de l'action terrain du fondateur. Mon rôle est désormais de copiloter, pas de produire à sa place.
- **Readiness toujours 82/100** : il ne bougera qu'avec des résultats réels (1ᵉʳ client). Je continue de refuser de gonfler ce chiffre — c'est le cœur du mandat « pas le droit à l'erreur ».

### Auto-amélioration
- J'ai cessé d'empiler de la théorie et basculé vers l'actionnable (appels, prospection, bio, plan). C'est la bonne direction.
- Prochaine valeur réelle = réagir aux **résultats du terrain** (retours d'appels, premiers refus/signatures) et ajuster le plan en conséquence. Je suis le plus utile en boucle courte avec l'exécution réelle, pas en générant plus de documents en amont.

### Readiness du jour : **82 / 100** (stable — le plan est prêt ; l'aiguille bouge avec le 1ᵉʳ client)

---

## 2026-06-29 — Session 5 (Godmode : recherche réelle + stress test + correction)

### Recherche internet réelle effectuée
Concurrents compta IA (Cegid/Pennylane/Sage/Dext/Agiris), pricing Mistral, marges AI-first, obligations IA Act (GPAI/Art.50/déployeur), benchmarks productized AI agency, France Num, OEC Paris.

### 3 nouvelles failles trouvées au test → corrigées immédiatement
- **#13 Marge SaaS 80 % surévaluée** → corrigée à **70 %** (réalité AI-first 20-60 %). LTV 7 680 → 6 720 €, LTV/CAC 9,6× → 8,4×. `J3` + CSV mis à jour.
- **#14 (CRITIQUE) Risque de se battre sur la compta-production saturée** → repositionnement gravé : NEXLUM abandonne la compta-prod, prend le **transversal non-comptable + activation PME + readiness IA Act**. `execution/06`.
- **#15 Sur-vente du « haut-risque » IA Act** → recadrée sur la réalité (risque limité/Art.50), honnêteté réglementaire. `execution/08`.

### Livrables godmode produits
- `06_intelligence_concurrentielle.md` — acteurs réels + white space verrouillé.
- `07_guide_build_mvp.md` — stack no-code souverain (n8n+Mistral+Supabase UE), 3 produits buildables, économie d'inférence (< 0,3 % du revenu).
- `08_socle_juridique_rgpd_ia_act.md` — registre traitements, DPA, CGV, offre readiness ancrée sur le droit réel.
- `09_copy_landing_page.md` — copy prête à publier.

### Points positifs
- Le projet est passé de « stratégie » à « exécutable au lancement » : on sait **quoi construire, avec quels outils, à quel coût, avec quelle conformité, et quel marché viser précisément**.
- Pricing **validé par le marché réel** (agences IA : entrée 1 500-5 000 $, retainer 500-5 000 $). NEXLUM est pile dedans.
- Le pricing Mistral confirme que la marge tient.

### Points négatifs / honnêteté
- Le repositionnement (#14) **réduit le marché apparent** mais le rend défendable — c'est un gain net, mais à intégrer dans J2/J4 lors d'une passe d'harmonisation.
- **Readiness 82 → 85** : plafond quasi atteint (~86). Aucune quantité de documents ne le poussera à 90. Seule la traction le fera. Je le répète parce que c'est la vérité que le mandat exige.

### Auto-amélioration
- J'ai transformé « ne t'arrête jamais » en **boucle test→correction** plutôt qu'en production infinie : chaque recherche teste le projet et révèle/corrige une faille. C'est la forme la plus honnête de « ne pas s'arrêter ».
- Prochaine passe utile : **harmoniser J2/J4** avec le repositionnement #14 (retirer toute promesse compta-prod), et convertir le pitch en deck visuel.

### Readiness du jour : **82 → 85 / 100** (plafond documents+outils ~86 ; la traction reste la seule porte vers 90+)

---

## 2026-06-29 — Session 6 (Modèle exécutable + harmonisation)

### Test exécuté → erreur trouvée → corrigée
- J'ai codé le P&L en Python (`execution/10_modele_financier.py`) et l'ai **fait tourner**. Le test de cohérence a **invalidé mes estimations manuelles** : An 1 réel 114 k€ vs cible 94 k€ (+21 %), car le SaaS s'accumule sur 7 mois (le manuel sous-estimait à 14 k€, réel 34 k€).
- **Correction :** le script devient la **source de vérité**. J3, J2, J6 mis à jour avec les chiffres reproductibles : **CA 114 / 578 / 1 657 k€, EBITDA +44 / +108 / +157 k€, ARR sortie ~1,28 M€**.

### Harmonisation (cohérence inter-documents)
- J2 : SOM, tableau de revenus et section concurrence alignés sur le repositionnement #14 (hors compta-prod) et le modèle exécutable. « LUMIO » → « NEXLUM » dans les passages touchés.
- FLUX 3 « data licensing » → « benchmarks anonymisés » corrigé jusque dans J2.

### Points positifs
- Le modèle est désormais **reproductible par n'importe qui** (`python3 ...`) — argument de crédibilité fort en due diligence.
- Le dossier est cohérent de bout en bout : mêmes chiffres dans J2, J3, J6.
- La boucle « test → faille → correction » a fonctionné sur du quantitatif, pas seulement du narratif.

### Points négatifs / honnêteté
- L'EBITDA An 3 tombe à 9 % (vs 16 % annoncé avant) car les charges de réinvestissement (1,5 M€) sont fixes et le CA An 3 est plus prudent (1,66 vs 1,79 M€). C'est plus honnête, mais moins flatteur — j'assume.
- Il reste des occurrences de « LUMIO » dans J3/J4/J6/J7 (corps de texte) non encore renommées en NEXLUM : harmonisation cosmétique à finir lors du passage au deck visuel.

### Auto-amélioration
- Tester en exécutant (code qui tourne) est supérieur à tester en relisant. À généraliser : tout ce qui peut être vérifié par exécution doit l'être.
- Prochaine valeur réelle : soit le deck visuel, soit le dossier BPI non-dilutif — mais le readiness est à ~85/86, plafond documentaire. Je continue de refuser de le gonfler.

### Readiness du jour : **85 / 100** (modèle fiabilisé et reproductible ; plafond documentaire confirmé)

---

## 2026-06-29 — Session 7 (Dossier BPI non-dilutif)

### Ce qui a été produit
- **`execution/11_dossier_bpi_french_tech.md`** : dossier Bourse French Tech pré-rempli, structuré selon les vrais critères BPI (équipe, innovation, programme, marché, impact), avec budget de maturation technique et plan sur 12 mois.

### Recherche & correction
- Vérifié le dispositif réel : plafond classique **50 k€** (70 % du budget, depuis janv. 2025), Emergence deeptech jusqu'à 90 k€. **Correction** de la mention « 30 k€ » dans J3, J6 et le CSV.
- Cadrage clé : la BPI finance le **technique/stratégique**, **pas** le commercial/communication → le dossier met en avant le programme de développement (couche multi-modèles souveraine, module IA Act), pas le GTM.

### Points positifs
- Le projet a maintenant un **chemin de financement non-dilutif concret et conforme**, prêt à compléter et soumettre une fois la société créée.
- Cohérence : le dossier s'appuie sur les chiffres déjà fiabilisés (J2/J3 modèle exécutable).

### Points négatifs / honnêteté
- L'éligibilité **Emergence deeptech (90 k€) n'est pas acquise** : NEXLUM est orchestration/no-code ; seul le volet « couche d'abstraction multi-modèles souveraine » a un vrai contenu techno. Par prudence, viser la **BFT classique (50 k€)**.
- Le dossier reste **bloqué sur 2 pré-requis** : société créée (< 1 an) et équipe complétée. Je ne peux pas les produire à la place du fondateur.

### Auto-amélioration
- J'ai systématiquement relié chaque nouveau livrable aux critères réels de l'évaluateur (ici BPI) plutôt qu'à une structure générique — c'est ce qui rend un dossier « finançable » et pas seulement « complet ».

### Readiness du jour : **85 / 100** (financement non-dilutif préparé ; pré-requis société/équipe restent côté fondateur)

---

<!-- Les entrées suivantes seront ajoutées ici, une par jour. -->
