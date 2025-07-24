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

export const submitFormData = async (
  basicInformation: basicInfoData,
  preferences: Preferences
) => {
  try {
    const response = await fetch("http://localhost:8000/api/submit-form/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        basicInformation,
        preferences,
      }),
    });

    if (!response.ok) {
      throw new Error(`Failed to submit form: ${response.statusText}`);
    }

    const data = await response.json();
    console.log("Submission successful:", data);
    return data;
  } catch (error) {
    console.error("Error submitting form:", error);
    throw error;
  }
};
