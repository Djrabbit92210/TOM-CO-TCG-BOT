export const SITES = [
  'FNAC',
  'JouéClub',
  'Toys R Us',
  'Amazon FR',
  'Cardmarket',
  'TCGPlayer',
] as const

export type Site = (typeof SITES)[number]

export type Product = {
  id: string
  name: string
  url: string
  sites: Site[]
  maxPrice: number
  qty: number
  status: 'ok' | 'ko'
  autoBuy: boolean
  threshold?: number
}

export type AccountRow = {
  id: string
  email: string
  site: Site
  proxy: string
  status: 'ok' | 'ko' | 'warn'
  lastUsed: string
}

export type BotRow = {
  id: string
  name: string
  site: Site
  accountEmail: string
  proxy: string
  status: 'running' | 'paused' | 'stopped'
  lastCheck: string
}

export type BudgetExpense = {
  id: string
  date: string
  product: string
  amount: number
  bot: string
}

export type LogEntry = {
  id: string
  ts: string
  site: Site
  level: 'Info' | 'Warning' | 'Error'
  message: string
  stack?: string
}

export type NotificationHistory = {
  id: string
  date: string
  channel: 'Discord' | 'SMS' | 'Email'
  message: string
}

export const mockProducts: Product[] = [
  {
    id: '1',
    name: 'Charizard ex SAR',
    url: 'https://fnac.com/example',
    sites: ['FNAC', 'Cardmarket'],
    maxPrice: 120,
    qty: 1,
    status: 'ok',
    autoBuy: true,
    threshold: 110,
  },
  {
    id: '2',
    name: 'Pikachu Promo',
    url: 'https://amazon.fr/example',
    sites: ['Amazon FR'],
    maxPrice: 45,
    qty: 2,
    status: 'ko',
    autoBuy: false,
  },
]

export const mockAccounts: AccountRow[] = [
  {
    id: 'a1',
    email: 'shop@example.com',
    site: 'FNAC',
    proxy: 'proxy-eu-1',
    status: 'ok',
    lastUsed: '2026-04-04 14:22',
  },
  {
    id: 'a2',
    email: 'backup@example.com',
    site: 'JouéClub',
    proxy: 'proxy-eu-2',
    status: 'warn',
    lastUsed: '2026-04-03 09:10',
  },
]

export const mockBots: BotRow[] = [
  {
    id: 'b1',
    name: 'Bot FNAC #1',
    site: 'FNAC',
    accountEmail: 'shop@example.com',
    proxy: 'proxy-eu-1',
    status: 'running',
    lastCheck: '2026-04-04 16:01',
  },
  {
    id: 'b2',
    name: 'Bot Amazon',
    site: 'Amazon FR',
    accountEmail: 'backup@example.com',
    proxy: 'proxy-eu-2',
    status: 'paused',
    lastCheck: '2026-04-04 15:40',
  },
]

export const stockBySite = [
  { name: 'FNAC', value: 38 },
  { name: 'Amazon FR', value: 22 },
  { name: 'Cardmarket', value: 18 },
  { name: 'Autres', value: 12 },
]

export const stockTrend = [
  { day: 'Lun', stock: 40 },
  { day: 'Mar', stock: 52 },
  { day: 'Mer', stock: 48 },
  { day: 'Jeu', stock: 61 },
  { day: 'Ven', stock: 55 },
  { day: 'Sam', stock: 70 },
  { day: 'Dim', stock: 66 },
]

export const recentPurchases = [
  { id: 'p1', label: 'Booster 151 — FNAC', time: 'Il y a 12 min' },
  { id: 'p2', label: 'ETB Temporal — Amazon FR', time: 'Il y a 1 h' },
  { id: 'p3', label: 'Display SV9 — Cardmarket', time: 'Hier' },
]

export const recentAlerts = [
  { id: 'n1', text: 'Seuil budget produit proche (Charizard)', channel: 'Discord' as const },
  { id: 'n2', text: 'Stock détecté — Pikachu Promo', channel: 'Email' as const },
  { id: 'n3', text: 'Bot Amazon en pause', channel: 'SMS' as const },
]

export const mockBotLogs: LogEntry[] = [
  {
    id: 'l1',
    ts: '2026-04-04 16:00:02',
    site: 'FNAC',
    level: 'Info',
    message: 'Check stock OK',
  },
  {
    id: 'l2',
    ts: '2026-04-04 15:58:11',
    site: 'Amazon FR',
    level: 'Warning',
    message: 'Délai réseau élevé',
  },
  {
    id: 'l3',
    ts: '2026-04-04 15:55:00',
    site: 'FNAC',
    level: 'Error',
    message: 'Timeout page panier',
    stack: 'Error: timeout\n  at fetchWithRetry (mock)',
  },
]

export const mockGlobalLogs: LogEntry[] = [
  ...mockBotLogs,
  {
    id: 'l4',
    ts: '2026-04-04 14:20:00',
    site: 'Cardmarket',
    level: 'Info',
    message: 'Export CSV terminé',
  },
]

export const mockExpenses: BudgetExpense[] = [
  { id: 'e1', date: '2026-04-04', product: 'Charizard ex SAR', amount: 98.5, bot: 'Bot FNAC #1' },
  { id: 'e2', date: '2026-04-03', product: 'ETB', amount: 54, bot: 'Bot Amazon' },
]

export const mockNotifHistory: NotificationHistory[] = [
  { id: 'h1', date: '2026-04-04 15:30', channel: 'Discord', message: 'Alerte stock' },
  { id: 'h2', date: '2026-04-04 12:00', channel: 'Email', message: 'Résumé quotidien' },
]

export const PROXY_OPTIONS = ['proxy-eu-1', 'proxy-eu-2', 'proxy-us-1', 'Aucun']
export const CAPTCHA_SOLVERS = ['2Captcha', 'Anti-Captcha'] as const
