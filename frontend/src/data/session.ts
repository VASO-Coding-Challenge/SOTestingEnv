const session_data = [
  {
    id: 1,
    name: "Session 1",
    start_time: "2025-02-24 16:42:58.164689",
    end_time: "2025-02-24 18:42:58.164697",
    teams: [1, 2],
  },
  {
    id: 2,
    name: "Session 2",
    start_time: "2025-02-24 19:42:58.164722",
    end_time: "2025-02-24 21:42:58.164723",
    teams: [3],
  },
];

const session_teams = [
  {
    name: "B1",
    session_id: 1,
    id: 1,
    password: "a-b-c",
  },
  {
    name: "B2",
    session_id: 1,
    id: 2,
    password: "a-b-c",
  },
  {
    name: "B3",
    session_id: 2,
    id: 3,
    password: "a-b-c",
  },
  {
    name: "B4",
    session_id: null,
    id: 4,
    password: "a-b-c",
  },
];

export { session_data, session_teams };
