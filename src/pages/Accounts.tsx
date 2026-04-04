import { useForm } from 'react-hook-form'
import { useState } from 'react'
import { Breadcrumb } from '../components/Breadcrumb'
import { Modal } from '../components/Modal'
import {
  CAPTCHA_SOLVERS,
  mockAccounts,
  PROXY_OPTIONS,
  SITES,
  type AccountRow,
  type Site,
} from '../data/mockData'
import { mockSave } from '../services/mockApi'
import { useToastStore } from '../stores/toastStore'

type Form = {
  email: string
  password: string
  site: Site
  proxy: string
  captcha: (typeof CAPTCHA_SOLVERS)[number]
}

export function Accounts() {
  const [rows, setRows] = useState<AccountRow[]>(mockAccounts)
  const [open, setOpen] = useState(false)
  const pushToast = useToastStore((s) => s.push)
  const form = useForm<Form>({
    defaultValues: {
      email: '',
      password: '',
      site: 'FNAC',
      proxy: PROXY_OPTIONS[0],
      captcha: '2Captcha',
    },
  })

  const onSave = form.handleSubmit(async (data) => {
    const row: AccountRow = {
      id: crypto.randomUUID(),
      email: data.email,
      site: data.site,
      proxy: data.proxy,
      status: 'ok',
      lastUsed: '—',
    }
    await mockSave(row)
    setRows((r) => [row, ...r])
    pushToast('Compte ajouté (mock).', 'success')
    setOpen(false)
    form.reset()
  })

  return (
    <div>
      <Breadcrumb items={[{ label: 'Comptes' }]} />
      <div className="mb-6 flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
        <h1>Comptes</h1>
        <button
          type="button"
          onClick={() => setOpen(true)}
          className="rounded-lg px-4 py-2.5 text-sm font-semibold text-black"
          style={{ background: 'var(--tcg-accent)' }}
        >
          Ajouter un compte
        </button>
      </div>

      <div
        className="overflow-x-auto rounded-xl border"
        style={{ borderColor: 'var(--tcg-border)', background: 'var(--tcg-surface)' }}
      >
        <table className="min-w-full text-left text-sm">
          <thead>
            <tr className="border-b" style={{ borderColor: 'var(--tcg-border)' }}>
              <th className="px-4 py-3">Email</th>
              <th className="px-4 py-3">Site</th>
              <th className="px-4 py-3">Proxy</th>
              <th className="px-4 py-3">Statut</th>
              <th className="px-4 py-3">Dernière utilisation</th>
              <th className="px-4 py-3">Actions</th>
            </tr>
          </thead>
          <tbody>
            {rows.map((a) => (
              <tr key={a.id} className="border-b last:border-0" style={{ borderColor: 'var(--tcg-border)' }}>
                <td className="px-4 py-3 font-medium">{a.email}</td>
                <td className="px-4 py-3">{a.site}</td>
                <td className="px-4 py-3">{a.proxy}</td>
                <td className="px-4 py-3">
                  {a.status === 'ok' ? '✓' : a.status === 'warn' ? '⚠' : '✗'}
                </td>
                <td className="px-4 py-3" style={{ color: 'var(--tcg-muted)' }}>
                  {a.lastUsed}
                </td>
                <td className="px-4 py-3">
                  <div className="flex flex-wrap gap-2 text-xs">
                    <button type="button" className="underline" style={{ color: 'var(--tcg-accent)' }} onClick={() => pushToast('Édition (mock)', 'info')}>
                      Éditer
                    </button>
                    <button
                      type="button"
                      className="underline"
                      onClick={() => {
                        setRows((r) => r.map((x) => (x.id === a.id ? { ...x, status: 'ko' as const } : x)))
                        pushToast('Compte désactivé (mock)', 'success')
                      }}
                    >
                      Désactiver
                    </button>
                  </div>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      <Modal
        open={open}
        onClose={() => setOpen(false)}
        title="Ajouter un compte"
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
              onClick={() => void onSave()}
            >
              Sauvegarder
            </button>
          </>
        }
      >
        <div className="space-y-3">
          <div>
            <label className="text-sm font-medium">Email</label>
            <input
              className="mt-1 w-full rounded-lg border px-3 py-2"
              style={{ borderColor: 'var(--tcg-border)', background: 'var(--tcg-bg)', color: 'var(--tcg-text)' }}
              type="email"
              {...form.register('email', { required: true })}
            />
          </div>
          <div>
            <label className="text-sm font-medium">Mot de passe</label>
            <input
              className="mt-1 w-full rounded-lg border px-3 py-2"
              style={{ borderColor: 'var(--tcg-border)', background: 'var(--tcg-bg)', color: 'var(--tcg-text)' }}
              type="password"
              {...form.register('password', { required: true, minLength: 6 })}
            />
          </div>
          <div>
            <label className="text-sm font-medium">Site</label>
            <select
              className="mt-1 w-full rounded-lg border px-3 py-2"
              style={{ borderColor: 'var(--tcg-border)', background: 'var(--tcg-bg)', color: 'var(--tcg-text)' }}
              {...form.register('site')}
            >
              {SITES.map((s) => (
                <option key={s} value={s}>
                  {s}
                </option>
              ))}
            </select>
          </div>
          <div>
            <label className="text-sm font-medium">Proxy</label>
            <select
              className="mt-1 w-full rounded-lg border px-3 py-2"
              style={{ borderColor: 'var(--tcg-border)', background: 'var(--tcg-bg)', color: 'var(--tcg-text)' }}
              {...form.register('proxy')}
            >
              {PROXY_OPTIONS.map((p) => (
                <option key={p} value={p}>
                  {p}
                </option>
              ))}
            </select>
          </div>
          <div>
            <label className="text-sm font-medium">Solveur CAPTCHA</label>
            <select
              className="mt-1 w-full rounded-lg border px-3 py-2"
              style={{ borderColor: 'var(--tcg-border)', background: 'var(--tcg-bg)', color: 'var(--tcg-text)' }}
              {...form.register('captcha')}
            >
              {CAPTCHA_SOLVERS.map((c) => (
                <option key={c} value={c}>
                  {c}
                </option>
              ))}
            </select>
          </div>
        </div>
      </Modal>
    </div>
  )
}
