import { DollarSign, BanknoteArrowDown } from "lucide-react";

import RightArrow from "@/assets/right-arrow.png";
import AgeIcon from "@/assets/age.png";
import AnnualIncomeIcon from "@/assets/money-bag.png";
import RiskSliderForm from "./RiskSliderForm";
import { useState } from "react";
import { submitFormData } from "./Utils";

const FullForm = () => {
  const [formType, setFormType] = useState(0);

  const [basicInfo, setBasicInfo] = useState({
    age: "",
    income: "",
    capital: "",
    expenses: "",
    emi: "",
    liquidity: "",
    dependents: "",
    experience: "",
  });

  const [preferences, setPreferences] = useState({
    confidence: 1,
    knowledge: 1,
    negatives: 1,
    awareness: 1,
  });

  const isBasicInfoValid = Object.values(basicInfo).every((val) => val !== "");

  const handleSubmit = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();

    if (formType === 0) {
      if (!isBasicInfoValid) {
        alert("Please fill all Basic Information fields.");
        return;
      }
      setFormType(1);
    } else {
      console.log("Basic Info:", basicInfo);
      console.log("Preferences:", preferences);

      submitFormData(basicInfo, preferences);
      alert("Form submitted!");
    }
  };

  const handleInputChange = (field: keyof typeof basicInfo, value: string) => {
    setBasicInfo({ ...basicInfo, [field]: value });
  };

  return (
    <div className="max-w-2xl mx-auto bg-[#111827] text-white p-8 rounded-xl shadow-lg space-y-6">
      {/* Step Indicator */}
      <div className="flex justify-between items-center">
        <div className="text-sm font-semibold text-white flex items-center gap-2">
          <div className="w-6 h-6 rounded-full bg-indigo-600 flex items-center justify-center text-xs">
            {formType + 1}
          </div>
          <span>{!formType ? "Basic Information" : "Preferences"}</span>
        </div>
        <div className="flex gap-4 text-gray-400 text-sm">
          <span
            className="w-60 rounded-md border border-gray-500 text-center flex gap-1 justify-center items-center hover:scale-110 transition-all duration-200 cursor-pointer"
            onClick={(e) => {
              e.preventDefault();
              setFormType((prev) => 1 - prev);
            }}
          >
            {formType == 0 ? (
              <>
                Move to <span className="font-bold">Preferences</span>
                <img src={RightArrow} width={40} height={5} className="mt-1" />
              </>
            ) : (
              <>
                Back to <span className="font-bold">Basic Information</span>
                <img
                  src={RightArrow}
                  width={40}
                  height={5}
                  className="mt-1 rotate-180"
                />
              </>
            )}
          </span>
        </div>
      </div>

      {/* Header */}
      <div>
        <h1 className="text-3xl font-bold mt-1 mb-2">Psychometric Profile</h1>
        <p className="text-gray-400 text-sm">
          Please enter all the basic details required for lorem ipsum
        </p>
      </div>

      {/* Form */}
      <form className="space-y-4" onSubmit={handleSubmit}>
        {formType === 0 ? (
          <>
            {/* Age */}
            <div className="relative space-y-1">
              <label className="block text-sm text-gray-300 ml-2">Age</label>
              <div className="relative">
                <img
                  src={AgeIcon}
                  width={22}
                  height={22}
                  className="absolute left-3 top-4 text-gray-400"
                />
                <input
                  type="number"
                  placeholder="Enter your age"
                  value={basicInfo.age}
                  onChange={(e) => handleInputChange("age", e.target.value)}
                  className="pl-10 bg-[#1f2937] p-3 rounded-md outline-none text-sm w-full mt-1"
                />
              </div>
            </div>

            {/* Annual Income */}
            <div className="relative space-y-1">
              <label className="block text-sm text-gray-300 ml-2">Income</label>
              <div className="relative">
                <img
                  src={AnnualIncomeIcon}
                  width={22}
                  height={22}
                  className="absolute left-3 top-4 text-gray-400"
                />
                <input
                  type="number"
                  placeholder="Enter your income"
                  value={basicInfo.income}
                  onChange={(e) => handleInputChange("income", e.target.value)}
                  className="pl-10 bg-[#1f2937] p-3 rounded-md outline-none text-sm w-full mt-1"
                />
              </div>
            </div>

            {/* Investable Capital */}
            <div className="relative space-y-1">
              <label className="block text-sm text-gray-300 ml-2">
                Investable Capital
              </label>
              <div className="relative">
                <DollarSign
                  className="absolute left-3 top-4 text-gray-400"
                  size={18}
                />
                <input
                  type="number"
                  placeholder="Enter investable capital"
                  value={basicInfo.capital}
                  onChange={(e) => handleInputChange("capital", e.target.value)}
                  className="pl-10 bg-[#1f2937] p-3 rounded-md outline-none text-sm w-full mt-1"
                />
              </div>
            </div>

            {/* Annual Expenses */}
            <div className="relative space-y-1">
              <label className="block text-sm text-gray-300 ml-2">
                Annual Expenses
              </label>
              <div className="relative">
                <BanknoteArrowDown
                  className="absolute left-3 top-4 text-gray-400"
                  size={18}
                />
                <input
                  type="number"
                  placeholder="Enter your annual expenses"
                  value={basicInfo.expenses}
                  onChange={(e) =>
                    handleInputChange("expenses", e.target.value)
                  }
                  className="pl-10 bg-[#1f2937] p-3 rounded-md outline-none text-sm w-full mt-1"
                />
              </div>
            </div>

            {/* Annual EMI */}
            <div className="relative space-y-1">
              <label className="block text-sm text-gray-300 ml-2">
                Annual EMI
              </label>
              <div className="relative">
                <BanknoteArrowDown
                  className="absolute left-3 top-4 text-gray-400"
                  size={18}
                />
                <input
                  type="number"
                  placeholder="Enter EMI amount"
                  value={basicInfo.emi}
                  onChange={(e) => handleInputChange("emi", e.target.value)}
                  className="pl-10 bg-[#1f2937] p-3 rounded-md outline-none text-sm w-full mt-1"
                />
              </div>
            </div>

            {/* Liquidity Need */}
            <div className="relative space-y-1">
              <label className="block text-sm text-gray-300 ml-2">
                Liquidity Need
              </label>
              <div className="relative">
                <BanknoteArrowDown
                  className="absolute left-3 top-3 text-gray-400"
                  size={18}
                />
                <input
                  type="number"
                  placeholder="Enter liquidity need"
                  value={basicInfo.liquidity}
                  onChange={(e) =>
                    handleInputChange("liquidity", e.target.value)
                  }
                  className="pl-10 bg-[#1f2937] p-3 rounded-md outline-none text-sm w-full mt-1"
                />
              </div>
            </div>

            {/* Dependents */}
            <div className="relative space-y-1">
              <label className="block text-sm text-gray-300 ml-2">
                Dependents
              </label>
              <div className="relative">
                <BanknoteArrowDown
                  className="absolute left-3 top-4 text-gray-400"
                  size={18}
                />
                <input
                  type="number"
                  placeholder="Enter number of dependents"
                  value={basicInfo.dependents}
                  onChange={(e) =>
                    handleInputChange("dependents", e.target.value)
                  }
                  className="pl-10 bg-[#1f2937] p-3 rounded-md outline-none text-sm w-full mt-1"
                />
              </div>
            </div>

            {/* Investment Experience */}
            <div className="relative space-y-1">
              <label className="block text-sm text-gray-300 ml-2">
                Investment Experience (Years)
              </label>
              <div className="relative">
                <BanknoteArrowDown
                  className="absolute left-3 top-4 text-gray-400"
                  size={18}
                />
                <input
                  type="number"
                  placeholder="Enter number of years"
                  value={basicInfo.experience}
                  onChange={(e) =>
                    handleInputChange("experience", e.target.value)
                  }
                  className="pl-10 bg-[#1f2937] p-3 rounded-md outline-none text-sm w-full mt-1"
                />
              </div>
            </div>
          </>
        ) : (
          <RiskSliderForm
            preferences={preferences}
            setPreferences={setPreferences}
          />
        )}

        <button
          type="submit"
          className="w-full bg-indigo-500 hover:bg-indigo-600 transition text-white py-2 px-4 rounded-md font-semibold cursor-pointer hover:scale-105 duration-200"
        >
          {formType === 1 ? "Submit" : "Next"}
        </button>
      </form>

      {/* <form className="space-y-4">
        {formType == 0 ? (
          <>
            <div className="relative">
              <img
                src={AgeIcon}
                width={22}
                height={22}
                className="absolute left-3 top-3 text-gray-400"
              />
              <input
                type="number"
                placeholder="Age"
                className="pl-10 bg-[#1f2937] p-3 rounded-md outline-none text-sm w-full"
              />
            </div>
            <div className="relative">
              <img
                src={AnnualIncomeIcon}
                width={22}
                height={22}
                className="absolute left-3 top-3 text-gray-400"
              />
              <input
                type="number"
                placeholder="Annual Income"
                className="pl-10 bg-[#1f2937] p-3 rounded-md outline-none text-sm w-full"
              />
            </div>
            <div className="relative">
              <DollarSign
                className="absolute left-3 top-3 text-gray-400"
                size={18}
              />
              <input
                type="number"
                placeholder="Investable Capital"
                className="pl-10 bg-[#1f2937] p-3 rounded-md outline-none text-sm w-full"
              />
            </div>
            <div className="relative">
              <BanknoteArrowDown
                className="absolute left-3 top-3 text-gray-400"
                size={18}
              />
              <input
                type="number"
                placeholder="Annual Expenses"
                className="pl-11 bg-[#1f2937] p-3 rounded-md outline-none text-sm w-full"
              />
            </div>
            <div className="relative">
              <BanknoteArrowDown
                className="absolute left-3 top-3 text-gray-400"
                size={18}
              />
              <input
                type="number"
                placeholder="Annual EMI"
                className="pl-11 bg-[#1f2937] p-3 rounded-md outline-none text-sm w-full"
              />
            </div>
            <div className="relative">
              <BanknoteArrowDown
                className="absolute left-3 top-3 text-gray-400"
                size={18}
              />
              <input
                type="number"
                placeholder="Liquidity Need"
                className="pl-11 bg-[#1f2937] p-3 rounded-md outline-none text-sm w-full"
              />
            </div>
            <div className="relative">
              <BanknoteArrowDown
                className="absolute left-3 top-3 text-gray-400"
                size={18}
              />
              <input
                type="number"
                placeholder="Dependents"
                className="pl-11 bg-[#1f2937] p-3 rounded-md outline-none text-sm w-full"
              />
            </div>
            <div className="relative">
              <BanknoteArrowDown
                className="absolute left-3 top-3 text-gray-400"
                size={18}
              />
              <input
                type="number"
                placeholder="Investment Experiences (Years)"
                className="pl-11 bg-[#1f2937] p-3 rounded-md outline-none text-sm w-full"
              />
            </div>
          </>
        ) : (
          <RiskSliderForm />
        )}

        <button
          className="w-full bg-indigo-500 hover:bg-indigo-600 transition text-white py-2 px-4 rounded-md font-semibold cursor-pointer hover:scale-105 duration-200"
          onClick={(e) => {
            e.preventDefault();
            setFormType((prev) => 1 - prev);
          }}
        >
          {formType == 1 ? "Next" : "Submit"}
        </button>
      </form> */}
    </div>
  );
};

export default FullForm;
