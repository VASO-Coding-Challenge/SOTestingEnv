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
import { Label } from "@/components/ui/label";
import { Separator } from "@/components/ui/separator";
import { Badge } from "@/components/ui/badge";
import CounterInput from "@/components/ui/counter-input";
import { RadioGroup, RadioGroupItem } from "@/components/ui/radio-group";
import { Button } from "@/components/ui/button";
import { Plus } from "lucide-react";

interface Team {
  id: string;
  name: string;
  division: "B" | "C";
}

interface CreateTeamWidgetProps {
  teams: Team[];
  onCreate: () => void;
}

const CreateTeamWidget = ({ teams = [], onCreate }: CreateTeamWidgetProps) => {
  const [open, setOpen] = useState(false);
  const [division, setDivision] = useState<"B" | "C">("B");
  const [rangeStart, setRangeStart] = useState<number>(1);
  const [rangeEnd, setRangeEnd] = useState<number>(1);
  const [teamNames, setTeamNames] = useState<string[]>([]);

  useEffect(() => {
    if (!open) {
      setDivision("B");
      setRangeStart(1);
      setRangeEnd(1);
      setTeamNames([]);
    }
    if (rangeStart > rangeEnd) {
      setTeamNames([]);
    }
    const names = Array.from(
      { length: rangeEnd - rangeStart + 1 },
      (_, i) => `${division}${rangeStart + i}`
    );
    setTeamNames(names);
  }, [rangeStart, rangeEnd, division, open]);

  const handleCreate = async () => {
    try {
      const now = new Date().toISOString();
      const requestBody = {
        team_names: teamNames,
        team_template: {
          name: "string",
          session_id: 0,
          password: "string",
          start_time: now,
          end_time: now,
        },
      };
      const response = await fetch("/api/team/batch", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${localStorage.getItem("token")}`,
        },
        body: JSON.stringify(requestBody),
      });

      if (!response.ok) {
        throw new Error("Failed to create teams");
      }
      console.log("Team(s) created successfully");
      onCreate();
      setOpen(false);
    } catch (error) {
      console.error("Error creating teams:", error);
    }
  };

  return (
    <Dialog open={open} onOpenChange={setOpen}>
      <DialogTrigger>
        <Button>
          <Plus className="w-4 h-4 mr-2" />
          Create Team
        </Button>
      </DialogTrigger>
      <DialogContent>
        <DialogHeader>
          <DialogTitle>Create Team</DialogTitle>
          <DialogDescription>
            Create new team(s) for the competition.
          </DialogDescription>
        </DialogHeader>
        <Separator />
        <div className="flex flex-col gap-4">
          <DialogTitle>Division</DialogTitle>
          <RadioGroup
            value={division}
            onValueChange={(value) => setDivision(value as "B" | "C")}
            className="flex space-x-4"
          >
            <div className="flex items-center space-x-2">
              <RadioGroupItem value="B" id="division-b" />
              <Label htmlFor="division-b">Middle School (B)</Label>
            </div>
            <div className="flex items-center space-x-2">
              <RadioGroupItem value="C" id="division-c" />
              <Label htmlFor="division-c">High School (C)</Label>
            </div>
          </RadioGroup>
          <Separator />
        </div>
        <div className="flex flex-col gap-4">
          <DialogTitle>Team Numbers</DialogTitle>

          <div className="flex flex-row gap-4 items-center">
            <CounterInput
              initialValue={1}
              onChange={(value) => setRangeStart(value)}
            />
            <span>to</span>
            <CounterInput
              initialValue={1}
              onChange={(value) => setRangeEnd(value)}
            />
          </div>
          <Separator />
        </div>
        <div className="flex flex-col gap-4">
          <DialogTitle>Confirm</DialogTitle>
          <div className="flex flex-row flex-wrap gap-2 items-center">
            {teamNames.length > 0 &&
              teamNames.map((name) => (
                <Badge
                  key={name}
                  variant="basic"
                  className="bg-blue-400 hover:bg-blue-500 transition-colors"
                >
                  {name}
                </Badge>
              ))}
            {teamNames.length === 0 && (
              <DialogDescription>No teams created yet.</DialogDescription>
            )}
          </div>

          <Separator />
        </div>

        <DialogFooter>
          <Button
            variant="secondary"
            type="button"
            onClick={() => setOpen(false)}
          >
            Cancel
          </Button>
          <Button type="button" onClick={handleCreate}>
            Save
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
};

export default CreateTeamWidget;
