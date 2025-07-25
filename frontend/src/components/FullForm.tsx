import { DollarSign, BanknoteArrowDown, Loader } from "lucide-react";

import RightArrow from "@/assets/right-arrow.png";
import AgeIcon from "@/assets/age.png";
import AnnualIncomeIcon from "@/assets/money-bag.png";
import LoginImgVector from "@/assets/login-im.svg";
import RiskSliderForm from "./RiskSliderForm";
import { useEffect, useState } from "react";
import { submitFormData } from "./Utils";
import { Link } from "react-router-dom";
import { CircularProgress } from "@mui/material";
import { useNavigate } from "react-router-dom";

const FullForm = () => {
  const [showLogin, setShowLogin] = useState(false);

  const toggleLogin = () => setShowLogin(!showLogin);
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
    confidence: 5,
    knowledge: 5,
    negatives: 5,
    awareness: 5,
  });

  const isBasicInfoValid = Object.values(basicInfo).every((val) => val !== "");
  const allValid = Object.values(basicInfo).every(
    (value) =>
      typeof value !== "string" ||
      (typeof value === "string" && !value.includes("-"))
  );
  const navigate = useNavigate();
  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();

    if (formType === 0) {
      if (!isBasicInfoValid && !allValid) {
        alert("Please fill all Basic Information fields.");
        return;
      }
      setFormType(1);
    } else {
      setSubmitting(true);
      try {
        const result = await submitFormData(basicInfo, preferences);
        localStorage.setItem('investmentResult', JSON.stringify(result));
        navigate("/chatbot/output-response");
      } catch (error) {
        alert("Failed to submit form. Please try again.");
      } finally {
        setSubmitting(false);
      }
    }
  };

  const handleInputChange = (field: keyof typeof basicInfo, value: string) => {
    setBasicInfo({ ...basicInfo, [field]: value });
  };
  const [submitting, setSubmitting] = useState(false);

  return (
    <div>
      <header className="bg-white shadow p-3 mb-3 flex justify-between items-center">
        <Link to={"/"}>
          <h1 className="text-3xl font-bold text-black cursor-pointer">
            nexAlt.ai
          </h1>
        </Link>
        {/* <img src={Logo} alt="Logo" className="h-6" /> */}
        <nav>
          <ul className="flex gap-6 text-sm font-medium items-center">
            <li>
              <a href="#features" className="hover:text-blue-600">
                Features
              </a>
            </li>
            <li>
              <a href="#about" className="hover:text-blue-600">
                About
              </a>
            </li>
            <li>
              <a href="#contact" className="hover:text-blue-600">
                Contact
              </a>
            </li>
            <li>
              <button
                onClick={toggleLogin}
                className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700 transition"
              >
                Login
              </button>
            </li>
          </ul>
        </nav>
      </header>
      {submitting && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-[#2a2828] bg-opacity-50">
          <CircularProgress color="secondary" />
        </div>
      )}
      <>
          {showLogin && (
            <div className="fixed inset-0 bg-black bg-opacity-50 flex justify-center items-center z-50">
              <div className="bg-white rounded-lg overflow-hidden w-full max-w-4xl flex">
                <div className="w-1/2 bg-white hidden md:flex items-center justify-center p-6">
                  <img
                    src={LoginImgVector}
                    alt="Login Illustration"
                    className="scale-125 ml-3"
                  />
                </div>
                <div className="w-full md:w-1/2 p-8">
                  <h2 className="text-3xl font-bold mb-2 text-gray-800">
                    Welcome to NextAlt.ai! 👋🏻
                  </h2>
                  <p className="mb-6 text-gray-500">
                    Please sign in to your account and start the adventure
                  </p>
                  <form>
                    <div className="mb-4">
                      <label className="block mb-1 text-sm text-gray-600">
                        Email
                      </label>
                      <input
                        type="email"
                        className="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                        placeholder="Enter your email"
                      />
                    </div>
                    <div className="mb-4">
                      <label className="block mb-1 text-sm text-gray-600">
                        Password
                      </label>
                      <input
                        type="password"
                        className="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                        placeholder="Enter your password"
                      />
                      <div className="text-right mt-1">
                        <a
                          href="#"
                          className="text-sm text-blue-500 hover:underline"
                        >
                          Forgot Password?
                        </a>
                      </div>
                    </div>
                    <div className="mb-4 flex items-center">
                      <input type="checkbox" id="remember" className="mr-2" />
                      <label
                        htmlFor="remember"
                        className="text-sm text-gray-600"
                      >
                        Remember Me
                      </label>
                    </div>
                    <Link to={"/chatbot/"}>
                      <button
                        type="submit"
                        className="w-full bg-blue-600 hover:bg-blue-700 text-white font-semibold py-2 rounded-lg"
                      >
                        Sign In
                      </button>
                    </Link>
                  </form>
                  <p className="mt-6 text-center text-sm text-gray-600">
                    New on our platform?{" "}
                    <a href="#" className="text-blue-500 hover:underline">
                      Create an account
                    </a>
                  </p>
                  <div className="mt-6 flex justify-center space-x-4 text-lg">
                    <a href="#" className="text-blue-700 hover:text-blue-900">
                      <i className="fab fa-facebook-f"></i>
                    </a>
                    <a href="#" className="text-blue-400 hover:text-blue-600">
                      <i className="fab fa-twitter"></i>
                    </a>
                    <a href="#" className="text-black hover:text-gray-700">
                      <i className="fab fa-github"></i>
                    </a>
                    <a href="#" className="text-red-600 hover:text-red-800">
                      <i className="fab fa-google"></i>
                    </a>
                  </div>
                  <button
                    onClick={toggleLogin}
                    className="mt-4 text-sm text-gray-500 hover:underline block mx-auto"
                  >
                    Close
                  </button>
                </div>
              </div>
            </div>
          )}
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
                      <img
                        src={RightArrow}
                        width={40}
                        height={5}
                        className="mt-1"
                      />
                    </>
                  ) : (
                    <>
                      Back to{" "}
                      <span className="font-bold">Basic Information</span>
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
              <h1 className="text-3xl font-bold mt-1 mb-2">
                Psychometric Profile
              </h1>
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
                    <label className="block text-sm text-gray-300 ml-2">
                      Age
                    </label>
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
                        onChange={(e) =>
                          handleInputChange("age", e.target.value)
                        }
                        className="pl-10 bg-[#1f2937] p-3 rounded-md outline-none text-sm w-full mt-1"
                      />
                    </div>
                  </div>

                  {/* Annual Income */}
                  <div className="relative space-y-1">
                    <label className="block text-sm text-gray-300 ml-2">
                      Income
                    </label>
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
                        onChange={(e) =>
                          handleInputChange("income", e.target.value)
                        }
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
                        onChange={(e) =>
                          handleInputChange("capital", e.target.value)
                        }
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
                        onChange={(e) =>
                          handleInputChange("emi", e.target.value)
                        }
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
      </>
    </div>
  );
};

export default FullForm;
