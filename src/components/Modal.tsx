import { X } from 'lucide-react'
import type { ReactNode } from 'react'
import { useEffect } from 'react'

type Props = {
  open: boolean
  title: string
  onClose: () => void
  children: ReactNode
  footer?: ReactNode
}

export function Modal({ open, title, onClose, children, footer }: Props) {
  useEffect(() => {
    if (!open) return
    const onKey = (e: KeyboardEvent) => {
      if (e.key === 'Escape') onClose()
    }
    window.addEventListener('keydown', onKey)
    return () => window.removeEventListener('keydown', onKey)
  }, [open, onClose])

  if (!open) return null

  return (
    <div
      className="fixed inset-0 z-50 flex items-center justify-center p-4"
      role="dialog"
      aria-modal="true"
      aria-labelledby="modal-title"
    >
      <button
        type="button"
        className="absolute inset-0 bg-black/55 transition-opacity"
        aria-label="Fermer"
        onClick={onClose}
      />
      <div
        className="relative z-10 w-full max-w-lg rounded-xl border shadow-xl transition-transform"
        style={{
          background: 'var(--tcg-surface)',
          borderColor: 'var(--tcg-border)',
          boxShadow: '0 25px 50px -12px rgba(0,0,0,0.35)',
        }}
      >
        <div
          className="flex items-center justify-between border-b px-5 py-4"
          style={{ borderColor: 'var(--tcg-border)' }}
        >
          <h2 id="modal-title" className="text-lg font-semibold">
            {title}
          </h2>
          <button
            type="button"
            onClick={onClose}
            className="rounded-lg p-2 transition-colors hover:bg-black/10 dark:hover:bg-white/10"
          >
            <X className="h-5 w-5" aria-hidden />
          </button>
        </div>
        <div className="max-h-[min(70vh,520px)] overflow-y-auto px-5 py-4">{children}</div>
        {footer ? (
          <div
            className="flex justify-end gap-2 border-t px-5 py-4"
            style={{ borderColor: 'var(--tcg-border)' }}
          >
            {footer}
          </div>
        ) : null}
      </div>
    </div>
  )
}
