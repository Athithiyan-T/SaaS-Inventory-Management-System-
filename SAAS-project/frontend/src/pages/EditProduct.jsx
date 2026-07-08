import { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import Navbar from "../components/Navbar";
import Sidebar from "../components/Sidebar";
import ProductForm from "../components/ProductForm";
import api from "../services/api";

function EditProduct() {
  const { id } = useParams();
  const navigate = useNavigate();
  const user = JSON.parse(localStorage.getItem("user") || "null");

  const [product, setProduct] = useState(null);
  const [errorMessage, setErrorMessage] = useState("");
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const fetchProduct = async () => {
      try {
        const response = await api.get(`/products/${id}`);
        setProduct(response.data.data);
      } catch (error) {
        setErrorMessage("Could not load this product.");
      } finally {
        setIsLoading(false);
      }
    };

    fetchProduct();
  }, [id]);

  const handleSubmit = async (formData) => {
    setErrorMessage("");
    try {
      await api.put(`/products/${id}`, formData);
      navigate("/products");
    } catch (error) {
      const message = error.response?.data?.message || "Could not update product.";
      setErrorMessage(message);
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
          <h1 className="text-xl font-bold text-gray-800 mb-6">Edit Product</h1>

          {isLoading && (
            <div className="flex items-center gap-2 text-gray-500 text-sm mb-4">
              <div className="w-4 h-4 border-2 border-gray-300 border-t-indigo-600 rounded-full animate-spin" />
              Loading...
            </div>
          )}

          <div className="max-w-xl">
            {product && (
              <ProductForm
                initialValues={product}
                onSubmit={handleSubmit}
                submitLabel="Save Changes"
                errorMessage={errorMessage}
              />
            )}
          </div>
        </main>
      </div>
    </div>
  );
}

export default EditProduct;
