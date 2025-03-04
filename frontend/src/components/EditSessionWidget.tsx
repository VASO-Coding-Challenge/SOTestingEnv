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
import { Separator } from "@/components/ui/separator";
import { Badge } from "@/components/ui/badge";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { PencilLine, Plus, X } from "lucide-react";

const EditSessionWidget = ({ session, teams, onSave }) => {
  // Local state for date, start time, end time and selected teams
  const [date, setDate] = useState("");
  const [startTime, setStartTime] = useState("");
  const [endTime, setEndTime] = useState("");
  const [selectedTeams, setSelectedTeams] = useState([]);
  const [selectedTeam, setSelectedTeam] = useState("");

  // When the session (or teams) changes, prepopulate fields
  useEffect(() => {
    if (session) {
      // Extract date and times from ISO strings
      const sessionDate = session.start_time.split("T")[0];
      const sessionStartTime = session.start_time.split("T")[1].substring(0, 5);
      const sessionEndTime = session.end_time.split("T")[1].substring(0, 5);
      setDate(sessionDate);
      setStartTime(sessionStartTime);
      setEndTime(sessionEndTime);

      const initialTeams = teams.filter((team) =>
        session.teams.includes(team.id)
      );
      setSelectedTeams(initialTeams);
    }
  }, [session, teams]);

  const handleAddTeam = (teamName) => {
    if (teamName && !selectedTeams.find((team) => team.name === teamName)) {
      const teamToAdd = teams.find((team) => team.name === teamName);
      if (teamToAdd) {
        setSelectedTeams([...selectedTeams, teamToAdd]);
      }
    }
    setSelectedTeam("");
  };

  const handleRemoveTeam = (teamId) => {
    setSelectedTeams(selectedTeams.filter((team) => team.id !== teamId));
  };

  const handleSave = async () => {
    // Build the updated session payload
    const updatedSession = {
      name: session.name,
      start_time: `${date}T${startTime}:00Z`,
      end_time: `${date}T${endTime}:00Z`,
      id: session.id,
      teams: selectedTeams.map((team) => team.id),
    };
    onSave(updatedSession, session);
  };

  return (
    <Dialog>
      <DialogTrigger>
        <PencilLine className="cursor-pointer" />
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
              <Badge
                key={team.id}
                variant="secondary"
                className="bg-blue-400 flex items-center"
              >
                {team.name}
                <X
                  size={16}
                  className="-mr-1 hover:text-[#FE7A7A] cursor-pointer transition-colors"
                  onClick={() => handleRemoveTeam(team.id)}
                />
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
