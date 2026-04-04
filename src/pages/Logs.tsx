import autoTable from 'jspdf-autotable'
import { jsPDF } from 'jspdf'
import { useMemo, useState } from 'react'
import { Breadcrumb } from '../components/Breadcrumb'
import { mockGlobalLogs, SITES } from '../data/mockData'
import { useToastStore } from '../stores/toastStore'

const PAGE_SIZE = 8

export function Logs() {
  const [filters, setFilters] = useState({
    date: '',
    site: 'all' as string,
    level: 'all' as string,
    q: '',
  })
  const [page, setPage] = useState(0)
  const [largeText, setLargeText] = useState(false)
  const pushToast = useToastStore((s) => s.push)

  const filtered = useMemo(() => {
    return mockGlobalLogs.filter((l) => {
      if (filters.level !== 'all' && l.level !== filters.level) return false
      if (filters.site !== 'all' && l.site !== filters.site) return false
      if (filters.date && !l.ts.startsWith(filters.date)) return false
      if (filters.q) {
        const qq = filters.q.toLowerCase()
        if (
          !l.message.toLowerCase().includes(qq) &&
          !l.ts.toLowerCase().includes(qq) &&
          !(l.stack?.toLowerCase().includes(qq))
        ) {
          return false
        }
      }
      return true
    })
  }, [filters])

  const rows = filtered.slice(page * PAGE_SIZE, page * PAGE_SIZE + PAGE_SIZE)
  const totalPages = Math.max(1, Math.ceil(filtered.length / PAGE_SIZE))

  const exportCsv = () => {
    const header = 'Timestamp,Site,Niveau,Message,Stack\n'
    const body = filtered
      .map((l) =>
        [l.ts, l.site, l.level, l.message, l.stack ?? '']
          .map((c) => `"${String(c).replace(/"/g, '""')}"`)
          .join(','),
      )
      .join('\n')
    const blob = new Blob([header + body], { type: 'text/csv;charset=utf-8' })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = 'logs-export.csv'
    a.click()
    URL.revokeObjectURL(url)
    pushToast('CSV exporté.', 'success')
  }

  const exportPdf = () => {
    const doc = new jsPDF()
    doc.setFontSize(14)
    doc.text('TCG Scalper Pro — Logs', 14, 16)
    autoTable(doc, {
      startY: 22,
      head: [['Date', 'Site', 'Niveau', 'Message']],
      body: filtered.map((l) => [l.ts, l.site, l.level, l.message]),
      styles: { fontSize: 8 },
    })
    doc.save('logs-export.pdf')
    pushToast('PDF exporté.', 'success')
  }

  return (
    <div>
      <Breadcrumb items={[{ label: 'Logs' }]} />
      <div className="mb-6 flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
        <h1>Logs</h1>
        <div className="flex flex-wrap gap-2">
          <button
            type="button"
            className="rounded-lg border px-4 py-2 text-sm"
            style={{ borderColor: 'var(--tcg-border)' }}
            onClick={exportCsv}
          >
            Exporter CSV
          </button>
          <button
            type="button"
            className="rounded-lg border px-4 py-2 text-sm"
            style={{ borderColor: 'var(--tcg-border)' }}
            onClick={exportPdf}
          >
            Exporter PDF
          </button>
          <label className="flex items-center gap-2 rounded-lg border px-4 py-2 text-sm" style={{ borderColor: 'var(--tcg-border)' }}>
            <input type="checkbox" checked={largeText} onChange={(e) => setLargeText(e.target.checked)} />
            Lecture seule (grand texte)
          </label>
        </div>
      </div>

      <div className="mb-4 flex flex-wrap gap-3">
        <input
          type="date"
          className="rounded-lg border px-3 py-2 text-sm"
          style={{ borderColor: 'var(--tcg-border)', background: 'var(--tcg-surface)', color: 'var(--tcg-text)' }}
          value={filters.date}
          onChange={(e) => {
            setFilters((f) => ({ ...f, date: e.target.value }))
            setPage(0)
          }}
        />
        <select
          className="rounded-lg border px-3 py-2 text-sm"
          style={{ borderColor: 'var(--tcg-border)', background: 'var(--tcg-surface)', color: 'var(--tcg-text)' }}
          value={filters.site}
          onChange={(e) => {
            setFilters((f) => ({ ...f, site: e.target.value }))
            setPage(0)
          }}
        >
          <option value="all">Tous les sites</option>
          {SITES.map((s) => (
            <option key={s} value={s}>
              {s}
            </option>
          ))}
        </select>
        <select
          className="rounded-lg border px-3 py-2 text-sm"
          style={{ borderColor: 'var(--tcg-border)', background: 'var(--tcg-surface)', color: 'var(--tcg-text)' }}
          value={filters.level}
          onChange={(e) => {
            setFilters((f) => ({ ...f, level: e.target.value }))
            setPage(0)
          }}
        >
          <option value="all">Tous niveaux</option>
          <option value="Info">Info</option>
          <option value="Warning">Warning</option>
          <option value="Error">Error</option>
        </select>
        <input
          className="min-w-[200px] flex-1 rounded-lg border px-3 py-2 text-sm"
          style={{ borderColor: 'var(--tcg-border)', background: 'var(--tcg-surface)', color: 'var(--tcg-text)' }}
          placeholder="Recherche…"
          value={filters.q}
          onChange={(e) => {
            setFilters((f) => ({ ...f, q: e.target.value }))
            setPage(0)
          }}
        />
      </div>

      <ul className="space-y-3">
        {rows.map((l) => (
          <li
            key={l.id}
            className="rounded-xl border p-4"
            style={{
              borderColor: 'var(--tcg-border)',
              background: 'var(--tcg-surface)',
              fontSize: largeText ? '1.125rem' : undefined,
              lineHeight: largeText ? 1.5 : undefined,
            }}
          >
            <div className="flex flex-wrap items-center gap-2 text-xs" style={{ color: 'var(--tcg-muted)' }}>
              <span>{l.ts}</span>
              <span>·</span>
              <span>{l.site}</span>
              <span>·</span>
              <span className="font-medium" style={{ color: 'var(--tcg-text)' }}>
                {l.level}
              </span>
            </div>
            <p className="mt-2">{l.message}</p>
            {l.stack && l.level === 'Error' ? (
              <pre
                className="mt-2 overflow-x-auto rounded-lg p-3 text-xs"
                style={{ background: 'var(--tcg-bg)', color: 'var(--tcg-muted)' }}
              >
                {l.stack}
              </pre>
            ) : null}
          </li>
        ))}
      </ul>

      <div className="mt-4 flex items-center justify-between text-sm" style={{ color: 'var(--tcg-muted)' }}>
        <span>
          Page {page + 1} / {totalPages}
        </span>
        <div className="flex gap-2">
          <button
            type="button"
            className="rounded border px-3 py-1"
            style={{ borderColor: 'var(--tcg-border)' }}
            disabled={page <= 0}
            onClick={() => setPage((p) => Math.max(0, p - 1))}
          >
            Précédent
          </button>
          <button
            type="button"
            className="rounded border px-3 py-1"
            style={{ borderColor: 'var(--tcg-border)' }}
            disabled={page >= totalPages - 1}
            onClick={() => setPage((p) => Math.min(totalPages - 1, p + 1))}
          >
            Suivant
          </button>
        </div>
      </div>
    </div>
  )
}
