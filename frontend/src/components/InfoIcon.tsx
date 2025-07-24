import {
  Tooltip,
  TooltipContent,
  TooltipTrigger,
} from "@/components/ui/tooltip";
import { Info } from "lucide-react";


export const InfoIcon = ({ text }: { text: string }) => (
  <Tooltip>
    <TooltipTrigger asChild>
      <Info className="w-4 h-4 ml-2 text-muted-foreground cursor-pointer" />
    </TooltipTrigger>
    <TooltipContent className="max-w-xs text-sm text-primary-foreground">
      {text}
    </TooltipContent>
  </Tooltip>
);