import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { useForm } from "@tanstack/react-form";
import { formSchema } from "@/config/questions";
import { z } from "zod";

type FormData = z.infer<typeof formSchema>;
const form = useForm<FormData, undefined, undefined, undefined, undefined, undefined, undefined, undefined, undefined, unknown>({
  defaultValues: {
    age: 0,
    income: 0,
    capital: 0,
    goal: "Other",
  },
  onSubmit: async ({ value }) => {
    console.log("Form Submitted:", value);
  },
});

type FormInstance = typeof form;

type NumberFieldProps = {
  name: keyof FormData;
  config: {
    label: string;
    placeholder: string;
    type: "number";
  };
  form: FormInstance;
};

export const NumberField = ({ name, config, form }: NumberFieldProps) => {
  return (
    <>
      <Label className="text-sm font-medium">{config.label}</Label>
      <form.Field
        name={name}
        validators={{
          onChange: async ({ value }) => {
            const parsed = formSchema.shape[name].safeParse(Number(value));
            return parsed.success ? undefined : parsed.error.message;
          },
        }}
      >
        {(field) => (
            <>
                <Input
                type="number"
                value={field.state.value}
                onChange={(e) => field.handleChange(Number(e.target.value))}
                placeholder={config.placeholder}
                />
                {field.state.meta.errors?.[0] && field.state.meta.isTouched && (
                <p className="text-sm text-red-500">
                    {field.state.meta.errors[0]}
                </p>
                )}
            </>
        )}

      </form.Field>
    </>
  );
};
