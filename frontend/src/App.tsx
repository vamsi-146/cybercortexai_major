import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import { AuthProvider } from '@contexts/AuthContext'
import { ProtectedRoute } from '@components/auth/ProtectedRoute'
import { Sidebar } from '@components/layout/Sidebar'
import { TopBar } from '@components/layout/TopBar'
import { Dashboard } from '@pages/Dashboard'
import { IncidentDetail } from '@pages/IncidentDetail'
import { LoginPage } from '@pages/LoginPage'

function App() {
  return (
    <AuthProvider>
      <Router>
        <Routes>
          <Route path="/login" element={<LoginPage />} />
          <Route
            path="/*"
            element={
              <ProtectedRoute>
                <div className="min-h-screen bg-background">
                  <Sidebar />
                  <div className="ml-64">
                    <TopBar />
                    <Routes>
                      <Route path="/" element={<Dashboard />} />
                      <Route path="/incidents/:id" element={<IncidentDetail />} />
                      {/* Add more routes as pages are implemented */}
                    </Routes>
                  </div>
                </div>
              </ProtectedRoute>
            }
          />
        </Routes>
      </Router>
    </AuthProvider>
  )
}

export default App
