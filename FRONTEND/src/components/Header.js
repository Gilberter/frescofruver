import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import { auth } from '../api';

const Header = ({ onLogout }) => {
  const currentUser = auth.getCurrentUser();
  const location = useLocation();
  
  const role = currentUser?.rol;
  const isAdmin = role === 'Administrador';
  const isOwner = role === 'Dueño';
  const isCajero = role === 'Vendedor';

  // Define navigation items based on role
  const navItems = [
    { name: 'Inicio', path: '/dashboard', roles: ['Administrador', 'Dueño', 'Vendedor'] },
    { name: 'Ventas', path: '/ventas', roles: ['Administrador', 'Vendedor'] },
    { name: 'Inventario', path: '/productos', roles: ['Administrador', 'Vendedor'] },
    { name: 'Compras', path: '/compras', roles: ['Administrador', 'Dueño'] },
    { name: 'Clientes', path: '/clientes', roles: ['Administrador', 'Vendedor'] },
    { name: 'Proveedores', path: '/proveedores', roles: ['Administrador', 'Dueño'] },
    { name: 'Informes', path: '/informes', roles: ['Administrador', 'Dueño'] },
    { name: 'Usuarios', path: '/usuarios', roles: ['Administrador'] },
    { name: 'Auditoría', path: '/auditoria', roles: ['Administrador'] },
  ];

  // Filter items current user can see
  const visibleItems = navItems.filter(item => item.roles.includes(role));

  const roleBadge = isAdmin ? '(ADMIN)' : isCajero ? '(CAJERO)' : isOwner ? '(DUEÑO)' : '';

  return (
    <header className="flex items-center justify-between px-10 py-5 bg-white shadow-md border-b border-gray-100 sticky top-0 z-40">
      <div className="flex items-center">
        <Link to="/dashboard" className="text-[22px] font-bold text-[#4263eb] tracking-tight">
          FrescoExpress <span className="text-[12px] opacity-50 ml-1">{roleBadge}</span>
        </Link>
      </div>

      <div className="flex items-center space-x-8">
        <nav>
          <ul className="flex space-x-5">
            {visibleItems.map((item) => (
              <li key={item.name}>
                <Link
                  to={item.path}
                  className={`text-[14px] font-bold transition-all duration-200 ${
                    location.pathname === item.path 
                    ? 'text-[#4263eb] bg-blue-50 px-4 py-2 rounded-xl' 
                    : 'text-[#343a40] hover:text-[#4263eb] px-4 py-2'
                  }`}
                >
                  {item.name}
                </Link>
              </li>
            ))}
          </ul>
        </nav>

        <button 
          className="bg-[#1a1c23] hover:bg-black text-white px-6 py-2.5 rounded-xl text-[14px] font-bold transition-all shadow-lg active:scale-95"
          onClick={onLogout}
        >
          Salir
        </button>
      </div>
    </header>
  );
};

export default Header;
