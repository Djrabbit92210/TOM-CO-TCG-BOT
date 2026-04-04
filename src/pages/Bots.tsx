import { useForm } from 'react-hook-form'
import { useMemo, useState } from 'react'
import { Breadcrumb } from '../components/Breadcrumb'
import { Modal } from '../components/Modal'
import { mockAccounts, mockBotLogs, mockBots, mockProducts, type BotRow } from '../data/mockData'
import { mockSave } from '../services/mockApi'
import { useToastStore } from '../stores/toastStore'

type Tab = 'list' | 'logs'

type BotForm = {
  name: string
  productId: string
  accountId: string
  delaySec: number
  retries: number
  randomize: boolean
}

export function Bots() {
  const [tab, setTab] = useState<Tab>('list')
  const [bots, setBots] = useState<BotRow[]>(mockBots)
  const [open, setOpen] = useState(false)
  const [logFilter, setLogFilter] = useState({ date: '', level: 'all', q: '' })
  const pushToast = useToastStore((s) => s.push)
  const form = useForm<BotForm>({
    defaultValues: {
      name: '',
      productId: mockProducts[0]?.id ?? '',
      accountId: mockAccounts[0]?.id ?? '',
      delaySec: 10,
      retries: 3,
      randomize: true,
    },
  })

  const filteredLogs = useMemo(() => {
    return mockBotLogs.filter((l) => {
      if (logFilter.level !== 'all' && l.level !== logFilter.level) return false
      if (logFilter.date && !l.ts.startsWith(logFilter.date)) return false
      if (logFilter.q && !l.message.toLowerCase().includes(logFilter.q.toLowerCase())) return false
      return true
    })
  }, [logFilter])

  const setStatus = (id: string, status: BotRow['status']) => {
    setBots((b) => b.map((x) => (x.id === id ? { ...x, status } : x)))
    pushToast(`Bot ${status} (mock)`, 'success')
  }

  const onStart = form.handleSubmit(async (data) => {
    const product = mockProducts.find((p) => p.id === data.productId)
    const account = mockAccounts.find((a) => a.id === data.accountId)
    const bot: BotRow = {
      id: crypto.randomUUID(),
      name: data.name || 'Nouveau bot',
      site: product?.sites[0] ?? 'FNAC',
      accountEmail: account?.email ?? '—',
      proxy: account?.proxy ?? '—',
      status: 'running',
      lastCheck: new Date().toISOString().slice(0, 16).replace('T', ' '),
    }
    await mockSave({ ...data, bot })
    setBots((b) => [bot, ...b])
    pushToast('Bot démarré (mock).', 'success')
    setOpen(false)
  })

  const exportCsv = () => {
    const header = 'Date,Niveau,Message\n'
    const body = filteredLogs.map((l) => `${l.ts},${l.level},"${l.message.replace(/"/g, '""')}"`).join('\n')
    const blob = new Blob([header + body], { type: 'text/csv;charset=utf-8' })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = 'bot-logs.csv'
    a.click()
    URL.revokeObjectURL(url)
    pushToast('CSV exporté.', 'success')
  }

  return (
    <div>
      <Breadcrumb items={[{ label: 'Bots' }]} />
      <div className="mb-6 flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
        <h1>Bots</h1>
        <button
          type="button"
          onClick={() => setOpen(true)}
          className="rounded-lg px-4 py-2.5 text-sm font-semibold text-black"
          style={{ background: 'var(--tcg-accent)' }}
        >
          Configurer un bot
        </button>
      </div>

      <div className="mb-4 flex gap-2 border-b" style={{ borderColor: 'var(--tcg-border)' }}>
        <button
          type="button"
          className={[
            'border-b-2 px-4 py-2 text-sm font-medium',
            tab === 'list' ? 'border-[var(--tcg-accent)]' : 'border-transparent opacity-70',
          ].join(' ')}
          onClick={() => setTab('list')}
        >
          Liste
        </button>
        <button
          type="button"
          className={[
            'border-b-2 px-4 py-2 text-sm font-medium',
            tab === 'logs' ? 'border-[var(--tcg-accent)]' : 'border-transparent opacity-70',
          ].join(' ')}
          onClick={() => setTab('logs')}
        >
          Logs
        </button>
      </div>

      {tab === 'list' ? (
        <div
          className="overflow-x-auto rounded-xl border"
          style={{ borderColor: 'var(--tcg-border)', background: 'var(--tcg-surface)' }}
        >
          <table className="min-w-full text-left text-sm">
            <thead>
              <tr className="border-b" style={{ borderColor: 'var(--tcg-border)' }}>
                <th className="px-4 py-3">Nom</th>
                <th className="px-4 py-3">Site</th>
                <th className="px-4 py-3">Compte</th>
                <th className="px-4 py-3">Proxy</th>
                <th className="px-4 py-3">Statut</th>
                <th className="px-4 py-3">Dernier check</th>
                <th className="px-4 py-3">Actions</th>
              </tr>
            </thead>
            <tbody>
              {bots.map((b) => (
                <tr key={b.id} className="border-b last:border-0" style={{ borderColor: 'var(--tcg-border)' }}>
                  <td className="px-4 py-3 font-medium">{b.name}</td>
                  <td className="px-4 py-3">{b.site}</td>
                  <td className="px-4 py-3">{b.accountEmail}</td>
                  <td className="px-4 py-3">{b.proxy}</td>
                  <td className="px-4 py-3">{b.status}</td>
                  <td className="px-4 py-3" style={{ color: 'var(--tcg-muted)' }}>
                    {b.lastCheck}
                  </td>
                  <td className="px-4 py-3">
                    <div className="flex flex-wrap gap-2 text-xs">
                      <button type="button" className="underline" onClick={() => setStatus(b.id, 'running')}>
                        Lancer
                      </button>
                      <button type="button" className="underline" onClick={() => setStatus(b.id, 'paused')}>
                        Pause
                      </button>
                      <button type="button" className="underline" onClick={() => setStatus(b.id, 'stopped')}>
                        Arrêter
                      </button>
                      <button type="button" className="underline" style={{ color: 'var(--tcg-accent)' }} onClick={() => pushToast('Check forcé (mock)', 'info')}>
                        Forcer check
                      </button>
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      ) : (
        <div>
          <div className="mb-4 flex flex-wrap items-end gap-3">
            <div>
              <label className="text-xs font-medium" style={{ color: 'var(--tcg-muted)' }}>
                Date
              </label>
              <input
                type="date"
                className="mt-1 block rounded-lg border px-3 py-2 text-sm"
                style={{ borderColor: 'var(--tcg-border)', background: 'var(--tcg-surface)', color: 'var(--tcg-text)' }}
                value={logFilter.date}
                onChange={(e) => setLogFilter((f) => ({ ...f, date: e.target.value }))}
              />
            </div>
            <div>
              <label className="text-xs font-medium" style={{ color: 'var(--tcg-muted)' }}>
                Niveau
              </label>
              <select
                className="mt-1 block rounded-lg border px-3 py-2 text-sm"
                style={{ borderColor: 'var(--tcg-border)', background: 'var(--tcg-surface)', color: 'var(--tcg-text)' }}
                value={logFilter.level}
                onChange={(e) => setLogFilter((f) => ({ ...f, level: e.target.value }))}
              >
                <option value="all">Tous</option>
                <option value="Info">Info</option>
                <option value="Warning">Warning</option>
                <option value="Error">Error</option>
              </select>
            </div>
            <div className="min-w-[200px] flex-1">
              <label className="text-xs font-medium" style={{ color: 'var(--tcg-muted)' }}>
                Recherche
              </label>
              <input
                className="mt-1 w-full rounded-lg border px-3 py-2 text-sm"
                style={{ borderColor: 'var(--tcg-border)', background: 'var(--tcg-surface)', color: 'var(--tcg-text)' }}
                value={logFilter.q}
                onChange={(e) => setLogFilter((f) => ({ ...f, q: e.target.value }))}
                placeholder="Mot-clé…"
              />
            </div>
            <button
              type="button"
              className="rounded-lg px-4 py-2 text-sm font-semibold text-black"
              style={{ background: 'var(--tcg-accent)' }}
              onClick={exportCsv}
            >
              Exporter CSV
            </button>
          </div>
          <div
            className="overflow-x-auto rounded-xl border"
            style={{ borderColor: 'var(--tcg-border)', background: 'var(--tcg-surface)' }}
          >
            <table className="min-w-full text-left text-sm">
              <thead>
                <tr className="border-b" style={{ borderColor: 'var(--tcg-border)' }}>
                  <th className="px-4 py-3">Date</th>
                  <th className="px-4 py-3">Niveau</th>
                  <th className="px-4 py-3">Message</th>
                </tr>
              </thead>
              <tbody>
                {filteredLogs.map((l) => (
                  <tr key={l.id} className="border-b last:border-0" style={{ borderColor: 'var(--tcg-border)' }}>
                    <td className="px-4 py-3 whitespace-nowrap">{l.ts}</td>
                    <td className="px-4 py-3">{l.level}</td>
                    <td className="px-4 py-3">{l.message}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}

      <Modal
        open={open}
        onClose={() => setOpen(false)}
        title="Configurer un bot"
        footer={
          <>
            <button
              type="button"
              className="rounded-lg border px-4 py-2 text-sm"
              style={{ borderColor: 'var(--tcg-border)' }}
              onClick={() => setOpen(false)}
            >
              Annuler
            </button>
            <button
              type="button"
              className="rounded-lg px-4 py-2 text-sm font-semibold text-black"
              style={{ background: 'var(--tcg-accent)' }}
              onClick={() => void onStart()}
            >
              Démarrer
            </button>
          </>
        }
      >
        <div className="space-y-3">
          <div>
            <label className="text-sm font-medium">Nom du bot</label>
            <input
              className="mt-1 w-full rounded-lg border px-3 py-2"
              style={{ borderColor: 'var(--tcg-border)', background: 'var(--tcg-bg)', color: 'var(--tcg-text)' }}
              {...form.register('name', { required: true })}
            />
          </div>
          <div>
            <label className="text-sm font-medium">Produit</label>
            <select
              className="mt-1 w-full rounded-lg border px-3 py-2"
              style={{ borderColor: 'var(--tcg-border)', background: 'var(--tcg-bg)', color: 'var(--tcg-text)' }}
              {...form.register('productId')}
            >
              {mockProducts.map((p) => (
                <option key={p.id} value={p.id}>
                  {p.name}
                </option>
              ))}
            </select>
          </div>
          <div>
            <label className="text-sm font-medium">Compte</label>
            <select
              className="mt-1 w-full rounded-lg border px-3 py-2"
              style={{ borderColor: 'var(--tcg-border)', background: 'var(--tcg-bg)', color: 'var(--tcg-text)' }}
              {...form.register('accountId')}
            >
              {mockAccounts.map((a) => (
                <option key={a.id} value={a.id}>
                  {a.email} — {a.site}
                </option>
              ))}
            </select>
          </div>
          <div className="grid grid-cols-2 gap-3">
            <div>
              <label className="text-sm font-medium">Délai (s)</label>
              <input
                type="number"
                className="mt-1 w-full rounded-lg border px-3 py-2"
                style={{ borderColor: 'var(--tcg-border)', background: 'var(--tcg-bg)', color: 'var(--tcg-text)' }}
                {...form.register('delaySec', { valueAsNumber: true, min: 1 })}
              />
            </div>
            <div>
              <label className="text-sm font-medium">Retries</label>
              <input
                type="number"
                className="mt-1 w-full rounded-lg border px-3 py-2"
                style={{ borderColor: 'var(--tcg-border)', background: 'var(--tcg-bg)', color: 'var(--tcg-text)' }}
                {...form.register('retries', { valueAsNumber: true, min: 0 })}
              />
            </div>
          </div>
          <label className="flex items-center gap-2 text-sm">
            <input type="checkbox" {...form.register('randomize')} />
            Randomisation
          </label>
        </div>
      </Modal>
    </div>
  )
}
