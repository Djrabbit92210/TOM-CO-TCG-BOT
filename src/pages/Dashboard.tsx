import { Bot, CreditCard, Package, Pause, Play, Plus, Sparkles } from 'lucide-react'
import type { LucideIcon } from 'lucide-react'
import type { ReactNode } from 'react'
import { useMemo, useState } from 'react'
import {
  CartesianGrid,
  Cell,
  Line,
  LineChart,
  Pie,
  PieChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from 'recharts'
import { Breadcrumb } from '../components/Breadcrumb'
import { Modal } from '../components/Modal'
import {
  mockBots,
  recentAlerts,
  recentPurchases,
  stockBySite,
  stockTrend,
} from '../data/mockData'
import { mockSave } from '../services/mockApi'
import { useToastStore } from '../stores/toastStore'

const PIE_COLORS = ['#7fff00', '#0078ff', '#a78bfa', '#fbbf24']

export function Dashboard() {
  const [bots, setBots] = useState(mockBots)
  const [addOpen, setAddOpen] = useState(false)
  const [productName, setProductName] = useState('')
  const pushToast = useToastStore((s) => s.push)

  const activeCount = useMemo(() => bots.filter((b) => b.status === 'running').length, [bots])

  const toggleBot = (id: string) => {
    setBots((prev) =>
      prev.map((b) =>
        b.id === id
          ? { ...b, status: b.status === 'running' ? ('paused' as const) : ('running' as const) }
          : b,
      ),
    )
    pushToast('Statut du bot mis à jour (simulation).', 'success')
  }

  const saveQuickProduct = async () => {
    await mockSave({ name: productName })
    pushToast('Produit enregistré (mock).', 'success')
    setAddOpen(false)
    setProductName('')
  }

  return (
    <div>
      <Breadcrumb items={[{ label: 'Tableau de bord' }]} />
      <div className="mb-6 flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
        <h1>Tableau de bord</h1>
        <button
          type="button"
          onClick={() => setAddOpen(true)}
          className="inline-flex items-center justify-center gap-2 rounded-lg px-4 py-2.5 text-sm font-semibold text-black transition-colors"
          style={{ background: 'var(--tcg-accent)' }}
        >
          <Plus className="h-4 w-4" aria-hidden />
          Ajouter un produit
        </button>
      </div>

      <div className="mb-8 grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
        <StatCard
          title="Bots actifs"
          value={String(activeCount)}
          icon={Bot}
          hint="En cours d’exécution"
        />
        <StatCard title="Produits surveillés" value="12" icon={Package} hint="Mock UI" />
        <StatCard title="Succès récents" value={String(recentPurchases.length)} icon={Sparkles} hint="5 derniers" />
        <StatCard title="Alertes en attente" value="3" icon={CreditCard} hint="Non lues (mock)" />
      </div>

      <div className="mb-8 grid gap-6 lg:grid-cols-2">
        <ChartCard title="Répartition des stocks par site">
          <div className="h-64 w-full">
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie data={stockBySite} dataKey="value" nameKey="name" cx="50%" cy="50%" outerRadius={88} label>
                  {stockBySite.map((_, i) => (
                    <Cell key={stockBySite[i].name} fill={PIE_COLORS[i % PIE_COLORS.length]} />
                  ))}
                </Pie>
                <Tooltip />
              </PieChart>
            </ResponsiveContainer>
          </div>
        </ChartCard>
        <ChartCard title="Évolution des stocks (7 jours)">
          <div className="h-64 w-full">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={stockTrend}>
                <CartesianGrid strokeDasharray="3 3" stroke="var(--tcg-border)" />
                <XAxis dataKey="day" stroke="var(--tcg-muted)" fontSize={12} />
                <YAxis stroke="var(--tcg-muted)" fontSize={12} />
                <Tooltip
                  contentStyle={{
                    background: 'var(--tcg-surface)',
                    border: '1px solid var(--tcg-border)',
                    borderRadius: 8,
                  }}
                />
                <Line type="monotone" dataKey="stock" stroke="var(--tcg-accent)" strokeWidth={2} dot={false} />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </ChartCard>
      </div>

      <div className="grid gap-6 xl:grid-cols-3">
        <section className="xl:col-span-2">
          <h2 className="mb-3">Bots actifs</h2>
          <div
            className="overflow-x-auto rounded-xl border"
            style={{ borderColor: 'var(--tcg-border)', background: 'var(--tcg-surface)' }}
          >
            <table className="min-w-full text-left text-sm">
              <thead>
                <tr className="border-b" style={{ borderColor: 'var(--tcg-border)' }}>
                  <th className="px-4 py-3 font-medium">Nom</th>
                  <th className="px-4 py-3 font-medium">Site</th>
                  <th className="px-4 py-3 font-medium">Statut</th>
                  <th className="px-4 py-3 font-medium">Dernier check</th>
                  <th className="px-4 py-3 font-medium">Actions</th>
                </tr>
              </thead>
              <tbody>
                {bots.map((b) => (
                  <tr key={b.id} className="border-b last:border-0" style={{ borderColor: 'var(--tcg-border)' }}>
                    <td className="px-4 py-3 font-medium">{b.name}</td>
                    <td className="px-4 py-3">{b.site}</td>
                    <td className="px-4 py-3">
                      <StatusPill status={b.status} />
                    </td>
                    <td className="px-4 py-3" style={{ color: 'var(--tcg-muted)' }}>
                      {b.lastCheck}
                    </td>
                    <td className="px-4 py-3">
                      <button
                        type="button"
                        onClick={() => toggleBot(b.id)}
                        className="inline-flex items-center gap-1 rounded-lg border px-2 py-1 text-xs font-medium transition-colors"
                        style={{ borderColor: 'var(--tcg-border)' }}
                      >
                        {b.status === 'running' ? (
                          <>
                            <Pause className="h-3.5 w-3.5" /> Pause
                          </>
                        ) : (
                          <>
                            <Play className="h-3.5 w-3.5" /> Relancer
                          </>
                        )}
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </section>
        <section>
          <h2 className="mb-3">Alertes récentes</h2>
          <ul
            className="space-y-3 rounded-xl border p-4"
            style={{ borderColor: 'var(--tcg-border)', background: 'var(--tcg-surface)' }}
          >
            {recentAlerts.map((a) => (
              <li key={a.id} className="text-sm">
                <p className="font-medium">{a.text}</p>
                <p className="text-xs" style={{ color: 'var(--tcg-muted)' }}>
                  {a.channel}
                </p>
              </li>
            ))}
          </ul>
          <h3 className="mb-2 mt-6 text-base font-semibold">Derniers achats réussis</h3>
          <ul className="space-2 text-sm" style={{ color: 'var(--tcg-muted)' }}>
            {recentPurchases.map((p) => (
              <li key={p.id} className="flex justify-between gap-2 border-b py-2 last:border-0" style={{ borderColor: 'var(--tcg-border)' }}>
                <span style={{ color: 'var(--tcg-text)' }}>{p.label}</span>
                <span className="shrink-0 text-xs">{p.time}</span>
              </li>
            ))}
          </ul>
        </section>
      </div>

      <Modal
        open={addOpen}
        onClose={() => setAddOpen(false)}
        title="Ajouter un produit (rapide)"
        footer={
          <>
            <button
              type="button"
              className="rounded-lg border px-4 py-2 text-sm"
              style={{ borderColor: 'var(--tcg-border)' }}
              onClick={() => setAddOpen(false)}
            >
              Annuler
            </button>
            <button
              type="button"
              className="rounded-lg px-4 py-2 text-sm font-semibold text-black"
              style={{ background: 'var(--tcg-accent)' }}
              onClick={() => void saveQuickProduct()}
            >
              Sauvegarder
            </button>
          </>
        }
      >
        <label className="block text-sm font-medium">Nom du produit</label>
        <input
          className="mt-1 w-full rounded-lg border px-3 py-2"
          style={{ borderColor: 'var(--tcg-border)', background: 'var(--tcg-bg)', color: 'var(--tcg-text)' }}
          value={productName}
          onChange={(e) => setProductName(e.target.value)}
          placeholder="Ex. Display SV9"
        />
        <p className="mt-2 text-xs" style={{ color: 'var(--tcg-muted)' }}>
          Pour le formulaire complet, utilisez la page Produits.
        </p>
      </Modal>
    </div>
  )
}

function StatCard({
  title,
  value,
  hint,
  icon: Icon,
}: {
  title: string
  value: string
  hint: string
  icon: LucideIcon
}) {
  return (
    <div
      className="rounded-xl border p-5 transition-transform hover:-translate-y-0.5"
      style={{ borderColor: 'var(--tcg-border)', background: 'var(--tcg-surface)' }}
    >
      <div className="flex items-start justify-between gap-3">
        <div>
          <p className="text-sm" style={{ color: 'var(--tcg-muted)' }}>
            {title}
          </p>
          <p className="mt-1 text-2xl font-semibold">{value}</p>
          <p className="mt-1 text-xs" style={{ color: 'var(--tcg-muted)' }}>
            {hint}
          </p>
        </div>
        <div
          className="rounded-lg p-2"
          style={{ background: 'color-mix(in srgb, var(--tcg-accent) 15%, transparent)' }}
        >
          <Icon className="h-6 w-6" style={{ color: 'var(--tcg-accent)' }} aria-hidden />
        </div>
      </div>
    </div>
  )
}

function ChartCard({ title, children }: { title: string; children: ReactNode }) {
  return (
    <div className="rounded-xl border p-4" style={{ borderColor: 'var(--tcg-border)', background: 'var(--tcg-surface)' }}>
      <h2 className="mb-4">{title}</h2>
      {children}
    </div>
  )
}

function StatusPill({ status }: { status: 'running' | 'paused' | 'stopped' }) {
  const label = status === 'running' ? 'Actif' : status === 'paused' ? 'Pause' : 'Arrêté'
  const color =
    status === 'running' ? 'var(--tcg-success)' : status === 'paused' ? '#fbbf24' : 'var(--tcg-muted)'
  return (
    <span className="inline-flex items-center gap-1 text-xs font-medium" style={{ color }}>
      <span className="h-2 w-2 rounded-full" style={{ background: color }} aria-hidden />
      {label}
    </span>
  )
}
