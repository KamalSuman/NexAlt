// import {
//   PieChart,
//   Pie,
//   Cell,
//   Tooltip,
//   Legend,
//   ResponsiveContainer,
// } from "recharts";

// const COLORS = [
//   "#0088FE",
//   "#00C49F",
//   "#FFBB28",
//   "#FF8042",
//   "#845EC2",
//   "#D65DB1",
// ];

// // JSON response directly embedded for demo (in practice, fetch from backend)
// const data = {
//   profile: {
//     age: 30,
//     income: 340000.0,
//     capital: 1000000.0,
//     expenses: 100000.0,
//     emi: 80000.0,
//     liquidity_need: 0.0,
//     dependents: 4,
//     confidence: 0.1,
//     knowledge: 0.1,
//     comfort_with_negatives: 1.0,
//     market_awareness: 0.1,
//     experience: 0.0,
//   },
//   allocation: {
//     equity: { percentage: 24.0, amount: 240000.0 },
//     debt: { percentage: 14.49, amount: 144900.0 },
//     gold: { percentage: 14.16, amount: 141600.0 },
//     real_estate: { percentage: 19.75, amount: 197500.0 },
//     crypto: { percentage: 14.72, amount: 147200.0 },
//     cash: { percentage: 12.88, amount: 128800.0 },
//   },
//   recommended_instruments: {
//     equity: [
//       "Reliance Industries (18.2%)",
//       "HDFC Bank (14.5%)",
//       "Infosys (12.1%)",
//       "ICICI Bank (10.8%)",
//       "Bharti Airtel (9.3%)",
//     ],
//     gold: ["Nippon India ETF Gold BeES", "HDFC Gold ETF", "SBI Gold ETF"],
//   },
// };

// // Create chart data with name, percentage and amount
// const allocationData = Object.entries(data.allocation).map(([key, value]) => ({
//   name: key.replace("_", " ").replace(/\b\w/g, (c) => c.toUpperCase()),
//   value: value.percentage,
//   amount: value.amount,
//   key, // to reference original key later
// }));

// export default function OutputResponse() {
//   return (
//     <div className="min-h-screen bg-[#f9fafb] p-10 text-gray-800 font-sans">
//       <h1 className="text-3xl font-semibold mb-6 text-gray-900">
//         Risk Profile Allocation
//       </h1>

//       {/* Allocation Pie Chart */}
//       <div className="bg-white rounded-xl p-6 shadow-md mb-10">
//         <h2 className="text-xl font-semibold mb-4">Asset Allocation</h2>
//         <div className="flex flex-col md:flex-row items-center gap-6">
//           <div className="w-full md:w-1/2 h-[300px]">
//             <ResponsiveContainer width="100%" height="100%">
//               <PieChart>
//                 <Pie
//                   data={allocationData}
//                   dataKey="value"
//                   nameKey="name"
//                   cx="50%"
//                   cy="50%"
//                   outerRadius={100}
//                   label={({ name, percent = 0, payload }) =>
//                     `${name}: ₹${payload.amount.toLocaleString()} (${(
//                       percent * 100
//                     ).toFixed(0)}%)`
//                   }
//                 >
//                   {allocationData.map((entry, index) => (
//                     <Cell
//                       key={`cell-${index}`}
//                       fill={COLORS[index % COLORS.length]}
//                     />
//                   ))}
//                 </Pie>
//                 <Tooltip
//                   formatter={(value: number, name: string, props: any) => [
//                     `${value.toFixed(2)}%`,
//                     name,
//                   ]}
//                 />
//                 <Legend />
//               </PieChart>
//             </ResponsiveContainer>
//           </div>

//           <div className="flex-1 space-y-2">
//             {allocationData.map((item, index) => (
//               <div key={item.name} className="flex items-center gap-2">
//                 <div
//                   className="w-4 h-4 rounded-full"
//                   style={{ backgroundColor: COLORS[index % COLORS.length] }}
//                 ></div>
//                 <span>
//                   {item.name}: ₹{item.amount.toLocaleString()} ({item.value}%)
//                 </span>
//               </div>
//             ))}
//           </div>
//         </div>
//       </div>

//       {/* Recommended Instruments */}
//       <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
//         {Object.entries(data.recommended_instruments).map(
//           ([category, items]) => (
//             <div key={category} className="bg-white rounded-xl p-6 shadow-md">
//               <h3 className="text-lg font-medium capitalize mb-4">
//                 {category} Instruments
//               </h3>
//               <ul className="space-y-2">
//                 {items.map((item, idx) => (
//                   <li
//                     key={idx}
//                     className="bg-gray-100 text-sm px-3 py-2 rounded-md shadow-sm"
//                   >
//                     {item}
//                   </li>
//                 ))}
//               </ul>
//             </div>
//           )
//         )}
//       </div>

//       <div className="bg-white rounded-xl p-6 shadow-md w-full md:w-2/3">
//         <h3 className="text-lg font-semibold mb-4">Top Issues</h3>

//         <div className="grid grid-cols-2 text-sm font-semibold text-gray-500 border-b pb-2 mb-3">
//           <div>Type of issues</div>
//           <div>Number of issues</div>
//         </div>

//         {Object.entries(data.recommended_instruments).map(
//           ([issueType, values], idx) => (
//             <div
//               key={idx}
//               className="grid grid-cols-2 text-sm text-gray-700 py-1 border-b last:border-b-0"
//             >
//               <div className="pr-2">{issueType}</div>
//               <div className="text-right">
//                 {values.length > 1 ? values.length : values[0]}
//               </div>
//             </div>
//           )
//         )}
//       </div>
//     </div>
//   );
// }

import {
  PieChart,
  Pie,
  Cell,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from "recharts";
import {
  Dialog,
  DialogTitle,
  DialogContent,
  IconButton,
  CircularProgress,
} from "@mui/material";
import CloseIcon from "@mui/icons-material/Close";
import DenseTable from "../Table";
import { useEffect, useState } from "react";

const COLORS = [
  "#0088FE",
  "#00C49F",
  "#FFBB28",
  "#FF8042",
  "#845EC2",
  "#D65DB1",
];

const data = {
  allocation: {
    equity: { percentage: 24.0, amount: 240000.0 },
    debt: { percentage: 14.49, amount: 144900.0 },
    gold: { percentage: 14.16, amount: 141600.0 },
    real_estate: { percentage: 19.75, amount: 197500.0 },
    crypto: { percentage: 14.72, amount: 147200.0 },
    cash: { percentage: 12.88, amount: 128800.0 },
  },
};

const allocationData = Object.entries(data.allocation).map(([key, value]) => ({
  name: key.replace("_", " ").replace(/\b\w/g, (c) => c.toUpperCase()),
  value: value.percentage,
  amount: value.amount,
}));

export default function OutputResponse({}) {
  const [selectedAsset, setSelectedAsset] = useState<
    null | (typeof allocationData)[0]
  >(null);

  const handleSliceClick = (_: any, index: number) => {
    setSelectedAsset(allocationData[index]);
  };

  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // simulate loading
    const timer = setTimeout(() => setLoading(false), 10000);

    return () => clearTimeout(timer);
  }, []);

  return (
    <div className="p-10 mx-[15%]">
      {loading ? (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-[#2a2828] bg-opacity-50">
          <CircularProgress color="secondary" />
        </div>
      ) : (
        ""
      )}
      <h1 className="text-3xl font-bold mb-10 text-center">Asset Allocation</h1>

      <div className="flex flex-col md:flex-row gap-8 bg-indigo-50 border border-indigo-200 rounded-xl shadow-lg p-6">
        {/* Pie Chart Section */}
        <div className="w-full md:w-1/2 h-[300px]">
          <ResponsiveContainer width="100%" height="100%">
            <PieChart>
              <Pie
                data={allocationData}
                dataKey="value"
                nameKey="name"
                cx="50%"
                cy="50%"
                outerRadius={100}
                onClick={handleSliceClick}
              >
                {allocationData.map((entry, index) => (
                  <Cell key={index} fill={COLORS[index % COLORS.length]} />
                ))}
              </Pie>
              <Tooltip />
              <Legend />
            </PieChart>
          </ResponsiveContainer>
        </div>

        {/* Allocation Data Section */}
        <div className="flex-1 space-y-2 mt-4 md:mt-6">
          {allocationData.map((item, index) => (
            <div key={item.name} className="flex items-center gap-2">
              <div
                className="w-4 h-4 rounded-full"
                style={{ backgroundColor: COLORS[index % COLORS.length] }}
              ></div>
              <span>
                {item.name}: ₹{item.amount.toLocaleString()} ({item.value}%)
              </span>
            </div>
          ))}
        </div>
      </div>

      {/* Dialog for clicked asset */}
      <Dialog
        open={!!selectedAsset}
        onClose={() => setSelectedAsset(null)}
        PaperProps={{
          sx: {
            width: "660px",
            maxWidth: "660px",
            m: 0,
            bgcolor: "#0f172a", // Dark blue
            color: "#fff", // White text
          },
        }}
      >
        <DialogTitle
          sx={{
            textAlign: "center",
            px: "5px",
            py: 1,
            position: "relative",
            bgcolor: "#0f172a", // Match dialog background
            color: "#fff",
          }}
        >
          {selectedAsset?.name} Details
          <IconButton
            aria-label="close"
            onClick={() => setSelectedAsset(null)}
            sx={{ position: "absolute", right: 8, top: 8, color: "#fff" }}
          >
            <CloseIcon />
          </IconButton>
        </DialogTitle>

        <DialogContent
          dividers
          sx={{ p: 0, bgcolor: "#285bad" /* light blue */ }}
        >
          <div style={{ width: "100%", overflowX: "auto" }}>
            {selectedAsset && (
              <DenseTable
                names={[selectedAsset.name]}
                amounts={[selectedAsset.amount]}
                percentages={[selectedAsset.value]}
              />
            )}
          </div>
        </DialogContent>
      </Dialog>
    </div>
  );
}
