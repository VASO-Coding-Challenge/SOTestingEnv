// Author: Andrew Lockard
import React, { useState, useEffect } from "react";

interface TeamMember {
  id: number | null;
  first_name: string;
  last_name: string;
}

export const MemberInput = ({ token }: { token: string }) => {
  const [members, setMembers] = useState<TeamMember[]>([]);
  const [newName, setNewName] = useState<string>("");
  const [errorDisplay, setErrorDisplay] = useState<JSX.Element>(<></>);

  useEffect(() => {
    const getMembers = async () => {
      const res = await fetch("/api/team/members", {
        headers: { Authorization: `Bearer ${token}` },
      });
      const json = (await res.json()) as TeamMember[];
      setMembers(json);
    };
    void getMembers();
  }, [token]);

  const delete_member = async (member_id: number) => {
    const res = await fetch(`/api/team/members/${member_id}`, {
      method: "DELETE",
      headers: { Authorization: `Bearer ${token}` },
    });
    if (res.ok) {
      setMembers((members) =>
        members.filter((member) => member.id !== member_id)
      );
    }
  };

  const add_new_member = async () => {
    const [firstname, ...rest] = newName.split(" ");
    const lastname = rest.join(" ");
    if (firstname === "") {
      throw new Error("Please enter a name.");
    } else if (lastname === "") {
      throw new Error("Please enter a last name separated by a space.")
    }

    const res = await fetch("/api/team/members", {
      method: "POST",
      headers: {
        Authorization: `Bearer ${token}`,
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        first_name: firstname,
        last_name: lastname,
      }),
    });
    if (res.ok) {
      const new_member = (await res.json()) as TeamMember;
      setMembers([...members, new_member]);
      setNewName("");
    } else {
      return res.json().then((json: { message: string }) => {
        throw new Error(json.message);
      });
    }
  };

  const on_submit = () => {
    add_new_member().catch((err) => {
      add_error_handler((err as Error).message);
    });
  };

  const submit_if_enter = (event: React.KeyboardEvent<HTMLInputElement>) => {
    if (event.key === "Enter") {
      on_submit();
    }
  };

  const add_error_handler = (msg: string = "") => {
    setErrorDisplay(
      <p className="text-red-500 text-center">
        Error: {msg} 
      </p>
    );
    setTimeout(() => setErrorDisplay(<></>), 10000);
  };

  const members_jsx = members.map((member) => (
    <tr key={member.id} className="border-b border-slate-600">
      <td className="w-[80%] text-center pb-1 justify-center">{member.first_name} {member.last_name}</td>
      <td className="w-[20%] py-2"><DeleteButton delete_handler={delete_member} member_id={member.id!} /></td>
    </tr>
  ));

  return (
    <>
      <h2 className="mt-2 text-center text-[130%] font-semibold">
        Please tell us your team member&apos;s names:
      </h2>
      <div className="float-root">
        <input
          value={newName}
          placeholder="Firstname Lastname"
          onChange={(e) => setNewName(e.target.value)}
          className="h-[50px]  max-w-[500px] text-lg rounded-[8px] border bg-white border-gray-300 pl-2 mt-2 mb-4 float-left"
          onKeyDown={submit_if_enter}
          required
        />
        <button onClick={on_submit} className="bg-white border border-gray-300 fill-black hover:fill-green-500 float-right p-1 ml-2 mt-3 rounded-[12px]">
          <svg
            xmlns="http://www.w3.org/2000/svg"
            height="30px"
            viewBox="0 -960 960 960"
            width="30px"
          >
            <path d="M720-400v-120H600v-80h120v-120h80v120h120v80H800v120h-80Zm-360-80q-66 0-113-47t-47-113q0-66 47-113t113-47q66 0 113 47t47 113q0 66-47 113t-113 47ZM40-160v-112q0-34 17.5-62.5T104-378q62-31 126-46.5T360-440q66 0 130 15.5T616-378q29 15 46.5 43.5T680-272v112H40Zm80-80h480v-32q0-11-5.5-20T580-306q-54-27-109-40.5T360-360q-56 0-111 13.5T140-306q-9 5-14.5 14t-5.5 20v32Zm240-320q33 0 56.5-23.5T440-640q0-33-23.5-56.5T360-720q-33 0-56.5 23.5T280-640q0 33 23.5 56.5T360-560Zm0-80Zm0 400Z" />
          </svg>
        </button>
      </div>
      {errorDisplay}
      <p className="w-[80%] text-center border-b border-slate-600 pb-2 font-semibold">Current Members</p>
      <table className="border-collapse table-fixed w-[80%]">
        <tbody>
          {members_jsx}
        </tbody>
      </table>
    </>
  );
};

const DeleteButton = ({
  delete_handler,
  member_id,
}: {
  delete_handler: (id: number) => Promise<void>;
  member_id: number;
}) => {
  const click_handler = () => {
    void delete_handler(member_id);
  };

  return (
    <button onClick={click_handler} className="fill-black hover:fill-red-500">
      <svg
        xmlns="http://www.w3.org/2000/svg"
        height="24px"
        viewBox="0 -960 960 960"
        width="24px"
      >
        <path d="M640-520v-80h240v80H640Zm-280 40q-66 0-113-47t-47-113q0-66 47-113t113-47q66 0 113 47t47 113q0 66-47 113t-113 47ZM40-160v-112q0-34 17.5-62.5T104-378q62-31 126-46.5T360-440q66 0 130 15.5T616-378q29 15 46.5 43.5T680-272v112H40Zm80-80h480v-32q0-11-5.5-20T580-306q-54-27-109-40.5T360-360q-56 0-111 13.5T140-306q-9 5-14.5 14t-5.5 20v32Zm240-320q33 0 56.5-23.5T440-640q0-33-23.5-56.5T360-720q-33 0-56.5 23.5T280-640q0 33 23.5 56.5T360-560Zm0-80Zm0 400Z" />
      </svg>
    </button>
  );
};
