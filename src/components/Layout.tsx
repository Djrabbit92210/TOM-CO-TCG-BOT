import { Menu } from 'lucide-react'
import { useState } from 'react'
import { Outlet } from 'react-router-dom'
import { Sidebar } from './Sidebar'
import { ToastContainer } from './ToastContainer'

export function Layout() {
  const [mobileOpen, setMobileOpen] = useState(false)

  return (
    <div className="flex min-h-screen">
      <Sidebar mobileOpen={mobileOpen} onCloseMobile={() => setMobileOpen(false)} />
      <div className="flex min-h-screen flex-1 flex-col">
        <header
          className="sticky top-0 z-30 flex items-center gap-3 border-b px-4 py-3 lg:hidden"
          style={{ background: 'var(--tcg-surface)', borderColor: 'var(--tcg-border)' }}
        >
          <button
            type="button"
            className="rounded-lg p-2"
            style={{ color: 'var(--tcg-text)' }}
            aria-label="Ouvrir le menu"
            onClick={() => setMobileOpen(true)}
          >
            <Menu className="h-6 w-6" />
          </button>
          <span className="text-sm font-semibold">TCG Scalper Pro</span>
        </header>
        <main className="flex-1 px-4 py-6 sm:px-6 lg:px-10">
          <Outlet />
        </main>
      </div>
      <ToastContainer />
    </div>
  )
}
