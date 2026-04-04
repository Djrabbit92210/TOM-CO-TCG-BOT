import { BrowserRouter, Navigate, Route, Routes } from 'react-router-dom'
import { Layout } from './components/Layout'
import { ProtectedRoute } from './components/ProtectedRoute'
import { Accounts } from './pages/Accounts'
import { Bots } from './pages/Bots'
import { Budgets } from './pages/Budgets'
import { Dashboard } from './pages/Dashboard'
import { Login } from './pages/Login'
import { Logs } from './pages/Logs'
import { Notifications } from './pages/Notifications'
import { Products } from './pages/Products'
import { Settings } from './pages/Settings'

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/login" element={<Login />} />
        <Route element={<ProtectedRoute />}>
          <Route element={<Layout />}>
            <Route path="/" element={<Dashboard />} />
            <Route path="/products" element={<Products />} />
            <Route path="/accounts" element={<Accounts />} />
            <Route path="/bots" element={<Bots />} />
            <Route path="/budgets" element={<Budgets />} />
            <Route path="/logs" element={<Logs />} />
            <Route path="/notifications" element={<Notifications />} />
            <Route path="/settings" element={<Settings />} />
          </Route>
        </Route>
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </BrowserRouter>
  )
}
