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

<!-- Les entrées suivantes seront ajoutées ici, une par jour. -->
