import { useState } from "react";
import { Form } from "@/components/ui/form";
import { zodResolver } from "@hookform/resolvers/zod";
import { useForm } from "react-hook-form";

import { FormStepHeader } from "@/components/FormStepHeader";
import { FormStepButtons } from "@/components/FormStepButtons";
import { FormFooter } from "@/components/FormFooter";
import { Step1FormFields } from "@/components/Step1FormFields";
import { Step2FormFields } from "@/components/Step2FormFields";

import { formSchema } from "@/config/formSchema";
import type { PortfolioFormValues } from "@/config/formSchema";
import { defaultValues } from "@/config/formDefaults";


export default function PortfolioForm() {
  const [step, setStep] = useState<1 | 2>(1);

  const form = useForm<PortfolioFormValues>({
    resolver: zodResolver(formSchema),
    mode: "onTouched",
    reValidateMode: "onBlur",
    defaultValues,
  });

  const onSubmit = (data: PortfolioFormValues) => {
    console.log(data);
  };

  return (
    <Form {...form}>
      <form
        onSubmit={form.handleSubmit(onSubmit)}
        className="space-y-6 max-w-xl mx-auto"
      >
        <FormStepHeader step={step} setStep={setStep} form={form} />
        <FormStepButtons step={step} setStep={setStep} form={form} />

        {step === 1 && <Step1FormFields form={form} />}
        {step === 2 && <Step2FormFields form={form} />}
        {step === 2 && <FormFooter />}
      </form>
    </Form>
  );
}
