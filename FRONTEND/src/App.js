import React, { useState } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import Header from './components/Header';
import LoginModal from './components/LoginModal';
import Dashboard from './pages/Dashboard';
import Sales from './pages/Sales';
import Inventory from './pages/Inventory';
import Reports from './pages/Reports';
import Users from './pages/Users';
import Clients from './pages/Clients';
import Providers from './pages/Providers';
import Purchases from './pages/Purchases';
import Audit from './pages/Audit';
import { auth } from './api';
import './App.css';

const ProtectedRoute = ({ children, allowedRoles }) => {
  const user = auth.getCurrentUser();
  if (!user) return <Navigate to="/" />;
  if (allowedRoles && !allowedRoles.includes(user.rol)) return <Navigate to="/dashboard" />;
  return children;
};

function App() {
  const [currentUser, setCurrentUser] = useState(auth.getCurrentUser());
  const [isLoginModalOpen, setIsLoginModalOpen] = useState(false);

  const handleLoginSuccess = () => {
    setCurrentUser(auth.getCurrentUser());
    setIsLoginModalOpen(false);
  };

  const handleLogout = () => {
    auth.logout();
    setCurrentUser(null);
  };

  return (
    <Router>
      <div className="min-h-screen bg-[#f8f9fa] font-sans">
        {currentUser && <Header onLogout={handleLogout} />}

        <main className="p-10 max-w-[1700px] mx-auto">
          <Routes>
            <Route path="/" element={
              !currentUser ? (
                <div className="flex flex-col items-center justify-center h-[80vh]">
                  <div className="text-center max-w-2xl">
                    <h1 className="text-7xl font-black text-gray-900 mb-6 tracking-tighter">
                      Fresco<span className="text-[#4263eb]">Express</span>
                    </h1>
                    <p className="text-xl text-gray-500 mb-12 font-medium">
                      Plataforma profesional para la gestión de fruvers y mercados.
                    </p>
                    <button 
                      onClick={() => setIsLoginModalOpen(true)}
                      className="bg-[#4263eb] text-white px-14 py-6 rounded-3xl font-black text-xl shadow-[0_20px_50px_rgba(66,99,235,0.3)] hover:bg-[#364fc7] transition-all transform hover:scale-105 active:scale-95"
                    >
                      Entrar al Portal
                    </button>
                  </div>
                </div>
              ) : <Navigate to="/dashboard" />
            } />

            <Route path="/dashboard" element={
              <ProtectedRoute allowedRoles={['Administrador', 'Dueño', 'Vendedor']}>
                <Dashboard />
              </ProtectedRoute>
            } />

            <Route path="/ventas" element={
              <ProtectedRoute allowedRoles={['Administrador', 'Vendedor']}>
                <Sales />
              </ProtectedRoute>
            } />

            <Route path="/productos" element={
              <ProtectedRoute allowedRoles={['Administrador', 'Vendedor']}>
                <Inventory />
              </ProtectedRoute>
            } />

            <Route path="/clientes" element={
              <ProtectedRoute allowedRoles={['Administrador', 'Vendedor']}>
                <Clients />
              </ProtectedRoute>
            } />

            <Route path="/compras" element={
              <ProtectedRoute allowedRoles={['Administrador', 'Dueño']}>
                <Purchases />
              </ProtectedRoute>
            } />

            <Route path="/usuarios" element={
              <ProtectedRoute allowedRoles={['Administrador']}>
                <Users />
              </ProtectedRoute>
            } />

            <Route path="/auditoria" element={
              <ProtectedRoute allowedRoles={['Administrador']}>
                <Audit />
              </ProtectedRoute>
            } />

            <Route path="/proveedores" element={
              <ProtectedRoute allowedRoles={['Administrador', 'Dueño']}>
                <Providers />
              </ProtectedRoute>
            } />

            <Route path="/informes" element={
              <ProtectedRoute allowedRoles={['Administrador', 'Dueño']}>
                <Reports />
              </ProtectedRoute>
            } />

            <Route path="*" element={<Navigate to="/" />} />
          </Routes>
        </main>

        <LoginModal 
          isOpen={isLoginModalOpen} 
          onClose={() => setIsLoginModalOpen(false)} 
          onLoginSuccess={handleLoginSuccess}
        />
      </div>
    </Router>
  );
}

export default App;
