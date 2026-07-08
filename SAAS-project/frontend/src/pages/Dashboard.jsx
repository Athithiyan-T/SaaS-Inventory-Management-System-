import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import Navbar from "../components/Navbar";
import Sidebar from "../components/Sidebar";
import DashboardCard from "../components/DashboardCard";
import api from "../services/api";

function Dashboard() {
  const navigate = useNavigate();

  const user = JSON.parse(localStorage.getItem("user") || "null");

  const [summary, setSummary] = useState(null);
  const [errorMessage, setErrorMessage] = useState("");
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const fetchDashboard = async () => {
      try {
        const response = await api.get("/dashboard");
        setSummary(response.data.data);
      } catch (error) {
        setErrorMessage("Could not load dashboard data.");
      } finally {
        setIsLoading(false);
      }
    };

    fetchDashboard();
  }, []);

  const handleLogout = async () => {
    try {
      await api.post("/logout");
    } catch (error) {
      // Even if this fails, we still clear the local session below
    }
    localStorage.removeItem("access_token");
    localStorage.removeItem("user");
    navigate("/login");
  };

  return (
    <div className="h-screen flex flex-col">
      <Navbar userEmail={user?.email} onLogout={handleLogout} />

      <div className="flex flex-1 overflow-hidden">
        <Sidebar />

        <main className="flex-1 overflow-y-auto p-6">
          <h1 className="text-xl font-bold text-gray-800 mb-6">Dashboard</h1>

          {isLoading && (
            <div className="flex items-center gap-2 text-gray-500 text-sm mb-4">
              <div className="w-4 h-4 border-2 border-gray-300 border-t-indigo-600 rounded-full animate-spin" />
              Loading...
            </div>
          )}
          {errorMessage && <p className="text-red-600">{errorMessage}</p>}

          {summary && (
            <>
              <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 mb-8">
                <DashboardCard title="Total Products" value={summary.total_products} />
                <DashboardCard title="Total Quantity" value={summary.total_quantity} />
                <DashboardCard
                  title="Low Stock Products"
                  value={summary.low_stock_count}
                  accentColor="text-red-600"
                  borderColor="border-t-red-500"
                />
              </div>

              <h2 className="text-lg font-semibold text-gray-800 mb-3">Low Stock Products</h2>

              {summary.low_stock_products.length === 0 ? (
                <p className="text-gray-500 text-sm">Nothing is low on stock right now. 🎉</p>
              ) : (
                <div className="bg-white border border-gray-200 rounded-xl overflow-hidden shadow-sm">
                  <table className="w-full text-sm text-left">
                    <thead className="bg-gray-50 text-gray-500 uppercase text-xs">
                      <tr>
                        <th className="px-4 py-3">Name</th>
                        <th className="px-4 py-3">SKU</th>
                        <th className="px-4 py-3">Quantity</th>
                      </tr>
                    </thead>
                    <tbody>
                      {summary.low_stock_products.map((product) => (
                        <tr key={product.id} className="border-t border-gray-100">
                          <td className="px-4 py-3 font-medium text-gray-800">{product.name}</td>
                          <td className="px-4 py-3 text-gray-500">{product.sku}</td>
                          <td className="px-4 py-3 text-red-600 font-medium">{product.quantity}</td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              )}
            </>
          )}
        </main>
      </div>
    </div>
  );
}

export default Dashboard;
