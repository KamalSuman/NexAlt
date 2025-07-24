import { z } from "zod";

export const formSchema = z.object({
  age: z.number().min(18, "Age must be at least 18"),
  income: z.number().min(0, "Income must be non-negative"),
  capital: z.number().min(0, "Capital must be non-negative"),
  goal: z.enum(["retirement", "growth", "income", "other"]),
});

export const formFields = {
  age: {
    label: "Age",
    placeholder: "Enter your age",
    type: "number" as const,
  },
  income: {
    label: "Income",
    placeholder: "Enter your income",
    type: "number" as const,
  },
  capital: {
    label: "Capital",
    placeholder: "Enter your capital",
    type: "number" as const,
  },
  goal: {
    label: "Goal",
    placeholder: "Select a goal",
    type: "select" as const,
    options: ["retirement", "growth", "income", "other"],
  },
};
