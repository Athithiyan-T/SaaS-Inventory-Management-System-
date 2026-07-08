import { useState } from "react";
import { useNavigate } from "react-router-dom";
import Navbar from "../components/Navbar";
import Sidebar from "../components/Sidebar";
import ProductForm from "../components/ProductForm";
import api from "../services/api";

function AddProduct() {
  const navigate = useNavigate();
  const user = JSON.parse(localStorage.getItem("user") || "null");

  const [errorMessage, setErrorMessage] = useState("");

  const handleSubmit = async (formData) => {
    setErrorMessage("");
    try {
      await api.post("/products", formData);
      navigate("/products");
    } catch (error) {
      const message = error.response?.data?.message || "Could not create product.";
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
          <h1 className="text-xl font-bold text-gray-800 mb-6">Add Product</h1>

          <div className="max-w-xl">
            <ProductForm onSubmit={handleSubmit} submitLabel="Add Product" errorMessage={errorMessage} />
          </div>
        </main>
      </div>
    </div>
  );
}

export default AddProduct;
