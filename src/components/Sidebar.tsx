import {
  Bot,
  LayoutDashboard,
  LogOut,
  Menu,
  Package,
  ScrollText,
  Settings,
  Users,
  Wallet,
  Bell,
} from 'lucide-react'
import { NavLink } from 'react-router-dom'
import { useAuthStore } from '../stores/authStore'
import { useSettingsStore } from '../stores/settingsStore'
import { t } from '../i18n/strings'

const nav = [
  { to: '/', icon: LayoutDashboard, key: 'dashboard' as const },
  { to: '/products', icon: Package, key: 'products' as const },
  { to: '/accounts', icon: Users, key: 'accounts' as const },
  { to: '/bots', icon: Bot, key: 'bots' as const },
  { to: '/budgets', icon: Wallet, key: 'budgets' as const },
  { to: '/logs', icon: ScrollText, key: 'logs' as const },
  { to: '/notifications', icon: Bell, key: 'notifications' as const },
  { to: '/settings', icon: Settings, key: 'settings' as const, adminOnly: true },
]

export function Sidebar({
  mobileOpen,
  onCloseMobile,
}: {
  mobileOpen: boolean
  onCloseMobile: () => void
}) {
  const logout = useAuthStore((s) => s.logout)
  const user = useAuthStore((s) => s.user)
  const lang = useSettingsStore((s) => s.settings.lang)
  const tr = t(lang)

  const linkClass = ({ isActive }: { isActive: boolean }) =>
    [
      'flex items-center gap-3 rounded-lg px-3 py-2.5 text-sm font-medium transition-colors',
      isActive ? 'ring-1' : 'hover:opacity-90',
    ].join(' ')

  const activeStyle = (isActive: boolean) =>
    isActive
      ? {
          background: 'color-mix(in srgb, var(--tcg-accent) 18%, transparent)',
          color: 'var(--tcg-accent)',
          borderColor: 'var(--tcg-border)',
          boxShadow: 'inset 0 0 0 1px var(--tcg-border)',
        }
      : { color: 'var(--tcg-text)' }

  const items = nav.filter((n) => !n.adminOnly || user?.isAdmin)

  return (
    <>
      <div
        className={[
          'fixed inset-0 z-40 bg-black/50 lg:hidden',
          mobileOpen ? 'block' : 'hidden',
        ].join(' ')}
        aria-hidden={!mobileOpen}
        onClick={onCloseMobile}
      />
      <aside
        className={[
          'fixed left-0 top-0 z-50 flex h-full w-64 flex-col border-r transition-transform lg:static lg:translate-x-0',
          mobileOpen ? 'translate-x-0' : '-translate-x-full',
        ].join(' ')}
        style={{
          background: 'var(--tcg-surface)',
          borderColor: 'var(--tcg-border)',
        }}
      >
        <div className="border-b px-4 py-5" style={{ borderColor: 'var(--tcg-border)' }}>
          <div className="flex items-center justify-between gap-2 lg:justify-start">
            <div>
              <p className="text-xs font-medium uppercase tracking-wide" style={{ color: 'var(--tcg-muted)' }}>
                {tr.app}
              </p>
              <p className="text-sm font-semibold" style={{ color: 'var(--tcg-text)' }}>
                Console
              </p>
            </div>
            <button
              type="button"
              className="rounded-lg p-2 lg:hidden"
              onClick={onCloseMobile}
              aria-label="Fermer le menu"
            >
              <Menu className="h-5 w-5" />
            </button>
          </div>
        </div>
        <nav className="flex-1 space-y-1 overflow-y-auto p-3">
          {items.map((item) => (
            <NavLink
              key={item.to}
              to={item.to}
              end={item.to === '/'}
              onClick={onCloseMobile}
              className={linkClass}
              style={({ isActive }) => activeStyle(isActive)}
            >
              <item.icon className="h-5 w-5 shrink-0" aria-hidden />
              {tr[item.key]}
            </NavLink>
          ))}
        </nav>
        <div className="border-t p-3" style={{ borderColor: 'var(--tcg-border)' }}>
          <p className="mb-2 truncate px-1 text-xs" style={{ color: 'var(--tcg-muted)' }}>
            {user?.email}
          </p>
          <button
            type="button"
            onClick={() => {
              logout()
              onCloseMobile()
            }}
            className="flex w-full items-center gap-3 rounded-lg px-3 py-2.5 text-sm font-medium transition-colors hover:bg-black/5 dark:hover:bg-white/5"
          >
            <LogOut className="h-5 w-5" aria-hidden />
            {tr.logout}
          </button>
        </div>
      </aside>
    </>
  )
}
