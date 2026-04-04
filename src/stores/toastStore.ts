import { create } from 'zustand'

export type ToastKind = 'success' | 'error' | 'info'

export type Toast = {
  id: string
  message: string
  kind: ToastKind
}

type ToastState = {
  toasts: Toast[]
  push: (message: string, kind?: ToastKind) => void
  dismiss: (id: string) => void
}

export const useToastStore = create<ToastState>((set) => ({
  toasts: [],
  push: (message, kind = 'info') => {
    const id = crypto.randomUUID()
    set((s) => ({ toasts: [...s.toasts, { id, message, kind }] }))
    window.setTimeout(() => {
      set((s) => ({ toasts: s.toasts.filter((t) => t.id !== id) }))
    }, 4200)
  },
  dismiss: (id) => set((s) => ({ toasts: s.toasts.filter((t) => t.id !== id) })),
}))
