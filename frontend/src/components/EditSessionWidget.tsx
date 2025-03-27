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
  const [open, setOpen] = useState(false);
  // Local state for date, start time, end time and selected teams
  const [name, setName] = useState("");
  const [date, setDate] = useState("");
  const [startTime, setStartTime] = useState("");
  const [endTime, setEndTime] = useState("");
  const [selectedTeams, setSelectedTeams] = useState([]);
  const [selectedTeam, setSelectedTeam] = useState("");

  // When the session (or teams) changes, prepopulate fields
  useEffect(() => {
    if (session) {
      const startDateTime = new Date(session.start_time);
      const endDateTime = new Date(session.end_time);

      // Convert UTC dates to local date strings (YYYY-MM-DD)
      const sessionDate = startDateTime.toLocaleDateString("en-CA");

      // Convert UTC times to local time strings (HH:mm)
      const sessionStartTime = startDateTime.toLocaleTimeString("en-GB", {
        hour: "2-digit",
        minute: "2-digit",
        hour12: false,
      });
      const sessionEndTime = endDateTime.toLocaleTimeString("en-GB", {
        hour: "2-digit",
        minute: "2-digit",
        hour12: false,
      });

      setName(session.name);
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
    // Create Date objects from local date and time inputs
    const startDateTime = new Date(`${date}T${startTime}:00`);
    const endDateTime = new Date(`${date}T${endTime}:00`);

    // Function to format date as local ISO string without timezone
    const formatLocalISO = (date: Date) => {
      const pad = (num: number) => num.toString().padStart(2, "0");
      return `${date.getFullYear()}-${pad(date.getMonth() + 1)}-${pad(
        date.getDate()
      )}T${pad(date.getHours())}:${pad(date.getMinutes())}:00`;
    };

    // Convert to local ISO strings
    const start_time = formatLocalISO(startDateTime);
    const end_time = formatLocalISO(endDateTime);

    // Create updated session object
    const updatedSession = {
      name: name,
      start_time: start_time,
      end_time: end_time,
      id: session.id,
      teams: selectedTeams.map((team) => team.id),
    };

    onSave(updatedSession, session);
    setOpen(false);
  };

  return (
    <Dialog open={open} onOpenChange={setOpen}>
      <DialogTrigger>
        <PencilLine className="hover:text-[#b1b1b1] cursor-pointer transition-colors" />
      </DialogTrigger>
      <DialogContent>
        <DialogHeader>
          <DialogTitle>Edit Session</DialogTitle>
          <DialogDescription>Edit the session details below.</DialogDescription>
        </DialogHeader>
        <div className="flex flex-col gap-4">
          <DialogTitle>Name</DialogTitle>
          <div className="flex flex-row gap-4 items-center">
            Name:{" "}
            <Input
              type="text"
              value={name}
              onChange={(e) => setName(e.target.value)}
            />
          </div>
          <Separator />

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
          <div className="flex flex-row flex-wrap gap-2 flex-wrap">
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
              type="submit"
              className="rounded-l-none -ml-px"
              onClick={() => handleAddTeam(selectedTeam)}
            >
              <Plus />
            </Button>
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
          <Button type="button" onClick={handleSave}>
            Save
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
};

export default EditSessionWidget;
