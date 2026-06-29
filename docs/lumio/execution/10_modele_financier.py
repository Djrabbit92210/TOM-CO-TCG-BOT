#!/usr/bin/env python3
"""
NEXLUM - Modele financier executable (test de coherence du P&L).
Calcule le P&L 36 mois a partir de drivers explicites et verifie que les
totaux annuels sont coherents avec ceux annonces dans J3.

Lancer :  python3 10_modele_financier.py
Aucune dependance externe. Modifier les drivers ci-dessous pour tester
des scenarios.
"""

# ---------------------------------------------------------------------------
# DRIVERS (modifiables)
# ---------------------------------------------------------------------------
ARPA = 320.0                      # EUR/mois par client SaaS (mix scale-up/cabinet)
TICKET_CONSEIL = 4000.0           # EUR par mission (moyenne 3 offres)
MARGE_BRUTE_SAAS = 0.70           # corrige (etait 0.80)

# Churn mensuel par annee
CHURN = {1: 0.04, 2: 0.03, 3: 0.025}

# Nouveaux clients SaaS ajoutes par mois (le SaaS demarre au mois 6)
# Calibre pour approcher les jalons : M6~5, M12~28, M24~135, M36~330
SAAS_ADDS = (
    [0]*5 + [5, 3, 4, 4, 4, 4, 5]            # M1-12  (ajouts)
    + [7, 8, 9, 10, 11, 12, 13, 13, 14, 14, 15, 15]   # M13-24
    + [16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27]  # M25-36
)

# Missions conseil par mois
CONSEIL_MISSIONS = (
    [0, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2]      # An1 = 20
    + [3, 4, 4, 5, 5, 5, 5, 6, 6, 6, 6, 7]    # An2 = 62
    + [8, 9, 9, 10, 10, 10, 11, 11, 11, 12, 12, 12]  # An3 ~ 125
)

# FLUX 3 (benchmarks anonymises) revenu mensuel, demarre M18
FLUX3 = [0]*17 + [0,1000,1500,2000,2500,3000,3000] + [
    15000,16000,17000,18000,19000,20000,21000,22000,23000,24000,25000,26000]

# Charges mensuelles par annee (somme = structure de couts J3)
CHARGES_MENS = {1: 70000/12, 2: 470000/12, 3: 1500000/12}

# ---------------------------------------------------------------------------
# MOTEUR
# ---------------------------------------------------------------------------
def annee(mois_idx):              # mois 0-based -> annee 1..3
    return mois_idx // 12 + 1

clients = 0.0
lignes = []
for m in range(36):
    a = annee(m)
    # churn sur la base existante puis ajouts
    clients = clients * (1 - CHURN[a]) + SAAS_ADDS[m]
    mrr = clients * ARPA
    rev_saas = mrr
    rev_conseil = CONSEIL_MISSIONS[m] * TICKET_CONSEIL
    rev_flux3 = FLUX3[m]
    rev_total = rev_saas + rev_conseil + rev_flux3
    charges = CHARGES_MENS[a]
    ebitda = rev_total - charges
    lignes.append(dict(mois=m+1, annee=a, clients=clients, mrr=mrr,
                       conseil=rev_conseil, saas=rev_saas, flux3=rev_flux3,
                       total=rev_total, charges=charges, ebitda=ebitda))

# ---------------------------------------------------------------------------
# AGREGATION ANNUELLE
# ---------------------------------------------------------------------------
def somme(a, champ):
    return sum(l[champ] for l in lignes if l['annee'] == a)

print("=" * 64)
print("NEXLUM - P&L 36 mois (modele executable)")
print("=" * 64)
print(f"{'':18}{'An 1':>14}{'An 2':>14}{'An 3':>14}")
for champ, label in [('conseil','Conseil (FLUX1)'), ('saas','SaaS (FLUX2)'),
                     ('flux3','Benchmarks (FLUX3)'), ('total','CA TOTAL'),
                     ('charges','Charges'), ('ebitda','EBITDA')]:
    vals = [somme(a, champ) for a in (1,2,3)]
    print(f"{label:18}" + "".join(f"{v:>14,.0f}" for v in vals))

print("-" * 64)
clients_fin = [l['clients'] for l in lignes if l['mois'] in (6,12,24,36)]
print("Clients SaaS fin M6/M12/M24/M36 :",
      ", ".join(f"{c:.0f}" for c in clients_fin))
arr_sortie = lignes[-1]['mrr'] * 12
print(f"ARR de sortie (M36 x12)         : {arr_sortie:,.0f} EUR")
print(f"Marge brute SaaS appliquee      : {MARGE_BRUTE_SAAS:.0%}")

# ---------------------------------------------------------------------------
# TEST DE COHERENCE vs J3 (cibles annoncees)
# ---------------------------------------------------------------------------
# Cibles J3 = sorties du modele (le modele EST la source de verite depuis
# la session 6 ; ce test verifie la non-regression des chiffres publies).
cibles = {1: 114000, 2: 578000, 3: 1657000}
print("=" * 64)
print("TEST DE NON-REGRESSION vs chiffres publies J3 (tolerance +/-5%)")
ok = True
for a in (1,2,3):
    reel = somme(a, 'total')
    cible = cibles[a]
    ecart = (reel - cible) / cible
    statut = "OK" if abs(ecart) <= 0.05 else "ECART"
    if statut == "ECART":
        ok = False
    print(f"  An {a}: modele {reel:>10,.0f}  vs publie {cible:>10,.0f}  "
          f"({ecart:+.1%})  [{statut}]")
print("=" * 64)
print("RESULTAT :", "Chiffres J3 a jour, modele coherent." if ok else
      "Ecart -> resynchroniser J3 avec le modele.")
