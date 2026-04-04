import { create } from 'zustand'
import { persist } from 'zustand/middleware'

export type AuthUser = {
  email: string
  isAdmin: boolean
}

type AuthState = {
  token: string | null
  user: AuthUser | null
  login: (email: string, password: string) => Promise<{ ok: boolean; error?: string }>
  logout: () => void
}

function fakeJwt(email: string): string {
  return btoa(JSON.stringify({ sub: email, exp: Date.now() + 864e5 }))
}

export const useAuthStore = create<AuthState>()(
  persist(
    (set) => ({
      token: null,
      user: null,
      login: async (email, password) => {
        await new Promise((r) => setTimeout(r, 400))
        const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
        if (!re.test(email)) {
          return { ok: false, error: 'Email invalide.' }
        }
        if (password.length < 8) {
          return { ok: false, error: 'Le mot de passe doit faire au moins 8 caractères.' }
        }
        const isAdmin = email.toLowerCase().includes('admin')
        const token = fakeJwt(email)
        set({ token, user: { email, isAdmin } })
        return { ok: true }
      },
      logout: () => {
        set({ token: null, user: null })
      },
    }),
    {
      name: 'tcg-scalper-auth',
      partialize: (s) => ({ token: s.token, user: s.user }),
    },
  ),
)
