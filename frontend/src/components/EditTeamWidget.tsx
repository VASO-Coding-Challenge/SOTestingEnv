import { useState, useEffect } from "react";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog";
import { Separator } from "@/components/ui/separator";
import { Badge } from "@/components/ui/badge";
import { RadioGroup, RadioGroupItem } from "@/components/ui/radio-group";
import { Button } from "@/components/ui/button";
import { PencilLine } from "lucide-react";

const EditTeamWidget = ({ team, onSave }) => {
  const [open, setOpen] = useState(false);

  return (
    <Dialog open={open} onOpenChange={setOpen}>
      <DialogTrigger>
        <Button size="icon" variant="ghost">
          <PencilLine className="w-4 h-4" />
        </Button>
      </DialogTrigger>

      <DialogContent></DialogContent>
    </Dialog>
  );
};

export default EditTeamWidget;
