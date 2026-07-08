/**
 * DashboardCard
 *
 * A small reusable card used on the Dashboard page to show one
 * summary statistic (e.g. Total Products, Total Quantity).
 *
 * Props:
 * - title: string - label shown above the number
 * - value: string | number - the stat itself
 * - accentColor: string - optional Tailwind color class for the value text
 */
function DashboardCard({ title, value, accentColor = "text-indigo-600", borderColor = "border-t-indigo-500" }) {
  return (
    <div className={`bg-white rounded-xl border border-gray-200 border-t-4 ${borderColor} shadow-sm p-6 hover:shadow-md transition-shadow`}>
      <p className="text-sm font-medium text-gray-500">{title}</p>
      <p className={`text-3xl font-bold mt-2 ${accentColor}`}>{value}</p>
    </div>
  );
}

export default DashboardCard;
