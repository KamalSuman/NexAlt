import React from "react";

const FullScreenLoader: React.FC = () => {
  return (
    <div className="fixed inset-0 bg-black bg-opacity-30 flex items-center justify-center z-50">
      <div className="animate-spin rounded-full h-16 w-16 border-t-4 border-white border-opacity-60"></div>
    </div>
  );
};

export default FullScreenLoader;
