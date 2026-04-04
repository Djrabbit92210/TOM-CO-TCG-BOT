import { ChevronRight, Home } from 'lucide-react'
import { Link } from 'react-router-dom'

type Crumb = { label: string; to?: string }

export function Breadcrumb({ items }: { items: Crumb[] }) {
  return (
    <nav aria-label="Fil d'Ariane" className="mb-6 text-sm" style={{ color: 'var(--tcg-muted)' }}>
      <ol className="flex flex-wrap items-center gap-1">
        <li className="flex items-center gap-1">
          <Home className="h-4 w-4" aria-hidden />
          <Link to="/" className="hover:underline" style={{ color: 'var(--tcg-accent)' }}>
            Accueil
          </Link>
        </li>
        {items.map((c) => (
          <li key={c.label} className="flex items-center gap-1">
            <ChevronRight className="h-4 w-4 shrink-0 opacity-60" aria-hidden />
            {c.to ? (
              <Link to={c.to} className="hover:underline" style={{ color: 'var(--tcg-accent)' }}>
                {c.label}
              </Link>
            ) : (
              <span style={{ color: 'var(--tcg-text)' }}>{c.label}</span>
            )}
          </li>
        ))}
      </ol>
    </nav>
  )
}
