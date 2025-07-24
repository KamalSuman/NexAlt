// src/config/questions.ts
import { z } from "zod";

export const formFields = {
  age: {
    label: "Age",
    type: "number",
    placeholder: "Enter your age",
  },
  income: {
    label: "Annual Income",
    type: "number",
    placeholder: "Enter your annual income",
  },
  capital: {
    label: "Available Capital",
    type: "number",
    placeholder: "Enter your available capital",
  },
  goal: {
    label: "Investment Goal",
    type: "select",
    options: ["Retirement", "Growth", "Income", "Other"],
    placeholder: "Select your investment goal",
  },
} as const;

export const formSchema = z.object({
  age: z.coerce.number().min(18, "Must be at least 18"),
  income: z.coerce.number().min(0, "Income must be positive"),
  capital: z.coerce.number().min(0, "Capital must be positive"),
  goal: z.string().min(1, "Goal is required"),
});