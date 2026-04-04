import { Navigate } from 'react-router-dom'
import { Breadcrumb } from '../components/Breadcrumb'
import { useAuthStore } from '../stores/authStore'
import { useSettingsStore, type Lang, type ThemeMode } from '../stores/settingsStore'
import { useToastStore } from '../stores/toastStore'

export function Settings() {
  const user = useAuthStore((s) => s.user)
  const { settings, setSettings } = useSettingsStore()
  const pushToast = useToastStore((s) => s.push)

  if (!user?.isAdmin) {
    return <Navigate to="/" replace />
  }

  const exportConfig = () => {
    const blob = new Blob([JSON.stringify({ settings }, null, 2)], { type: 'application/json' })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = 'tcg-scalper-config.json'
    a.click()
    URL.revokeObjectURL(url)
    pushToast('Configuration exportée.', 'success')
  }

  const importConfig = () => {
    const input = document.createElement('input')
    input.type = 'file'
    input.accept = 'application/json'
    input.onchange = () => {
      const file = input.files?.[0]
      if (!file) return
      file.text().then((text) => {
        try {
          const data = JSON.parse(text) as { settings?: typeof settings }
          if (data.settings) {
            setSettings(data.settings)
            pushToast('Configuration importée.', 'success')
          } else {
            pushToast('Fichier invalide.', 'error')
          }
        } catch {
          pushToast('JSON invalide.', 'error')
        }
      })
    }
    input.click()
  }

  return (
    <div>
      <Breadcrumb items={[{ label: 'Paramètres' }]} />
      <h1 className="mb-2">Paramètres</h1>
      <p className="mb-6 text-sm" style={{ color: 'var(--tcg-muted)' }}>
        Réservé aux comptes administrateur (email contenant « admin » à la connexion).
      </p>

      <div
        className="max-w-xl space-y-6 rounded-xl border p-6"
        style={{ borderColor: 'var(--tcg-border)', background: 'var(--tcg-surface)' }}
      >
        <div>
          <label className="text-sm font-medium">Délai entre checks (secondes)</label>
          <input
            type="number"
            min={1}
            className="mt-1 w-full rounded-lg border px-3 py-2"
            style={{ borderColor: 'var(--tcg-border)', background: 'var(--tcg-bg)', color: 'var(--tcg-text)' }}
            value={settings.checkIntervalSec}
            onChange={(e) => setSettings({ checkIntervalSec: Number(e.target.value) })}
          />
        </div>
        <div>
          <label className="text-sm font-medium">Nombre max de bots simultanés</label>
          <input
            type="number"
            min={1}
            className="mt-1 w-full rounded-lg border px-3 py-2"
            style={{ borderColor: 'var(--tcg-border)', background: 'var(--tcg-bg)', color: 'var(--tcg-text)' }}
            value={settings.maxConcurrentBots}
            onChange={(e) => setSettings({ maxConcurrentBots: Number(e.target.value) })}
          />
        </div>
        <div>
          <label className="text-sm font-medium">Langue</label>
          <select
            className="mt-1 w-full rounded-lg border px-3 py-2"
            style={{ borderColor: 'var(--tcg-border)', background: 'var(--tcg-bg)', color: 'var(--tcg-text)' }}
            value={settings.lang}
            onChange={(e) => setSettings({ lang: e.target.value as Lang })}
          >
            <option value="fr">Français</option>
            <option value="en">English</option>
          </select>
        </div>
        <div>
          <label className="text-sm font-medium">Thème</label>
          <select
            className="mt-1 w-full rounded-lg border px-3 py-2"
            style={{ borderColor: 'var(--tcg-border)', background: 'var(--tcg-bg)', color: 'var(--tcg-text)' }}
            value={settings.theme}
            onChange={(e) => setSettings({ theme: e.target.value as ThemeMode })}
          >
            <option value="dark">Sombre</option>
            <option value="light">Clair</option>
          </select>
        </div>
        <div className="flex flex-wrap gap-2">
          <button
            type="button"
            className="rounded-lg border px-4 py-2 text-sm"
            style={{ borderColor: 'var(--tcg-border)' }}
            onClick={exportConfig}
          >
            Exporter la configuration
          </button>
          <button
            type="button"
            className="rounded-lg border px-4 py-2 text-sm"
            style={{ borderColor: 'var(--tcg-border)' }}
            onClick={importConfig}
          >
            Importer la configuration
          </button>
        </div>
      </div>
    </div>
  )
}
