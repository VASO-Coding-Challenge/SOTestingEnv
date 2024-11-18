import { useNavigate } from "react-router-dom";


export const LogOut = () => {
    const nav = useNavigate();

    const handle_log_out = () => {
        localStorage.removeItem("token");
        nav("/login")
    }

    return (
        <button 
        className="my-10 px-4 py-2 bg-gray-800 text-white font-bold rounded-lg text-[28px] hover:bg-gray-400 active:bg-gray-950"
        onClick={handle_log_out}>
            Log Out
        </button>
    )
}