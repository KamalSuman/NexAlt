export const sliderMarks = [
  { value: 0, label: "Low" },
  { value: 0.5, label: "Medium" },
  { value: 1, label: "High" },
];

export const steps = [
  { label: "Basic Info" },
  { label: "Preferences" },
];

export const step1Fields = [
  "age",
  "income",
  "capital",
  "expenses",
  "emi",
  "liquidity_need",
  "dependents",
  "experience",
] as const;

export const step2Fields = [
  "confidence",
  "knowledge",
  "comfort_with_negatives",
  "market_awareness",
] as const;

export const sliderTooltips = {
  confidence: "How confident you are in making investment decisions.",
  knowledge: "Your knowledge of financial and investment concepts.",
  comfort_with_negatives: "How comfortable you are seeing negative returns in the short term.",
  market_awareness: "How aware you are of current market events and trends.",
} as const;

export const inputFields = [
  {
    name: "age",
    label: "Age",
    info: "Your current age in years.",
    type: "number",
  },
  {
    name: "income",
    label: "Annual Income",
    info: "Your total yearly income.",
    type: "number",
  },
  {
    name: "capital",
    label: "Investable Capital",
    info: "Funds available for investment.",
    type: "number",
  },
  {
    name: "expenses",
    label: "Annual Expenses",
    info: "Your yearly necessary expenditures.",
    type: "number",
  },
  {
    name: "emi",
    label: "Annual EMI",
    info: "Total yearly EMI payment obligations.",
    type: "number",
  },
  {
    name: "liquidity_need",
    label: "Liquidity Need (%)",
    info: "Percentage of capital you might need for emergencies.",
    type: "number",
  },
  {
    name: "dependents",
    label: "Dependents",
    info: "Number of financial dependents.",
    type: "number",
  },
  {
    name: "experience",
    label: "Investment Experience (Years)",
    info: "Years of experience with investing.",
    type: "number",
  },
] as const;