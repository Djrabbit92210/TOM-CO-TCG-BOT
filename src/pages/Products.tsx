import { useForm } from 'react-hook-form'
import { useMemo, useState } from 'react'
import { Breadcrumb } from '../components/Breadcrumb'
import { Modal } from '../components/Modal'
import { mockProducts, SITES, type Product, type Site } from '../data/mockData'
import { mockSave } from '../services/mockApi'
import { useToastStore } from '../stores/toastStore'

type AddForm = {
  name: string
  url: string
  maxPrice: number
  qty: number
  autoBuy: boolean
  threshold: number
}

const PAGE_SIZE = 10

export function Products() {
  const [rows, setRows] = useState<Product[]>(mockProducts)
  const [filterSite, setFilterSite] = useState<string>('all')
  const [filterPrice, setFilterPrice] = useState<string>('all')
  const [filterStatus, setFilterStatus] = useState<string>('all')
  const [page, setPage] = useState(0)
  const [open, setOpen] = useState(false)
  const [selectedSites, setSelectedSites] = useState<Site[]>([])
  const pushToast = useToastStore((s) => s.push)

  const form = useForm<AddForm>({
    defaultValues: { name: '', url: '', maxPrice: 50, qty: 1, autoBuy: false, threshold: 0 },
  })
  const autoBuy = form.watch('autoBuy')

  const filtered = useMemo(() => {
    return rows.filter((r) => {
      if (filterSite !== 'all' && !r.sites.includes(filterSite as Site)) return false
      if (filterStatus !== 'all' && r.status !== filterStatus) return false
      if (filterPrice === '100' && r.maxPrice > 100) return false
      if (filterPrice === '200' && r.maxPrice > 200) return false
      return true
    })
  }, [rows, filterSite, filterPrice, filterStatus])

  const pageRows = filtered.slice(page * PAGE_SIZE, page * PAGE_SIZE + PAGE_SIZE)
  const totalPages = Math.max(1, Math.ceil(filtered.length / PAGE_SIZE))

  const toggleSite = (s: Site) => {
    setSelectedSites((prev) => (prev.includes(s) ? prev.filter((x) => x !== s) : [...prev, s]))
  }

  const onAdd = form.handleSubmit(async (data) => {
    if (selectedSites.length === 0) {
      pushToast('Sélectionnez au moins un site.', 'error')
      return
    }
    const p: Product = {
      id: crypto.randomUUID(),
      name: data.name,
      url: data.url,
      sites: selectedSites,
      maxPrice: data.maxPrice,
      qty: data.qty,
      status: 'ok',
      autoBuy: data.autoBuy,
      threshold: data.autoBuy ? data.threshold : undefined,
    }
    await mockSave(p)
    setRows((r) => [p, ...r])
    pushToast('Produit ajouté (mock).', 'success')
    setOpen(false)
    form.reset()
    setSelectedSites([])
  })

  return (
    <div>
      <Breadcrumb items={[{ label: 'Produits' }]} />
      <div className="mb-6 flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
        <h1>Produits</h1>
        <button
          type="button"
          onClick={() => setOpen(true)}
          className="rounded-lg px-4 py-2.5 text-sm font-semibold text-black"
          style={{ background: 'var(--tcg-accent)' }}
        >
          Ajouter un produit
        </button>
      </div>

      <div className="mb-4 flex flex-wrap gap-3">
        <select
          className="rounded-lg border px-3 py-2 text-sm"
          style={{ borderColor: 'var(--tcg-border)', background: 'var(--tcg-surface)', color: 'var(--tcg-text)' }}
          value={filterSite}
          onChange={(e) => {
            setFilterSite(e.target.value)
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
          value={filterPrice}
          onChange={(e) => {
            setFilterPrice(e.target.value)
            setPage(0)
          }}
        >
          <option value="all">Tous les prix</option>
          <option value="100">≤ 100 €</option>
          <option value="200">≤ 200 €</option>
        </select>
        <select
          className="rounded-lg border px-3 py-2 text-sm"
          style={{ borderColor: 'var(--tcg-border)', background: 'var(--tcg-surface)', color: 'var(--tcg-text)' }}
          value={filterStatus}
          onChange={(e) => {
            setFilterStatus(e.target.value)
            setPage(0)
          }}
        >
          <option value="all">Tous les statuts</option>
          <option value="ok">OK</option>
          <option value="ko">KO</option>
        </select>
      </div>

      <div
        className="overflow-x-auto rounded-xl border"
        style={{ borderColor: 'var(--tcg-border)', background: 'var(--tcg-surface)' }}
      >
        <table className="min-w-full text-left text-sm">
          <thead>
            <tr className="border-b" style={{ borderColor: 'var(--tcg-border)' }}>
              <th className="px-4 py-3">Nom</th>
              <th className="px-4 py-3">Sites</th>
              <th className="px-4 py-3">Prix max</th>
              <th className="px-4 py-3">Qté</th>
              <th className="px-4 py-3">Statut</th>
              <th className="px-4 py-3">Actions</th>
            </tr>
          </thead>
          <tbody>
            {pageRows.map((p) => (
              <tr key={p.id} className="border-b last:border-0" style={{ borderColor: 'var(--tcg-border)' }}>
                <td className="px-4 py-3 font-medium">{p.name}</td>
                <td className="px-4 py-3">{p.sites.join(', ')}</td>
                <td className="px-4 py-3">{p.maxPrice} €</td>
                <td className="px-4 py-3">{p.qty}</td>
                <td className="px-4 py-3">{p.status === 'ok' ? '✓' : '✗'}</td>
                <td className="px-4 py-3">
                  <div className="flex flex-wrap gap-2">
                    <button
                      type="button"
                      className="text-xs underline"
                      style={{ color: 'var(--tcg-accent)' }}
                      onClick={() => pushToast('Édition (mock)', 'info')}
                    >
                      Éditer
                    </button>
                    <button
                      type="button"
                      className="text-xs underline"
                      style={{ color: 'var(--tcg-danger)' }}
                      onClick={() => {
                        setRows((r) => r.filter((x) => x.id !== p.id))
                        pushToast('Supprimé (mock)', 'success')
                      }}
                    >
                      Supprimer
                    </button>
                    <button
                      type="button"
                      className="text-xs underline"
                      onClick={() => pushToast(`Check forcé pour ${p.name} (mock)`, 'info')}
                    >
                      Forcer check
                    </button>
                  </div>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

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

      <Modal
        open={open}
        onClose={() => setOpen(false)}
        title="Ajouter un produit"
        footer={
          <>
            <button
              type="button"
              className="rounded-lg border px-4 py-2 text-sm"
              style={{ borderColor: 'var(--tcg-border)' }}
              onClick={() => setOpen(false)}
            >
              Annuler
            </button>
            <button
              type="button"
              className="rounded-lg px-4 py-2 text-sm font-semibold text-black"
              style={{ background: 'var(--tcg-accent)' }}
              onClick={() => void onAdd()}
            >
              Sauvegarder
            </button>
          </>
        }
      >
        <div className="space-y-3">
          <div>
            <label className="text-sm font-medium">Nom</label>
            <input
              className="mt-1 w-full rounded-lg border px-3 py-2"
              style={{ borderColor: 'var(--tcg-border)', background: 'var(--tcg-bg)', color: 'var(--tcg-text)' }}
              list="product-suggestions"
              {...form.register('name', { required: true })}
            />
            <datalist id="product-suggestions">
              <option value="Charizard ex SAR" />
              <option value="Pikachu Promo" />
              <option value="Display SV9" />
            </datalist>
          </div>
          <div>
            <label className="text-sm font-medium">URL</label>
            <input
              className="mt-1 w-full rounded-lg border px-3 py-2"
              style={{ borderColor: 'var(--tcg-border)', background: 'var(--tcg-bg)', color: 'var(--tcg-text)' }}
              {...form.register('url', {
                required: true,
                pattern: {
                  value: /^https?:\/\/.+/i,
                  message: 'URL invalide (http/https)',
                },
              })}
            />
            {form.formState.errors.url ? (
              <p className="mt-1 text-xs" style={{ color: 'var(--tcg-danger)' }}>
                {form.formState.errors.url.message}
              </p>
            ) : null}
          </div>
          <div>
            <p className="mb-1 text-sm font-medium">Sites</p>
            <div className="flex flex-wrap gap-2">
              {SITES.map((s) => (
                <button
                  key={s}
                  type="button"
                  onClick={() => toggleSite(s)}
                  className="rounded-full border px-3 py-1 text-xs"
                  style={{
                    borderColor: 'var(--tcg-border)',
                    background: selectedSites.includes(s)
                      ? 'color-mix(in srgb, var(--tcg-accent) 25%, transparent)'
                      : 'transparent',
                  }}
                >
                  {s}
                </button>
              ))}
            </div>
          </div>
          <div className="grid grid-cols-2 gap-3">
            <div>
              <label className="text-sm font-medium">Prix max (€)</label>
              <input
                type="number"
                className="mt-1 w-full rounded-lg border px-3 py-2"
                style={{ borderColor: 'var(--tcg-border)', background: 'var(--tcg-bg)', color: 'var(--tcg-text)' }}
                {...form.register('maxPrice', { valueAsNumber: true, min: 0 })}
              />
            </div>
            <div>
              <label className="text-sm font-medium">Quantité</label>
              <input
                type="number"
                className="mt-1 w-full rounded-lg border px-3 py-2"
                style={{ borderColor: 'var(--tcg-border)', background: 'var(--tcg-bg)', color: 'var(--tcg-text)' }}
                {...form.register('qty', { valueAsNumber: true, min: 1 })}
              />
            </div>
          </div>
          <label className="flex items-center gap-2 text-sm">
            <input type="checkbox" {...form.register('autoBuy')} />
            Auto-achat
          </label>
          {autoBuy ? (
            <div>
              <label className="text-sm font-medium">Seuil (€)</label>
              <input
                type="number"
                className="mt-1 w-full rounded-lg border px-3 py-2"
                style={{ borderColor: 'var(--tcg-border)', background: 'var(--tcg-bg)', color: 'var(--tcg-text)' }}
                {...form.register('threshold', { valueAsNumber: true, min: 0 })}
              />
            </div>
          ) : null}
        </div>
      </Modal>
    </div>
  )
}
