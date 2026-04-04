import { create } from 'zustand'
import { persist } from 'zustand/middleware'

export type ThemeMode = 'light' | 'dark'
export type Lang = 'fr' | 'en'

export type AppSettings = {
  checkIntervalSec: number
  maxConcurrentBots: number
  lang: Lang
  theme: ThemeMode
}

const defaultSettings: AppSettings = {
  checkIntervalSec: 10,
  maxConcurrentBots: 5,
  lang: 'fr',
  theme: 'dark',
}

type SettingsState = {
  settings: AppSettings
  setSettings: (p: Partial<AppSettings>) => void
  applyThemeToDom: () => void
}

export const useSettingsStore = create<SettingsState>()(
  persist(
    (set, get) => ({
      settings: defaultSettings,
      setSettings: (p) => {
        set((s) => ({ settings: { ...s.settings, ...p } }))
        get().applyThemeToDom()
      },
      applyThemeToDom: () => {
        const t = get().settings.theme
        document.documentElement.dataset.theme = t
      },
    }),
    {
      name: 'tcg-scalper-settings',
    },
  ),
)
