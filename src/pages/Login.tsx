import { useForm } from 'react-hook-form'
import { Link, Navigate, useLocation } from 'react-router-dom'
import { useAuthStore } from '../stores/authStore'

type Form = { email: string; password: string }

export function Login() {
  const token = useAuthStore((s) => s.token)
  const login = useAuthStore((s) => s.login)
  const loc = useLocation()
  const from = (loc.state as { from?: string } | null)?.from || '/'

  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting },
    setError: setFormError,
  } = useForm<Form>({ defaultValues: { email: '', password: '' } })

  if (token) {
    return <Navigate to={from} replace />
  }

  const onSubmit = async (data: Form) => {
    const res = await login(data.email, data.password)
    if (!res.ok) {
      setFormError('root', { message: res.error || 'Échec de la connexion.' })
    }
  }

  return (
    <div className="relative flex min-h-screen flex-col items-center justify-center overflow-hidden px-4">
      <div
        className="pointer-events-none absolute inset-0"
        style={{
          background: 'linear-gradient(135deg, #7fff00 0%, #0a0a0a 45%, #121212 100%)',
          opacity: 0.95,
        }}
      />
      <div
        className="relative z-10 w-full max-w-md rounded-2xl border p-8 shadow-2xl backdrop-blur-sm"
        style={{
          background: 'color-mix(in srgb, var(--tcg-surface) 92%, transparent)',
          borderColor: 'var(--tcg-border)',
        }}
      >
        <div className="mb-8 text-center">
          <h1 className="text-2xl font-bold tracking-tight text-white drop-shadow-sm">TCG Scalper Pro</h1>
          <p className="mt-2 text-sm text-white/80">Interface frontend — connexion simulée</p>
        </div>
        <form onSubmit={handleSubmit(onSubmit)} className="space-y-4" noValidate>
          <div>
            <label htmlFor="email" className="mb-1 block text-sm font-medium text-white/90">
              Email
            </label>
            <input
              id="email"
              type="email"
              autoComplete="email"
              className="w-full rounded-lg border px-3 py-2.5 text-[var(--tcg-text)] shadow-inner"
              style={{ borderColor: 'var(--tcg-border)', background: 'var(--tcg-surface)' }}
              {...register('email', { required: 'Email requis' })}
            />
            {errors.email ? (
              <p className="mt-1 text-sm" style={{ color: 'var(--tcg-danger)' }}>
                {errors.email.message}
              </p>
            ) : null}
          </div>
          <div>
            <label htmlFor="password" className="mb-1 block text-sm font-medium text-white/90">
              Mot de passe
            </label>
            <input
              id="password"
              type="password"
              autoComplete="current-password"
              className="w-full rounded-lg border px-3 py-2.5 text-[var(--tcg-text)] shadow-inner"
              style={{ borderColor: 'var(--tcg-border)', background: 'var(--tcg-surface)' }}
              {...register('password', {
                required: 'Mot de passe requis',
                minLength: { value: 8, message: 'Minimum 8 caractères' },
              })}
            />
            {errors.password ? (
              <p className="mt-1 text-sm" style={{ color: 'var(--tcg-danger)' }}>
                {errors.password.message}
              </p>
            ) : null}
          </div>
          {errors.root?.message ? (
            <p className="rounded-lg bg-red-500/15 px-3 py-2 text-sm text-red-200">{errors.root.message}</p>
          ) : null}
          <button
            type="submit"
            disabled={isSubmitting}
            className="w-full rounded-lg py-3 text-sm font-semibold text-black transition-colors disabled:opacity-60"
            style={{ background: 'var(--tcg-accent)' }}
            onMouseEnter={(e) => {
              e.currentTarget.style.background = 'var(--tcg-accent-hover)'
            }}
            onMouseLeave={(e) => {
              e.currentTarget.style.background = 'var(--tcg-accent)'
            }}
          >
            {isSubmitting ? 'Connexion…' : 'Se connecter'}
          </button>
        </form>
        <div className="mt-6 flex flex-col gap-2 text-center text-sm">
          <Link to="/login" className="text-white/80 underline-offset-2 hover:underline" state={loc.state}>
            Mot de passe oublié ? (bientôt)
          </Link>
          <Link to="/login" className="text-white/80 underline-offset-2 hover:underline" state={loc.state}>
            S&apos;inscrire (bientôt)
          </Link>
        </div>
        <p className="mt-6 text-center text-xs text-white/60">
          Astuce : utilisez un email contenant <code className="rounded bg-black/30 px-1">admin</code> pour
          voir Paramètres (admin).
        </p>
      </div>
    </div>
  )
}
