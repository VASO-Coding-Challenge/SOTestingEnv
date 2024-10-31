import { useState, useEffect } from "react";

export const CountdownTimer = ({end_time}: {end_time: Date}) => {
    const [timeLeft, setTimeLeft] = useState<number>(Math.floor((end_time.getTime() - Date.now()) / 1000))

    useEffect(() => {
        const timerInterval = setInterval(() => {
            setTimeLeft((prevTime) => {
                if (prevTime === 0) {
                    clearInterval(timerInterval);
                    return 0;
                } else {
                    return prevTime - 1;
                }
            });
        }, 1000);

        // Make sure to delete the interval when the component unmounts
        return () => clearInterval(timerInterval);
    }, []);

    // Get hours, minutes, and seconds
    const hours = Math.floor(timeLeft / 3600);
    const minutes = Math.floor((timeLeft % 3600) / 60);
    const seconds = timeLeft % 60;

    return (
        <p>{`${hours}:${minutes}:${seconds}`}</p>
    )
}