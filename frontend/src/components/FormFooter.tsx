import { Button } from "@/components/ui/button";

export const FormFooter: React.FC = () => {
  return (
    <div className="mt-10 flex justify-center">
      <Button type="submit" className="px-8">
        Submit
      </Button>
    </div>
  );
};