import { useState } from "react";

/**
 * ProductForm
 *
 * A form for creating or editing a product. Used by both the
 * "Add Product" and "Edit Product" pages.
 *
 * Props:
 * - initialValues: object - starting values for the form fields (optional)
 * - onSubmit: function(formData) - called with the form data when submitted
 * - submitLabel: string - text shown on the submit button
 * - errorMessage: string - error text to show above the form (optional)
 */
function ProductForm({ initialValues = {}, onSubmit, submitLabel = "Save", errorMessage }) {
  const [formData, setFormData] = useState({
    name: initialValues.name || "",
    sku: initialValues.sku || "",
    description: initialValues.description || "",
    quantity: initialValues.quantity ?? 0,
    cost_price: initialValues.cost_price ?? 0,
    selling_price: initialValues.selling_price ?? 0,
    low_stock_threshold: initialValues.low_stock_threshold ?? "",
  });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();

    // Convert numeric fields from strings to numbers before submitting
    onSubmit({
      ...formData,
      quantity: Number(formData.quantity) || 0,
      cost_price: Number(formData.cost_price) || 0,
      selling_price: Number(formData.selling_price) || 0,
      low_stock_threshold:
        formData.low_stock_threshold === "" ? null : Number(formData.low_stock_threshold),
    });
  };

  // Small helper so we don't repeat the same input styles everywhere
  const inputClasses =
    "w-full border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500";

  return (
    <form onSubmit={handleSubmit} className="bg-white border border-gray-200 rounded-xl shadow-sm p-6 space-y-4">
      {errorMessage && (
        <div className="bg-red-50 text-red-600 text-sm rounded-lg px-3 py-2">{errorMessage}</div>
      )}

      <div>
        <label className="block text-sm font-medium text-gray-700 mb-1">Product Name *</label>
        <input
          type="text"
          name="name"
          value={formData.name}
          onChange={handleChange}
          className={inputClasses}
          placeholder="e.g. Wireless Mouse"
        />
      </div>

      <div>
        <label className="block text-sm font-medium text-gray-700 mb-1">SKU *</label>
        <input
          type="text"
          name="sku"
          value={formData.sku}
          onChange={handleChange}
          className={inputClasses}
          placeholder="e.g. WM-001"
        />
      </div>

      <div>
        <label className="block text-sm font-medium text-gray-700 mb-1">Description</label>
        <textarea
          name="description"
          value={formData.description}
          onChange={handleChange}
          rows={3}
          className={inputClasses}
          placeholder="Optional short description"
        />
      </div>

      <div className="grid grid-cols-2 gap-4">
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">Quantity</label>
          <input
            type="number"
            name="quantity"
            value={formData.quantity}
            onChange={handleChange}
            className={inputClasses}
            min="0"
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">Low Stock Threshold</label>
          <input
            type="number"
            name="low_stock_threshold"
            value={formData.low_stock_threshold}
            onChange={handleChange}
            className={inputClasses}
            placeholder="Leave blank to use default"
            min="0"
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">Cost Price</label>
          <input
            type="number"
            name="cost_price"
            value={formData.cost_price}
            onChange={handleChange}
            className={inputClasses}
            min="0"
            step="0.01"
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">Selling Price</label>
          <input
            type="number"
            name="selling_price"
            value={formData.selling_price}
            onChange={handleChange}
            className={inputClasses}
            min="0"
            step="0.01"
          />
        </div>
      </div>

      <button
        type="submit"
        className="w-full bg-indigo-600 hover:bg-indigo-700 active:bg-indigo-800 text-white font-medium py-2.5 rounded-lg transition-colors focus:outline-none focus:ring-2 focus:ring-indigo-300"
      >
        {submitLabel}
      </button>
    </form>
  );
}

export default ProductForm;
