import { useToastStore } from '../stores/toastStore'

export function ToastContainer() {
  const toasts = useToastStore((s) => s.toasts)
  const dismiss = useToastStore((s) => s.dismiss)

  if (!toasts.length) return null

  return (
    <div className="pointer-events-none fixed bottom-4 right-4 z-[60] flex max-w-sm flex-col gap-2">
      {toasts.map((t) => (
        <div
          key={t.id}
          className="pointer-events-auto flex items-start justify-between gap-3 rounded-lg border px-4 py-3 text-sm shadow-lg transition-all"
          style={{
            background: 'var(--tcg-surface)',
            borderColor: 'var(--tcg-border)',
            color: 'var(--tcg-text)',
          }}
          role="status"
        >
          <span>
            {t.kind === 'error' ? (
              <span className="font-medium" style={{ color: 'var(--tcg-danger)' }}>
                Erreur —{' '}
              </span>
            ) : null}
            {t.kind === 'success' ? (
              <span className="font-medium" style={{ color: 'var(--tcg-success)' }}>
                OK —{' '}
              </span>
            ) : null}
            {t.message}
          </span>
          <button
            type="button"
            className="shrink-0 rounded px-1 text-xs opacity-70 hover:opacity-100"
            onClick={() => dismiss(t.id)}
          >
            ✕
          </button>
        </div>
      ))}
    </div>
  )
}
