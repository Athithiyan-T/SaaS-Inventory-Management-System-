import { NavLink } from "react-router-dom";

/**
 * Sidebar
 *
 * Left-hand navigation menu shown on every page after login.
 * Uses NavLink so the active page is automatically highlighted.
 */
function Sidebar() {
  // Tailwind classes applied to every link
  const baseClasses =
    "flex items-center gap-3 px-4 py-2.5 rounded-lg text-sm font-medium transition-colors";

  // NavLink gives us an "isActive" flag we can use to style the current page differently
  const linkClasses = ({ isActive }) =>
    isActive
      ? `${baseClasses} bg-indigo-600 text-white shadow-sm`
      : `${baseClasses} text-gray-600 hover:bg-gray-100`;

  return (
    <aside className="w-56 shrink-0 bg-white border-r border-gray-200 h-full p-4 hidden md:block">
      <p className="text-xs font-semibold text-gray-400 uppercase tracking-wide px-4 mb-2">
        Menu
      </p>
      <nav className="flex flex-col gap-1">
        <NavLink to="/dashboard" className={linkClasses}>
          <span className="w-1.5 h-1.5 rounded-full bg-current opacity-60" />
          Dashboard
        </NavLink>
        <NavLink to="/products" className={linkClasses}>
          <span className="w-1.5 h-1.5 rounded-full bg-current opacity-60" />
          Products
        </NavLink>
        <NavLink to="/settings" className={linkClasses}>
          <span className="w-1.5 h-1.5 rounded-full bg-current opacity-60" />
          Settings
        </NavLink>
      </nav>
    </aside>
  );
}

export default Sidebar;
