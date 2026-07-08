/**
 * Navbar
 *
 * Top bar shown on every page after login.
 * Shows the app name, the logged-in user's email, and a logout button.
 *
 * Props:
 * - userEmail: string - the current user's email address
 * - onLogout: function - called when the logout button is clicked
 */
function Navbar({ userEmail, onLogout }) {
  return (
    <header className="h-16 shrink-0 bg-white border-b border-gray-200 flex items-center justify-between px-6 shadow-sm sticky top-0 z-10">
      <div className="flex items-center gap-2">
        <div className="w-8 h-8 rounded-lg bg-indigo-600 flex items-center justify-center text-white font-bold text-sm">
          SF
        </div>
        <span className="text-xl font-bold text-gray-800">StockFlow</span>
      </div>

      <div className="flex items-center gap-4">
        {userEmail && (
          <span className="text-sm text-gray-500 hidden sm:inline">{userEmail}</span>
        )}
        <button
          onClick={onLogout}
          className="text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700 active:bg-indigo-800 px-4 py-2 rounded-lg transition-colors focus:outline-none focus:ring-2 focus:ring-indigo-300"
        >
          Logout
        </button>
      </div>
    </header>
  );
}

export default Navbar;
