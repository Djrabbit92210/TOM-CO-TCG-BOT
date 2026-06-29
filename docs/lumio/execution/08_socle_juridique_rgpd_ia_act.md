# Socle juridique — RGPD & IA Act (starter pack exécutable)

**But :** donner à NEXLUM la conformité minimale pour vendre dès le lancement, et structurer l'offre « Readiness IA Act ».
**⚠️ Disclaimer :** ce document est un **socle opérationnel**, pas un avis juridique. L'acte juridique engageant doit être porté par l'**avocat partenaire** (faille #3). NEXLUM fait le diagnostic et la préparation ; l'avocat signe la conformité.

---

## 1. Ce que dit vraiment l'IA Act pour NEXLUM et ses clients (vérifié)

| Échéance | Ce qui s'applique | Impact NEXLUM |
|---|---|---|
| **2 fév. 2025** | Interdiction des pratiques « risque inacceptable » | À éviter par design (jamais de scoring social, biométrie, etc.) |
| **2 août 2025** | Obligations des fournisseurs de **GPAI** (modèles à usage général) actives | C'est **Mistral** (notre fournisseur) qui les porte, pas nous |
| **2 août 2026** | Obligations **systèmes haut-risque** (report possible déc. 2027) | La **plupart des cas PME ne sont PAS haut-risque** |

**Point capital (à dire honnêtement aux clients) :** la majorité des usages IA d'une PME relèvent du **« risque limité » (Article 50 — transparence)**, pas du « haut-risque ». NEXLUM ne doit **pas** vendre la peur du haut-risque à tort. La vraie valeur readiness :
- **Transparence (Art. 50)** : informer qu'un contenu/échange est généré par IA.
- **Obligations du déployeur** : qualité des données, **formation du personnel** à l'usage de l'IA, supervision humaine, monitoring.
- **Cartographie & classification** des systèmes IA utilisés (le livrable de diagnostic).

**Bonus PME :** l'IA Act prévoit des **plafonds de sanction réduits pour les PME/startups**. *Source : guides EU AI Act 2025.*

---

## 2. Offre « Readiness IA Act » — contenu livrable (3 500 €)

1. **Inventaire** des systèmes IA utilisés par le client (cartographie).
2. **Classification du risque** (inacceptable / haut / limité / minimal) par système.
3. **Checklist de conformité** selon la classe (transparence Art. 50, registre, supervision).
4. **Plan de formation** du personnel (obligation déployeur).
5. **Orientation juridique** vers l'avocat partenaire pour l'acte engageant.

> Positionnement marketing honnête : *« On vous rend prêt et serein face à l'IA Act, sans vous vendre une peur disproportionnée. »*

---

## 3. Conformité RGPD de NEXLUM lui-même (avant de vendre)

Checklist minimale pour être vendable sans risque :

- [ ] **Registre des traitements** (clients, prospects, données traitées par l'IA).
- [ ] **DPA (accord de sous-traitance)** signé avec chaque outil : Mistral, n8n/Make, Supabase, hébergeur.
- [ ] **Localisation UE** des données (Mistral UE, Supabase région Europe, VPS OVH/Scaleway).
- [ ] **Base légale** claire pour chaque traitement (contrat, consentement).
- [ ] **Mentions légales + politique de confidentialité** sur le site.
- [ ] **Politique de rétention** et procédure d'effacement.
- [ ] **Minimisation** : ne traiter que les données nécessaires ; anonymisation pour FLUX 3.
- [ ] **Clause de non-réutilisation** des données client pour l'entraînement (argument de confiance fort).

### Squelette de registre des traitements
| Traitement | Finalité | Base légale | Données | Destinataires | Localisation | Rétention |
|---|---|---|---|---|---|---|
| Diagnostic client | Réaliser la mission | Contrat | Données métier | Mistral (UE) | UE | Durée mission + X |
| Prospection | Démarchage B2B | Intérêt légitime | Contacts pro | CRM (UE) | UE | 3 ans |
| SaaS production | Faire tourner workflows | Contrat | Données client | Mistral, Supabase (UE) | UE | Durée abo |

---

## 4. Documents contractuels à préparer (templates à finaliser avec l'avocat)

| Document | Usage | Priorité |
|---|---|---|
| **CGV** (conseil + SaaS) | Toute vente | 🔴 Avant 1ʳᵉ vente |
| **Contrat de mission** (périmètre, prix, livrables) | FLUX 1 | 🔴 |
| **Contrat SaaS / abonnement** | FLUX 2 | 🟠 Avant 1ᵉʳ abo |
| **Accord marque blanche cabinet** (revenue-share 25 %) | Canal cabinet | 🟠 Phase 2 |
| **DPA** (vis-à-vis du client) | RGPD | 🔴 |
| **Mentions légales + politique conf.** | Site | 🔴 |

### Clauses non négociables (différenciantes)
- Données hébergées et traitées **en Union européenne**.
- **Aucune réutilisation** des données client pour entraîner des modèles.
- Réversibilité / export des données à la fin du contrat.
- Conformité IA Act « readiness » fournie, acte juridique via partenaire.

---

## 5. Plan d'action conformité (semaine 1-2)
1. [ ] Sécuriser l'**avocat partenaire** (tech/IP/IA) — apport d'affaires croisé.
2. [ ] Rédiger CGV + mentions légales + politique de confidentialité (modèles → avocat).
3. [ ] Signer les DPA avec Mistral, hébergeur, outils.
4. [ ] Monter le registre des traitements.
5. [ ] Finaliser le livrable « Readiness IA Act » comme produit.

---

## 6. Sources
- [EU AI Act — cadre réglementaire (Commission)](https://digital-strategy.ec.europa.eu/en/policies/regulatory-framework-ai)
- [Article 50 — obligations de transparence](https://artificialintelligenceact.eu/article/50/)
- [Guidelines GPAI providers](https://digital-strategy.ec.europa.eu/en/policies/guidelines-gpai-providers) · [EU AI Act timeline](https://artificialintelligenceact.eu/implementation-timeline/)
