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
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { Separator } from "@radix-ui/react-select";
import { Badge } from "@/components/ui/badge";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { PencilLine, Plus } from "lucide-react";

const EditSessionWidget = ({ session, teams, onSave }) => {
  const [date, setDate] = useState(session?.date || "");
  const [startTime, setStartTime] = useState(session?.startTime || "");
  const [endTime, setEndTime] = useState(session?.endTime || "");
  const [selectedTeams, setSelectedTeams] = useState(session?.teams || []);
  const [selectedTeam, setSelectedTeam] = useState("");

  const handleSave = () => {
    onSave({
      ...session,
      date,
      startTime,
      endTime,
      teams: selectedTeams,
    });
  };

  const handleAddTeam = (teamName) => {
    if (teamName && !selectedTeams.find((team) => team.name === teamName)) {
      const teamToAdd = teams.find((team) => team.name === teamName);
      if (teamToAdd) {
        setSelectedTeams([...selectedTeams, teamToAdd]);
      }
    }
    setSelectedTeam("");
  };

  return (
    <Dialog>
      <DialogTrigger>
        <PencilLine />
      </DialogTrigger>
      <DialogContent>
        <DialogHeader>
          <DialogTitle>Edit Session</DialogTitle>
          <DialogDescription>Edit the session details below.</DialogDescription>
        </DialogHeader>
        <div className="flex flex-col gap-4">
          <DialogTitle>Date & Time</DialogTitle>
          <div className="flex flex-row gap-4 items-center">
            Date:{" "}
            <Input
              type="date"
              value={date}
              onChange={(e) => setDate(e.target.value)}
            />
          </div>
          <div className="flex flex-row gap-4 items-center">
            Time:{" "}
            <Input
              type="time"
              value={startTime}
              onChange={(e) => setStartTime(e.target.value)}
            />
            to{" "}
            <Input
              type="time"
              value={endTime}
              onChange={(e) => setEndTime(e.target.value)}
            />
          </div>
          <Separator />
        </div>
        <div className="flex flex-col gap-4">
          <DialogTitle>Team Selection</DialogTitle>
          <div className="flex flex-row gap-2 flex-wrap">
            {selectedTeams.map((team) => (
              <Badge key={team.id} variant="secondary" className="bg-blue-400">
                {team.name}
              </Badge>
            ))}
          </div>
          <div className="flex flex-row items-center">
            <Select value={selectedTeam} onValueChange={setSelectedTeam}>
              <SelectTrigger className="rounded-r-none">
                <SelectValue placeholder="Select a Team" />
              </SelectTrigger>
              <SelectContent>
                {teams.map((team) => (
                  <SelectItem key={team.id} value={team.name}>
                    {team.name}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
            <Button
              type="button"
              className="rounded-l-none -ml-px"
              onClick={() => handleAddTeam(selectedTeam)}
            >
              <Plus />
            </Button>
          </div>
          <Separator />
        </div>
        <DialogFooter>
          <Button variant="secondary" type="button">
            Cancel
          </Button>
          <Button type="button" onClick={handleSave}>
            Save
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
};

export default EditSessionWidget;
