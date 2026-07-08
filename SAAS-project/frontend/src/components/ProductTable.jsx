import { Link } from "react-router-dom";

/**
 * ProductTable
 *
 * Displays a list of products in a table, with Edit and Delete actions.
 *
 * Props:
 * - products: array of product objects (see backend Product model)
 * - onDelete: function(productId) - called when the Delete button is clicked
 */
function ProductTable({ products, onDelete }) {
  if (!products || products.length === 0) {
    return (
      <div className="bg-white border border-gray-200 rounded-xl p-8 text-center text-gray-500">
        No products found. Try adding one!
      </div>
    );
  }

  return (
    <div className="bg-white border border-gray-200 rounded-xl overflow-hidden shadow-sm">
      <table className="w-full text-sm text-left">
        <thead className="bg-gray-50 text-gray-500 uppercase text-xs">
          <tr>
            <th className="px-4 py-3">Name</th>
            <th className="px-4 py-3">SKU</th>
            <th className="px-4 py-3">Quantity</th>
            <th className="px-4 py-3">Cost Price</th>
            <th className="px-4 py-3">Selling Price</th>
            <th className="px-4 py-3 text-right">Actions</th>
          </tr>
        </thead>
        <tbody>
          {products.map((product) => (
            <tr key={product.id} className="border-t border-gray-100 hover:bg-gray-50">
              <td className="px-4 py-3 font-medium text-gray-800">{product.name}</td>
              <td className="px-4 py-3 text-gray-500">{product.sku}</td>
              <td className="px-4 py-3">{product.quantity}</td>
              <td className="px-4 py-3">₹{product.cost_price}</td>
              <td className="px-4 py-3">₹{product.selling_price}</td>
              <td className="px-4 py-3 text-right space-x-3">
                <Link
                  to={`/products/${product.id}/edit`}
                  className="text-indigo-600 hover:underline font-medium"
                >
                  Edit
                </Link>
                <button
                  onClick={() => onDelete(product.id)}
                  className="text-red-600 hover:underline font-medium"
                >
                  Delete
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default ProductTable;
