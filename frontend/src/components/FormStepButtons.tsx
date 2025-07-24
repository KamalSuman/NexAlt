import { Button } from "@/components/ui/button";
import { step1Fields } from "@/config/formFields";
import type { UseFormReturn } from "react-hook-form";
import type { PortfolioFormValues } from "@/config/formSchema";
import type { Dispatch, SetStateAction } from "react";
import { ArrowLeft, ArrowRight } from "lucide-react";

interface FormStepButtonsProps {
  step: 1 | 2;
  setStep: Dispatch<SetStateAction<1 | 2>>;
  form: UseFormReturn<PortfolioFormValues>;
}

export const FormStepButtons: React.FC<FormStepButtonsProps> = ({
  step,
  setStep,
  form,
}) => {
  return (
    <div className="flex justify-between items-center mt-8">
      {step === 2 && (
        <Button
          type="button"
          variant="secondary"
          onClick={() => setStep(1)}
          className="cursor-pointer hover:bg-secondary/80"
        >
          <ArrowLeft className="mr-2 h-4 w-4" />
          Back
        </Button>
      )}
      {step === 1 && (
        <div className="ml-auto">
          <Button
            type="button"
            variant="secondary"
            onClick={async () => {
              const valid = await form.trigger(step1Fields);
              if (valid) setStep(2);
            }}
            className="cursor-pointer hover:bg-secondary/80"
          >
            Next
            <ArrowRight className="ml-2 h-4 w-4" />
          </Button>
        </div>
      )}
    </div>
  );
};