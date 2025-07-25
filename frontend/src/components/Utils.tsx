import type { Preferences } from "./RiskSliderForm";

type basicInfoData = {
  age: string;
  income: string;
  capital: string;
  expenses: string;
  emi: string;
  liquidity: string;
  dependents: string;
  experience: string;
};

type SendInputData = {
  age: number;
  income: number;
  capital: number;
  expenses: number;
  emi: number;
  liquidity_need: number;
  dependents: number;
  experience: number;
  confidence: number;
  knowledge: number;
  comfort_with_negatives: number;
  market_awareness: number;
}

export const submitFormData = async (
  basicInformation: basicInfoData,
  preferences: Preferences
) => {
  try {
    const sendInput: SendInputData = {
      age: Number(basicInformation.age),
      income: Number(basicInformation.income),
      capital: Number(basicInformation.capital),
      expenses: Number(basicInformation.expenses),
      emi: Number(basicInformation.emi),
      liquidity_need: Number(basicInformation.liquidity),
      dependents: Number(basicInformation.dependents),
      experience: Number(basicInformation.experience),
      confidence: preferences.confidence/10,
      knowledge: preferences.knowledge/10,
      comfort_with_negatives: preferences.negatives/10,
      market_awareness: preferences.awareness/10,
    };
    const response = await fetch("http://127.0.0.1:8082/api/investment-profile/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(sendInput),
    });

    if (!response.ok) {
      throw new Error(`Failed to submit form: ${response.statusText}`);
    }

    const data = await response.json();
    console.log("=== API RESPONSE DEBUG ===");
    console.log("Full API Response:", data);
    console.log("Response Keys:", Object.keys(data));
    if (data.allocation) {
      console.log("Allocation:", data.allocation);
    }
    if (data.currency_recommendations) {
      console.log("Currency Recommendations:", data.currency_recommendations);
    }
    console.log("=== END API RESPONSE DEBUG ===");
    return data;
  } catch (error) {
    console.error("Error submitting form:", error);
    throw error;
  }
};
