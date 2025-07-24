import React from "react";
import { steps, step1Fields } from "@/config/formFields";
import type { UseFormReturn } from "react-hook-form";
import type { PortfolioFormValues } from "@/config/formSchema";

interface FormStepHeaderProps {
  step: number;
  setStep: (s: 1 | 2) => void;
  form: UseFormReturn<PortfolioFormValues>;
}

export const FormStepHeader: React.FC<FormStepHeaderProps> = ({
  step,
  setStep,
  form,
}) => {
  const handleClick = async (targetStep: 1 | 2) => {
    if (targetStep === step) return;

    if (targetStep === 1) {
      setStep(1);
    } else {
      const valid = await form.trigger(step1Fields);
      if (valid) {
        setStep(2);
      }
    }
  };

  return (
    <div className="mb-6">
      <p className="text-sm text-muted-foreground mb-3 text-center">
        Step {step} of {steps.length}
      </p>
      <div className="flex justify-around items-center">
        {steps.map((s, idx) => {
          const index = (idx + 1) as 1 | 2;
          const isActive = step === index;

          return (
            <button
              key={idx}
              type="button"
              onClick={() => handleClick(index)}
              className="flex flex-col items-center gap-1 focus:outline-none cursor-pointer group"
            >
              <div
                className={`w-4 h-4 rounded-full transition-all duration-300 ${
                  isActive ? "bg-primary" : "bg-muted group-hover:bg-primary/60"
                }`}
              />
              <span
                className={`text-sm transition-all duration-300 ${
                  isActive
                    ? "text-primary font-semibold"
                    : "text-muted-foreground group-hover:text-primary"
                }`}
              >
                {s.label}
              </span>
            </button>
          );
        })}
      </div>
    </div>
  );
};
