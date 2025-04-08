import { Session } from "./session";

export interface Team {
  /**
   * Represents a team with a unique ID, name, and associated session
   */
  name: string;
  id: number;
  password: string;
  session_id: number | null;
  session: Session | null;
}

export interface TeamMember {
  /**
   * Represents a team member with a unique ID, first and last name
   */
  first_name: string;
  last_name: string;
  id: number;
}

export interface TeamScore {
  /**
   * Represents a team's score in a competition.
   */
  "Team Number": string;
  Score: number;
  "Max Score": number;
}
