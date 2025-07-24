import { useForm } from "@tanstack/react-form";
import { z } from 'zod'
import { formFields, formSchema } from "@/config/questions";
import { Input } from "@/components/ui/input";
import {
  Select,
  SelectTrigger,
  SelectValue,
  SelectContent,
  SelectItem,
} from "@/components/ui/select";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";

type FormData = z.infer<typeof formSchema>

const defaultValues: FormData = {
  age: 0,
  income: 0,
  capital: 0,
  goal: "Other"
}

const PsychometricForm = () => {
  const form = useForm({
    defaultValues,
    onSubmit: async ({ value }) => {
      console.log("Form Submitted:", value);
    }
  });

  return (
    <form
      onSubmit={(e) => {
        e.preventDefault();
        form.handleSubmit();
      }}
      className="max-w-xl mx-auto space-y-6 p-6"
    >
      {(Object.entries(formFields) as [keyof FormData, typeof formFields[keyof FormData]][]).map(([key, config]) => (
        <Card key={key}>
          <CardContent className="p-4 space-y-2">
            <label className="text-sm font-medium">{config.label}</label>
            {config.type === "number" && (
              <form.Field
                name={key}
                children={(field) => (
                  <Input
                    type="number"
                    value={field.state.value}
                    onChange={(e) => field.handleChange(e.target.value)}
                    placeholder={config.placeholder}
                  />
                )}
              />
            )}
            {config.type === "select" && (
              <form.Field
                name={key}
                children={(field) => (
                  <Select
                    defaultValue={String(field.state.value)}
                    onValueChange={field.handleChange}
                  >
                    <SelectTrigger>
                      <SelectValue placeholder={config.placeholder} />
                    </SelectTrigger>
                    <SelectContent>
                      {config.options?.map((opt) => (
                        <SelectItem key={opt} value={opt}>
                          {opt}
                        </SelectItem>
                      ))}
                    </SelectContent>
                  </Select>
                )}
              />
            )}
          </CardContent>
        </Card>
      ))}
      <Button type="submit" className="w-full">
        Submit
      </Button>
    </form>
  );
};

export default PsychometricForm;
