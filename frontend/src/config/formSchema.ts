import { z } from "zod";

export const formSchema = z.object({
  age: z
    .number()
    .min(18, { message: "Age must be at least 18" })
    .max(100, { message: "Age must be at most 100" }),

  income: z
    .number()
    .nonnegative({ message: "Income cannot be negative" }),

  capital: z
    .number()
    .nonnegative({ message: "Capital cannot be negative" }),

  expenses: z
    .number()
    .nonnegative({ message: "Expenses cannot be negative" }),

  emi: z
    .number()
    .nonnegative({ message: "EMI cannot be negative" }),

  liquidity_need: z
    .number()
    .min(0, { message: "Liquidity need must be at least 0" })
    .max(100, { message: "Liquidity need must be at most 100" }),

  dependents: z
    .number()
    .min(0, { message: "Must be at least 0 dependents" })
    .max(10, { message: "Cannot have more than 10 dependents" }),

  confidence: z
    .number()
    .min(0)
    .max(1),

  knowledge: z
    .number()
    .min(0)
    .max(1),

  comfort_with_negatives: z
    .number()
    .min(0)
    .max(1),

  market_awareness: z
    .number()
    .min(0)
    .max(1),

  experience: z
    .number()
    .min(0, { message: "Experience must be at least 0" })
    .max(40, { message: "Experience cannot exceed 40 years" }),
});

export type PortfolioFormValues = z.infer<typeof formSchema>
