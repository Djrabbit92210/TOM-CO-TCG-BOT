import { useState } from 'react'
import { Breadcrumb } from '../components/Breadcrumb'
import { mockExpenses } from '../data/mockData'
import { useToastStore } from '../stores/toastStore'

export function Budgets() {
  const [globalBudget, setGlobalBudget] = useState(1000)
  const [productBudget, setProductBudget] = useState(50)
  const [botBudget, setBotBudget] = useState(10)
  const pushToast = useToastStore((s) => s.push)

  return (
    <div>
      <Breadcrumb items={[{ label: 'Budgets' }]} />
      <h1 className="mb-6">Budgets</h1>

      <div className="mb-8 grid gap-4 md:grid-cols-3">
        <BudgetCard
          title="Budget global (€ / mois)"
          value={globalBudget}
          onChange={setGlobalBudget}
          onSave={() => pushToast('Budget global sauvegardé (mock)', 'success')}
        />
        <BudgetCard
          title="Budget par produit (ex. Charizard)"
          value={productBudget}
          onChange={setProductBudget}
          onSave={() => pushToast('Budget produit sauvegardé (mock)', 'success')}
        />
        <BudgetCard
          title="Budget par bot (€)"
          value={botBudget}
          onChange={setBotBudget}
          onSave={() => pushToast('Budget bot sauvegardé (mock)', 'success')}
        />
      </div>

      <div
        className="mb-6 rounded-xl border p-4"
        style={{ borderColor: 'var(--tcg-border)', background: 'var(--tcg-surface)' }}
      >
        <h2 className="mb-2 text-base font-semibold">Alertes</h2>
        <p className="text-sm" style={{ color: 'var(--tcg-muted)' }}>
          Notification simulée si dépassement — aucune logique serveur.
        </p>
        <button
          type="button"
          className="mt-3 rounded-lg px-4 py-2 text-sm font-semibold text-black"
          style={{ background: 'var(--tcg-accent)' }}
          onClick={() => pushToast('Alerte de test : proche du plafond (mock)', 'info')}
        >
          Tester une alerte
        </button>
      </div>

      <h2 className="mb-3">Historique des dépenses</h2>
      <div
        className="overflow-x-auto rounded-xl border"
        style={{ borderColor: 'var(--tcg-border)', background: 'var(--tcg-surface)' }}
      >
        <table className="min-w-full text-left text-sm">
          <thead>
            <tr className="border-b" style={{ borderColor: 'var(--tcg-border)' }}>
              <th className="px-4 py-3">Date</th>
              <th className="px-4 py-3">Produit</th>
              <th className="px-4 py-3">Montant</th>
              <th className="px-4 py-3">Bot</th>
            </tr>
          </thead>
          <tbody>
            {mockExpenses.map((e) => (
              <tr key={e.id} className="border-b last:border-0" style={{ borderColor: 'var(--tcg-border)' }}>
                <td className="px-4 py-3">{e.date}</td>
                <td className="px-4 py-3 font-medium">{e.product}</td>
                <td className="px-4 py-3">{e.amount} €</td>
                <td className="px-4 py-3">{e.bot}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  )
}

function BudgetCard({
  title,
  value,
  onChange,
  onSave,
}: {
  title: string
  value: number
  onChange: (n: number) => void
  onSave: () => void
}) {
  return (
    <div className="rounded-xl border p-4" style={{ borderColor: 'var(--tcg-border)', background: 'var(--tcg-surface)' }}>
      <p className="text-sm font-medium">{title}</p>
      <input
        type="number"
        className="mt-2 w-full rounded-lg border px-3 py-2"
        style={{ borderColor: 'var(--tcg-border)', background: 'var(--tcg-bg)', color: 'var(--tcg-text)' }}
        value={value}
        onChange={(e) => onChange(Number(e.target.value))}
      />
      <button
        type="button"
        className="mt-3 w-full rounded-lg border px-3 py-2 text-sm"
        style={{ borderColor: 'var(--tcg-border)' }}
        onClick={onSave}
      >
        Sauvegarder
      </button>
    </div>
  )
}
