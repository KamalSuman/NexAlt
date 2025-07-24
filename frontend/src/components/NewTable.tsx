"use client";
import React, { useState } from "react";
import {
  PieChart,
  Pie,
  Cell,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from "recharts";

type DataCardProps = {
  title: string;
  columnName: string[];
  amount: number[];
  percentage: number[];
};

const COLORS = [
  "#3A2FC9",
  "#FF6B6B",
  "#FFC300",
  "#36CFC9",
  "#FF7A45",
  "#00B8D9",
];

const DataCardWithChartSwitch = ({
  title,
  columnName,
  amount,
  percentage,
}: DataCardProps) => {
  const [view, setView] = useState<"table" | "pie">("table");
  const [pieDataKey, setPieDataKey] = useState<"amount" | "percentage">(
    "amount"
  );

  // Prepare data for pie chart based on selected dataKey
  const pieData = columnName.map((name, i) => ({
    name,
    value: pieDataKey === "amount" ? amount[i] : percentage[i],
  }));

  return (
    <div className="max-w-md mx-auto bg-white rounded-lg shadow-lg p-6 mb-6">
      <div className="flex justify-between items-center mb-4">
        <h3 className="text-lg font-semibold">{title}</h3>

        {/* View Switch Buttons */}
        <div className="flex space-x-2">
          <button
            onClick={() => setView("table")}
            className={`px-3 py-1 rounded ${
              view === "table"
                ? "bg-indigo-600 text-white"
                : "bg-gray-200 text-gray-700"
            }`}
          >
            Table
          </button>
          <button
            onClick={() => setView("pie")}
            className={`px-3 py-1 rounded ${
              view === "pie"
                ? "bg-indigo-600 text-white"
                : "bg-gray-200 text-gray-700"
            }`}
          >
            Pie Chart
          </button>
        </div>
      </div>

      {/* Show pie data key toggle only if Pie Chart is active */}
      {view === "pie" && (
        <div className="mb-4 flex justify-center space-x-4">
          <button
            onClick={() => setPieDataKey("amount")}
            className={`px-3 py-1 rounded ${
              pieDataKey === "amount"
                ? "bg-purple-600 text-white"
                : "bg-gray-200 text-gray-700"
            }`}
          >
            Amount
          </button>
          <button
            onClick={() => setPieDataKey("percentage")}
            className={`px-3 py-1 rounded ${
              pieDataKey === "percentage"
                ? "bg-purple-600 text-white"
                : "bg-gray-200 text-gray-700"
            }`}
          >
            Percentage
          </button>
        </div>
      )}

      {view === "table" ? (
        <div className="overflow-x-auto">
          <table className="min-w-full border border-gray-300 rounded-lg">
            <thead className="bg-gray-100">
              <tr>
                <th className="px-4 py-2 text-left border-b border-gray-300">
                  Month
                </th>
                <th className="px-4 py-2 text-right border-b border-gray-300">
                  Amount ($)
                </th>
                <th className="px-4 py-2 text-right border-b border-gray-300">
                  Percentage (%)
                </th>
              </tr>
            </thead>
            <tbody>
              {columnName.map((month, i) => (
                <tr
                  key={month}
                  className={i % 2 === 0 ? "bg-white" : "bg-gray-50"}
                >
                  <td className="px-4 py-2 border-b border-gray-300">
                    {month}
                  </td>
                  <td className="px-4 py-2 text-right border-b border-gray-300">
                    {amount[i].toLocaleString()}
                  </td>
                  <td className="px-4 py-2 text-right border-b border-gray-300">
                    {percentage[i]}%
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      ) : (
        <div style={{ width: "100%", height: 320 }}>
          <ResponsiveContainer>
            <PieChart>
              <Pie
                data={pieData}
                dataKey="value"
                nameKey="name"
                cx="50%"
                cy="50%"
                outerRadius={100}
                label={({ name, percent }) =>
                  name && typeof percent === "number"
                    ? `${name}: ${(percent * 100).toFixed(0)}%`
                    : name
                }
                labelLine={false}
              >
                {pieData.map((entry, index) => (
                  <Cell
                    key={`cell-${index}`}
                    fill={COLORS[index % COLORS.length]}
                  />
                ))}
              </Pie>
              <Tooltip
                formatter={(value: number) =>
                  pieDataKey === "amount"
                    ? `$${value.toLocaleString()}`
                    : `${value}%`
                }
              />
              <Legend verticalAlign="bottom" height={36} />
            </PieChart>
          </ResponsiveContainer>
        </div>
      )}
    </div>
  );
};

export default DataCardWithChartSwitch;
