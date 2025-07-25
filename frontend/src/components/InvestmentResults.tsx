import React from 'react';
import { PieChart, Pie, Cell, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';
import { TrendingUp, IndianRupee, Target, Award } from 'lucide-react';

interface AllocationData {
  percentage: number;
  amount: number;
}

interface Recommendation {
  symbol: string;
  name?: string;
  weight: number;
  amount: number;
}

interface InvestmentData {
  allocation: {
    equity: AllocationData;
    debt: AllocationData;
    gold: AllocationData;
    real_estate: AllocationData;
    crypto: AllocationData;
    cash: AllocationData;
  };
  equity_recommendations?: Recommendation[];
  bond_recommendations?: Recommendation[];
  crypto_recommendations?: Recommendation[];
  currency_recommendations?: Recommendation[];
  risk_profile?: string;
}

interface InvestmentResultsProps {
  data: InvestmentData;
}

const COLORS = ['#8884d8', '#82ca9d', '#ffc658', '#ff7300', '#8dd1e1', '#d084d0'];

const InvestmentResults: React.FC<InvestmentResultsProps> = ({ data }) => {
  const allocationData = Object.entries(data.allocation).map(([key, value], index) => ({
    name: key.replace('_', ' ').toUpperCase(),
    value: value.percentage,
    amount: value.amount,
    color: COLORS[index]
  }));

  const totalAmount = Object.values(data.allocation).reduce((sum, item) => sum + item.amount, 0);

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 to-gray-800 text-white p-6">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold mb-2">Investment Portfolio Analysis</h1>
          <p className="text-gray-300">Your personalized investment recommendations</p>
          {data.risk_profile && (
            <div className="mt-4 inline-flex items-center px-4 py-2 bg-blue-600 rounded-full">
              <Target className="w-5 h-5 mr-2" />
              Risk Profile: {data.risk_profile.toUpperCase()}
            </div>
          )}
        </div>

        {/* Summary Cards */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          <div className="bg-gray-800 rounded-lg p-6 border border-gray-700">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-gray-400 text-sm">Total Investment</p>
                <p className="text-2xl font-bold">₹{totalAmount.toLocaleString()}</p>
              </div>
              <IndianRupee className="w-8 h-8 text-green-500" />
            </div>
          </div>
          
          <div className="bg-gray-800 rounded-lg p-6 border border-gray-700">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-gray-400 text-sm">Asset Classes</p>
                <p className="text-2xl font-bold">{Object.keys(data.allocation).length}</p>
              </div>
              <TrendingUp className="w-8 h-8 text-blue-500" />
            </div>
          </div>

          <div className="bg-gray-800 rounded-lg p-6 border border-gray-700">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-gray-400 text-sm">Recommendations</p>
                <p className="text-2xl font-bold">
                  {(data.equity_recommendations?.length || 0) + 
                   (data.bond_recommendations?.length || 0) + 
                   (data.crypto_recommendations?.length || 0)}
                </p>
              </div>
              <Award className="w-8 h-8 text-yellow-500" />
            </div>
          </div>
        </div>

        {/* Charts Section */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8">
          {/* Pie Chart */}
          <div className="bg-gray-800 rounded-lg p-6 border border-gray-700">
            <h3 className="text-xl font-semibold mb-4">Asset Allocation</h3>
            <ResponsiveContainer width="100%" height={300}>
              <PieChart>
                <Pie
                  data={allocationData}
                  cx="50%"
                  cy="50%"
                  labelLine={false}
                  label={({ name, value }) => `${name}: ${value}%`}
                  outerRadius={80}
                  fill="#8884d8"
                  dataKey="value"
                >
                  {allocationData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                  ))}
                </Pie>
                <Tooltip formatter={(value) => [`${value}%`, 'Allocation']} />
              </PieChart>
            </ResponsiveContainer>
          </div>

          {/* Bar Chart */}
          <div className="bg-gray-800 rounded-lg p-6 border border-gray-700">
            <h3 className="text-xl font-semibold mb-4">Investment Amount by Asset</h3>
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={allocationData}>
                <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
                <XAxis dataKey="name" stroke="#9CA3AF" />
                <YAxis stroke="#9CA3AF" />
                <Tooltip 
                  formatter={(value) => [`₹${Number(value).toLocaleString()}`, 'Amount']}
                  labelStyle={{ color: '#000' }}
                />
                <Bar dataKey="amount" fill="#8884d8" />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Recommendations Tables */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Equity Recommendations */}
          {data.equity_recommendations && data.equity_recommendations.length > 0 && (
            <div className="bg-gray-800 rounded-lg p-6 border border-gray-700">
              <h3 className="text-xl font-semibold mb-4 flex items-center">
                <TrendingUp className="w-5 h-5 mr-2 text-green-500" />
                Equity Recommendations
              </h3>
              <div className="overflow-x-auto">
                <table className="w-full text-sm">
                  <thead>
                    <tr className="border-b border-gray-600">
                      <th className="text-left py-2">Symbol</th>
                      <th className="text-right py-2">Weight</th>
                      <th className="text-right py-2">Amount</th>
                    </tr>
                  </thead>
                  <tbody>
                    {data.equity_recommendations.map((item, index) => (
                      <tr key={index} className="border-b border-gray-700">
                        <td className="py-2 font-medium">{item.symbol}</td>
                        <td className="text-right py-2">{item.weight.toFixed(1)}%</td>
                        <td className="text-right py-2">₹{item.amount.toLocaleString()}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          )}

          {/* Bond Recommendations */}
          {data.bond_recommendations && data.bond_recommendations.length > 0 && (
            <div className="bg-gray-800 rounded-lg p-6 border border-gray-700">
              <h3 className="text-xl font-semibold mb-4 flex items-center">
                <Award className="w-5 h-5 mr-2 text-blue-500" />
                Bond Recommendations
              </h3>
              <div className="overflow-x-auto">
                <table className="w-full text-sm">
                  <thead>
                    <tr className="border-b border-gray-600">
                      <th className="text-left py-2">Name</th>
                      <th className="text-right py-2">Weight</th>
                      <th className="text-right py-2">Amount</th>
                    </tr>
                  </thead>
                  <tbody>
                    {data.bond_recommendations.map((item, index) => (
                      <tr key={index} className="border-b border-gray-700">
                        <td className="py-2 font-medium">{item.name || item.symbol}</td>
                        <td className="text-right py-2">{item.weight.toFixed(1)}%</td>
                        <td className="text-right py-2">₹{item.amount.toLocaleString()}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          )}

          {/* Crypto Recommendations */}
          {data.crypto_recommendations && data.crypto_recommendations.length > 0 && (
            <div className="bg-gray-800 rounded-lg p-6 border border-gray-700">
              <h3 className="text-xl font-semibold mb-4 flex items-center">
                <IndianRupee className="w-5 h-5 mr-2 text-yellow-500" />
                Crypto Recommendations
              </h3>
              <div className="overflow-x-auto">
                <table className="w-full text-sm">
                  <thead>
                    <tr className="border-b border-gray-600">
                      <th className="text-left py-2">Symbol</th>
                      <th className="text-right py-2">Weight</th>
                      <th className="text-right py-2">Amount</th>
                    </tr>
                  </thead>
                  <tbody>
                    {data.crypto_recommendations.map((item, index) => (
                      <tr key={index} className="border-b border-gray-700">
                        <td className="py-2 font-medium">{item.symbol}</td>
                        <td className="text-right py-2">{item.weight.toFixed(1)}%</td>
                        <td className="text-right py-2">₹{item.amount.toLocaleString()}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          )}

          {/* Currency/Cash Recommendations */}
          {data.currency_recommendations && data.currency_recommendations.length > 0 && (
            <div className="bg-gray-800 rounded-lg p-6 border border-gray-700">
              <h3 className="text-xl font-semibold mb-4 flex items-center">
                <IndianRupee className="w-5 h-5 mr-2 text-green-500" />
                Currency Recommendations
              </h3>
              <div className="overflow-x-auto">
                <table className="w-full text-sm">
                  <thead>
                    <tr className="border-b border-gray-600">
                      <th className="text-left py-2">Currency</th>
                      <th className="text-right py-2">Weight</th>
                      <th className="text-right py-2">Amount</th>
                    </tr>
                  </thead>
                  <tbody>
                    {data.currency_recommendations.map((item, index) => (
                      <tr key={index} className="border-b border-gray-700">
                        <td className="py-2 font-medium">{item.symbol}</td>
                        <td className="text-right py-2">{item.weight.toFixed(1)}%</td>
                        <td className="text-right py-2">₹{item.amount.toLocaleString()}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default InvestmentResults;