import {
  FormControl,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from "@/components/ui/form";
import { Slider } from "@/components/ui/slider";
import { InfoIcon } from "@/components/InfoIcon";
import { step2Fields, sliderMarks, sliderTooltips } from "@/config/formFields";
import type { UseFormReturn } from "react-hook-form";
import type { PortfolioFormValues } from "@/config/formSchema";

interface Props {
  form: UseFormReturn<PortfolioFormValues>;
}

export const Step2FormFields = ({ form }: Props) => {
  const {
    formState: { errors },
  } = form;

  return (
    <>
      {step2Fields.map((key) => (
        <FormField
          key={key}
          control={form.control}
          name={key}
          render={({ field }) => (
            <FormItem>
              <FormLabel className="flex items-center capitalize">
                {key.replaceAll("_", " ")}
                <InfoIcon text={sliderTooltips[key]} />
              </FormLabel>
              <FormControl>
                <Slider
                  value={[field.value ?? 0]}
                  step={0.1}
                  min={0}
                  max={1}
                  onValueChange={(val) => field.onChange(val[0])}
                />
              </FormControl>
              <div className="flex justify-between text-sm text-muted-foreground">
                {sliderMarks.map((mark) => (
                  <span key={mark.value}>{mark.label}</span>
                ))}
              </div>
              {errors[key] && <FormMessage />}
            </FormItem>
          )}
        />
      ))}
    </>
  );
};
