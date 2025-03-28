export interface Session {
  /**
   * Represents a session with a unique ID, name, start and end times, and associated teams
   */
  id: number;
  name: string;
  start_time: string;
  end_time: string;
  teams: number[];
}
