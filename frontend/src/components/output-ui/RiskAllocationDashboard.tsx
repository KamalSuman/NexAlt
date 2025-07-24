import React from "react";
import {
  PieChart,
  Pie,
  Cell,
  Legend,
  Tooltip,
  ResponsiveContainer,
} from "recharts";

const COLORS = [
  "#4c6ef5",
  "#20c997",
  "#f59f00",
  "#845ef7",
  "#ff6b6b",
  "#adb5bd",
];

const data = {
  profile: {
    age: 30,
    income: 340000.0,
    capital: 1000000.0,
    expenses: 100000.0,
    emi: 80000.0,
    liquidity_need: 0.0,
    dependents: 4,
    confidence: 0.1,
    knowledge: 0.1,
    comfort_with_negatives: 0.0,
    market_awareness: 0.1,
    experience: 0.0,
  },
  allocation: {
    equity: 16.61,
    debt: 14.35,
    gold: 15.03,
    real_estate: 23.22,
    crypto: 17.14,
    cash: 13.64,
  },
  recommended_instruments: {
    equity: [
      "HDFC Bank (15.5%)",
      "TCS (12.3%)",
      "Infosys (10.8%)",
      "HUL (9.7%)",
      "ITC (8.2%)",
    ],
    gold: ["Nippon India ETF Gold BeES", "HDFC Gold ETF", "SBI Gold ETF"],
  },
  comparisons: [
    { label: "Your site", value: 80, color: "#4c6ef5" },
    { label: "Top-10% website", value: 80, color: "#f76707" },
  ],
  risk_profile: "low",
};

type Allocation = Record<string, number>;
type Profile = Record<string, number>;
type Instruments = Record<string, string[]>;
type Comparison = { label: string; value: number; color: string };

interface AllocationPieChartProps {
  allocation: Allocation;
}

interface ProfileSectionProps {
  profile: Profile;
}

interface InstrumentsSectionProps {
  instruments: Instruments;
}

interface ComparisonCardProps {
  title: string;
  items: Comparison[];
}

const AllocationPieChart = ({ allocation }: AllocationPieChartProps) => {
  const chartData = Object.entries(allocation).map(([key, value]) => ({
    name: key,
    value,
  }));

  return (
    <ResponsiveContainer width="100%" height={300}>
      <PieChart>
        <Pie
          data={chartData}
          cx="50%"
          cy="50%"
          labelLine={false}
          label={({ name, percent = 0 }) =>
            `${name} (${(percent * 100).toFixed(0)}%)`
          }
          outerRadius={100}
          fill="#8884d8"
          dataKey="value"
        >
          {chartData.map((entry, index) => (
            <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
          ))}
        </Pie>
        <Tooltip />
        <Legend />
      </PieChart>
    </ResponsiveContainer>
  );
};

const ProfileSection = ({ profile }: ProfileSectionProps) => (
  <div className="grid grid-cols-2 gap-4 p-4 bg-white shadow rounded-xl">
    {Object.entries(profile).map(([key, value]) => (
      <div key={key} className="text-sm text-gray-700">
        <span className="font-semibold capitalize">
          {key.replace(/_/g, " ")}:
        </span>{" "}
        {value}
      </div>
    ))}
  </div>
);

const InstrumentsSection = ({ instruments }: InstrumentsSectionProps) => (
  <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mt-6">
    {Object.entries(instruments).map(([category, items]) => (
      <div key={category} className="bg-white p-4 rounded-xl shadow">
        <h2 className="text-md font-bold capitalize mb-2">{category}</h2>
        <ul className="list-disc list-inside text-sm text-gray-700">
          {items.map((item, idx) => (
            <li key={idx}>{item}</li>
          ))}
        </ul>
      </div>
    ))}
  </div>
);

const ComparisonCard = ({ title, items }: ComparisonCardProps) => (
  <div className="bg-white rounded-xl shadow p-4 w-full">
    <h2 className="text-center text-sm font-semibold text-gray-600 mb-2">
      {title}
    </h2>
    <hr className="mb-3" />
    <div className="space-y-2">
      {items.map((item, index) => (
        <div key={index} className="flex justify-between text-sm text-gray-700">
          <div className="flex items-center space-x-2">
            <span
              className="inline-block w-3 h-3 rounded-full"
              style={{ backgroundColor: item.color }}
            ></span>
            <span>{item.label}</span>
          </div>
          <span style={{ color: item.color }}>{item.value}%</span>
        </div>
      ))}
    </div>
  </div>
);

const RiskAllocationDashboard = () => {
  return (
    <div className="p-6 bg-gray-100 min-h-screen">
      <h1 className="text-2xl font-bold mb-6">Risk Profile Dashboard</h1>
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <ProfileSection profile={data.profile} />
        <div className="bg-white rounded-xl shadow p-4">
          <h2 className="text-md font-bold mb-4">Asset Allocation</h2>
          <AllocationPieChart allocation={data.allocation} />
        </div>
      </div>
      <div className="mt-6">
        <ComparisonCard title="Your site" items={data.comparisons} />
      </div>
      <InstrumentsSection instruments={data.recommended_instruments} />
    </div>
  );
};

export default RiskAllocationDashboard;
