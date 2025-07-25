import { Info } from "lucide-react";

export type Preferences = {
  confidence: number;
  knowledge: number;
  negatives: number;
  awareness: number;
};

type SliderInputProps = {
  label: string;
  id: keyof Preferences; // Ensures 'id' matches keys like 'confidence', 'knowledge', etc.
  value: number;
  onChange: (id: keyof Preferences, value: number) => void;
};

type RiskSliderFormProps = {
  preferences: Preferences;
  setPreferences: React.Dispatch<React.SetStateAction<Preferences>>;
  liquidity: number;
  onLiquidityChange: (value: number) => void;
};

const SliderInput = ({ label, id, value, onChange }: SliderInputProps) => {
  return (
    <div className="bg-[#1f2937] p-4 rounded-xl space-y-2 w-full">
      <div className="flex items-center justify-between">
        <label htmlFor={id} className="text-white font-medium text-sm">
          {label}
        </label>
        <Info className="text-gray-400 w-4 h-4 cursor-pointer" />
      </div>
      <input
        type="range"
        id={id}
        min={1}
        max={10}
        step={1}
        value={value}
        onChange={(e) => onChange(id, parseInt(e.target.value))}
        className="w-full appearance-none h-2 bg-gray-700 rounded-lg outline-none accent-indigo-500"
      />
      <div className="flex justify-between text-xs text-gray-400 px-1">
        <span>1</span>
        <span>2</span>
        <span>3</span>
        <span>4</span>
        <span>5</span>
        <span>6</span>
        <span>7</span>
        <span>8</span>
        <span>9</span>
        <span>10</span>
      </div>
    </div>
  );
};

const RiskSliderForm = ({
  preferences,
  setPreferences,
  liquidity,
  onLiquidityChange,
}: RiskSliderFormProps) => {
  const handleSliderChange = (id: keyof Preferences, value: number) => {
    setPreferences((prev) => ({ ...prev, [id]: value }));
  };

  return (
    <div className="max-w-xl mx-auto space-y-4 text-white">
      <SliderInput
        label="Confidence"
        id="confidence"
        value={preferences.confidence}
        onChange={handleSliderChange}
      />
      <SliderInput
        label="Knowledge"
        id="knowledge"
        value={preferences.knowledge}
        onChange={handleSliderChange}
      />
      <SliderInput
        label="Comfort With Negatives"
        id="negatives"
        value={preferences.negatives}
        onChange={handleSliderChange}
      />
      <SliderInput
        label="Market Awareness"
        id="awareness"
        value={preferences.awareness}
        onChange={handleSliderChange}
      />
      
      {/* Liquidity Need */}
      <div className="bg-[#1f2937] p-4 rounded-xl space-y-2 w-full">
        <div className="flex items-center justify-between">
          <label className="text-white font-medium text-sm">
            Liquidity Need
          </label>
          <Info className="text-gray-400 w-4 h-4 cursor-pointer" />
        </div>
        <input
          type="range"
          min={1}
          max={10}
          step={1}
          value={liquidity}
          onChange={(e) => onLiquidityChange(parseInt(e.target.value))}
          className="w-full appearance-none h-2 bg-gray-700 rounded-lg outline-none accent-indigo-500"
        />
        <div className="flex justify-between text-xs text-gray-400 px-1">
          <span>1</span>
          <span>2</span>
          <span>3</span>
          <span>4</span>
          <span>5</span>
          <span>6</span>
          <span>7</span>
          <span>8</span>
          <span>9</span>
          <span>10</span>
        </div>
      </div>
    </div>
  );
};

export default RiskSliderForm;
