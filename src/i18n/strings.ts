import type { Lang } from '../stores/settingsStore'

const fr = {
  app: 'TCG Scalper Pro',
  dashboard: 'Tableau de bord',
  products: 'Produits',
  accounts: 'Comptes',
  bots: 'Bots',
  budgets: 'Budgets',
  logs: 'Logs',
  notifications: 'Notifications',
  settings: 'Paramètres',
  logout: 'Déconnexion',
  login: 'Connexion',
  save: 'Enregistrer',
  cancel: 'Annuler',
  add: 'Ajouter',
  edit: 'Éditer',
  delete: 'Supprimer',
  search: 'Rechercher',
  exportCsv: 'Exporter CSV',
  exportPdf: 'Exporter PDF',
}

const en: typeof fr = {
  app: 'TCG Scalper Pro',
  dashboard: 'Dashboard',
  products: 'Products',
  accounts: 'Accounts',
  bots: 'Bots',
  budgets: 'Budgets',
  logs: 'Logs',
  notifications: 'Notifications',
  settings: 'Settings',
  logout: 'Log out',
  login: 'Sign in',
  save: 'Save',
  cancel: 'Cancel',
  add: 'Add',
  edit: 'Edit',
  delete: 'Delete',
  search: 'Search',
  exportCsv: 'Export CSV',
  exportPdf: 'Export PDF',
}

export function t(lang: Lang): typeof fr {
  return lang === 'en' ? en : fr
}
