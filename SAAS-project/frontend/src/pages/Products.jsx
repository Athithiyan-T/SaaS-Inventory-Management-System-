import { useEffect, useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import Navbar from "../components/Navbar";
import Sidebar from "../components/Sidebar";
import ProductTable from "../components/ProductTable";
import api from "../services/api";

function Products() {
  const navigate = useNavigate();
  const user = JSON.parse(localStorage.getItem("user") || "null");

  const [products, setProducts] = useState([]);
  const [searchTerm, setSearchTerm] = useState("");
  const [errorMessage, setErrorMessage] = useState("");
  const [isLoading, setIsLoading] = useState(true);

  const fetchProducts = async (search = "") => {
    setIsLoading(true);
    try {
      const response = await api.get("/products", { params: { search } });
      setProducts(response.data.data);
    } catch (error) {
      setErrorMessage("Could not load products.");
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    fetchProducts();
  }, []);

  const handleSearchSubmit = (e) => {
    e.preventDefault();
    fetchProducts(searchTerm);
  };

  const handleDelete = async (productId) => {
    const confirmed = window.confirm("Are you sure you want to delete this product?");
    if (!confirmed) return;

    try {
      await api.delete(`/products/${productId}`);
      setProducts((prev) => prev.filter((p) => p.id !== productId));
    } catch (error) {
      alert("Could not delete this product. Please try again.");
    }
  };

  const handleLogout = async () => {
    try {
      await api.post("/logout");
    } catch (error) {
      // ignore, we clear locally anyway
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
          <div className="flex items-center justify-between mb-6">
            <h1 className="text-xl font-bold text-gray-800">Products</h1>
            <Link
              to="/products/add"
              className="bg-indigo-600 hover:bg-indigo-700 text-white text-sm font-medium px-4 py-2 rounded-lg transition-colors"
            >
              + Add Product
            </Link>
          </div>

          <form onSubmit={handleSearchSubmit} className="mb-4 flex gap-2">
            <input
              type="text"
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              placeholder="Search by name or SKU..."
              className="w-full max-w-sm border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500"
            />
            <button
              type="submit"
              className="bg-gray-100 hover:bg-gray-200 text-gray-700 text-sm font-medium px-4 py-2 rounded-lg transition-colors"
            >
              Search
            </button>
          </form>

          {isLoading && (
            <div className="flex items-center gap-2 text-gray-500 text-sm mb-4">
              <div className="w-4 h-4 border-2 border-gray-300 border-t-indigo-600 rounded-full animate-spin" />
              Loading...
            </div>
          )}
          {errorMessage && <p className="text-red-600">{errorMessage}</p>}

          {!isLoading && !errorMessage && (
            <ProductTable products={products} onDelete={handleDelete} />
          )}
        </main>
      </div>
    </div>
  );
}

export default Products;
