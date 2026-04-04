import { useState } from 'react'
import { Breadcrumb } from '../components/Breadcrumb'
import { mockNotifHistory } from '../data/mockData'
import { useToastStore } from '../stores/toastStore'

export function Notifications() {
  const [discord, setDiscord] = useState(true)
  const [sms, setSms] = useState(false)
  const [email, setEmail] = useState(true)
  const [webhook, setWebhook] = useState('https://discord.com/api/webhooks/…')
  const [phone, setPhone] = useState('')
  const [smtpHost, setSmtpHost] = useState('smtp.example.com')
  const [smtpUser, setSmtpUser] = useState('')
  const pushToast = useToastStore((s) => s.push)

  return (
    <div>
      <Breadcrumb items={[{ label: 'Notifications' }]} />
      <h1 className="mb-6">Notifications</h1>

      <section
        className="mb-8 rounded-xl border p-5"
        style={{ borderColor: 'var(--tcg-border)', background: 'var(--tcg-surface)' }}
      >
        <h2 className="mb-4 text-base font-semibold">Canaux</h2>
        <div className="space-y-4">
          <label className="flex items-center justify-between gap-4">
            <span className="text-sm font-medium">Discord</span>
            <input type="checkbox" checked={discord} onChange={(e) => setDiscord(e.target.checked)} />
          </label>
          <label className="flex items-center justify-between gap-4">
            <span className="text-sm font-medium">SMS</span>
            <input type="checkbox" checked={sms} onChange={(e) => setSms(e.target.checked)} />
          </label>
          <label className="flex items-center justify-between gap-4">
            <span className="text-sm font-medium">Email</span>
            <input type="checkbox" checked={email} onChange={(e) => setEmail(e.target.checked)} />
          </label>
        </div>
        <div className="mt-6 space-y-3">
          <div>
            <label className="text-sm font-medium">Webhook Discord</label>
            <input
              className="mt-1 w-full rounded-lg border px-3 py-2 text-sm"
              style={{ borderColor: 'var(--tcg-border)', background: 'var(--tcg-bg)', color: 'var(--tcg-text)' }}
              value={webhook}
              onChange={(e) => setWebhook(e.target.value)}
            />
          </div>
          <div>
            <label className="text-sm font-medium">Téléphone (SMS)</label>
            <input
              className="mt-1 w-full rounded-lg border px-3 py-2 text-sm"
              style={{ borderColor: 'var(--tcg-border)', background: 'var(--tcg-bg)', color: 'var(--tcg-text)' }}
              value={phone}
              onChange={(e) => setPhone(e.target.value)}
              placeholder="+33…"
            />
          </div>
          <div className="grid gap-3 sm:grid-cols-2">
            <div>
              <label className="text-sm font-medium">SMTP hôte</label>
              <input
                className="mt-1 w-full rounded-lg border px-3 py-2 text-sm"
                style={{ borderColor: 'var(--tcg-border)', background: 'var(--tcg-bg)', color: 'var(--tcg-text)' }}
                value={smtpHost}
                onChange={(e) => setSmtpHost(e.target.value)}
              />
            </div>
            <div>
              <label className="text-sm font-medium">SMTP utilisateur</label>
              <input
                className="mt-1 w-full rounded-lg border px-3 py-2 text-sm"
                style={{ borderColor: 'var(--tcg-border)', background: 'var(--tcg-bg)', color: 'var(--tcg-text)' }}
                value={smtpUser}
                onChange={(e) => setSmtpUser(e.target.value)}
              />
            </div>
          </div>
        </div>
        <button
          type="button"
          className="mt-6 rounded-lg px-4 py-2.5 text-sm font-semibold text-black"
          style={{ background: 'var(--tcg-accent)' }}
          onClick={() => pushToast('Configuration notifications enregistrée (mock)', 'success')}
        >
          Enregistrer
        </button>
      </section>

      <h2 className="mb-3">Historique</h2>
      <div
        className="overflow-x-auto rounded-xl border"
        style={{ borderColor: 'var(--tcg-border)', background: 'var(--tcg-surface)' }}
      >
        <table className="min-w-full text-left text-sm">
          <thead>
            <tr className="border-b" style={{ borderColor: 'var(--tcg-border)' }}>
              <th className="px-4 py-3">Date</th>
              <th className="px-4 py-3">Canal</th>
              <th className="px-4 py-3">Message</th>
            </tr>
          </thead>
          <tbody>
            {mockNotifHistory.map((h) => (
              <tr key={h.id} className="border-b last:border-0" style={{ borderColor: 'var(--tcg-border)' }}>
                <td className="px-4 py-3 whitespace-nowrap">{h.date}</td>
                <td className="px-4 py-3">{h.channel}</td>
                <td className="px-4 py-3">{h.message}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  )
}
