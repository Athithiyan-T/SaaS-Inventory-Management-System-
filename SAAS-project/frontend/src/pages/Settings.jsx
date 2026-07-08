import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import Navbar from "../components/Navbar";
import Sidebar from "../components/Sidebar";
import api from "../services/api";

function Settings() {
  const navigate = useNavigate();
  const user = JSON.parse(localStorage.getItem("user") || "null");

  const [threshold, setThreshold] = useState("");
  const [errorMessage, setErrorMessage] = useState("");
  const [successMessage, setSuccessMessage] = useState("");
  const [isLoading, setIsLoading] = useState(true);
  const [isSaving, setIsSaving] = useState(false);

  useEffect(() => {
    const fetchSettings = async () => {
      try {
        const response = await api.get("/settings");
        setThreshold(response.data.data.default_low_stock_threshold);
      } catch (error) {
        setErrorMessage("Could not load settings.");
      } finally {
        setIsLoading(false);
      }
    };

    fetchSettings();
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setErrorMessage("");
    setSuccessMessage("");
    setIsSaving(true);

    try {
      await api.put("/settings", { default_low_stock_threshold: Number(threshold) });
      setSuccessMessage("Settings updated successfully.");
    } catch (error) {
      const message = error.response?.data?.message || "Could not update settings.";
      setErrorMessage(message);
    } finally {
      setIsSaving(false);
    }
  };

  const handleLogout = async () => {
    try {
      await api.post("/logout");
    } catch (error) {
      // ignore
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
          <h1 className="text-xl font-bold text-gray-800 mb-6">Settings</h1>

          {isLoading ? (
            <div className="flex items-center gap-2 text-gray-500 text-sm">
              <div className="w-4 h-4 border-2 border-gray-300 border-t-indigo-600 rounded-full animate-spin" />
              Loading...
            </div>
          ) : (
            <div className="max-w-md bg-white border border-gray-200 rounded-xl shadow-sm p-6">
              {errorMessage && (
                <div className="bg-red-50 text-red-600 text-sm rounded-lg px-3 py-2 mb-4">
                  {errorMessage}
                </div>
              )}
              {successMessage && (
                <div className="bg-green-50 text-green-600 text-sm rounded-lg px-3 py-2 mb-4">
                  {successMessage}
                </div>
              )}

              <form onSubmit={handleSubmit} className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Default Low Stock Threshold
                  </label>
                  <p className="text-xs text-gray-400 mb-2">
                    Used for any product that doesn't have its own threshold set.
                  </p>
                  <input
                    type="number"
                    min="0"
                    value={threshold}
                    onChange={(e) => setThreshold(e.target.value)}
                    className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500"
                  />
                </div>

                <button
                  type="submit"
                  disabled={isSaving}
                  className="w-full bg-indigo-600 hover:bg-indigo-700 text-white font-medium py-2.5 rounded-lg transition-colors disabled:opacity-60"
                >
                  {isSaving ? "Saving..." : "Save Settings"}
                </button>
              </form>
            </div>
          )}
        </main>
      </div>
    </div>
  );
}

export default Settings;
