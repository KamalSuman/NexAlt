import React from "react";

type AssetData = {
  name: string;
  percentage: number;
  amount: number;
  position: { top: string; left: string }; // Position as percentage or px
};

type Props = {
  data: AssetData[];
  imageUrl: string;
};

const AssetAllocation: React.FC<Props> = ({ data, imageUrl }) => {
  return (
    <div className="relative w-full max-w-5xl mx-auto">
      <img src={imageUrl} alt="Asset Allocation" className="w-full" />

      {data.map((asset, index) => (
        <div
          key={index}
          className="absolute text-center transform -translate-x-1/2 -translate-y-full text-xs"
          style={{
            top: asset.position.top,
            left: asset.position.left,
          }}
        >
          <div className="bg-white bg-opacity-80 rounded-md px-2 py-1 shadow text-sm font-semibold text-gray-800">
            {asset.percentage}%<br />₹{asset.amount.toLocaleString()}
          </div>
        </div>
      ))}
    </div>
  );
};

export default AssetAllocation;
