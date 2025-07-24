import { Input } from "@/components/ui/input";
import {
  FormControl,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from "@/components/ui/form";
import { InfoIcon } from "@/components/InfoIcon";
import { step1Fields, inputFields } from "@/config/formFields";
import type { UseFormReturn } from "react-hook-form";
import type { PortfolioFormValues } from "@/config/formSchema";

interface Props {
  form: UseFormReturn<PortfolioFormValues>;
}

export const Step1FormFields = ({ form }: Props) => {
  const {
    formState: { errors },
  } = form;

  return (
    <>
      {inputFields
        .filter(({ name }) => step1Fields.includes(name))
        .map(({ name, label, info, type }) => (
          <FormField
            key={name}
            control={form.control}
            name={name}
            render={({ field }) => (
              <FormItem>
                <FormLabel className="flex items-center">
                  {label}
                  <InfoIcon text={info} />
                </FormLabel>
                <FormControl>
                  <Input
                    type={type}
                    {...field}
                    onChange={(e) => {
                      const value = e.target.value;
                      field.onChange(value === "" ? "" : Number(value));
                    }}
                  />
                </FormControl>
                {errors[name] && <FormMessage />}
              </FormItem>
            )}
          />
        ))}
    </>
  );
};
