import React, { useState, useEffect } from "react";
import { format } from "date-fns";

const Weather: React.FC = () => {
  const [currentTime, setCurrentTime] = useState(new Date());

  useEffect(() => {
    const intervalId = setInterval(() => {
      setCurrentTime(new Date());
    }, 1000);

    return () => clearInterval(intervalId);
  }, []);

  const formattedDate = format(currentTime, "EEEE, MMMM do, yyyy");
  const formattedTime = format(currentTime, "HH:mm:ss");

  return (
    <div className="flex items-center gap-20 p-4">
      <div className="flex flex-col justify-center">
        <p className="text-gray-500">{formattedDate}</p>
        <h2 className="text-3xl font-semibold">{formattedTime}</h2>
      </div>
      <div className="flex items-center space-x-2">
        <div className="text-6xl">🌧️</div>
        <div className="flex flex-col">
          <h2 className="text-2xl font-semibold">60°</h2>
          <p className="text-gray-500">Philadelphia</p>
        </div>
      </div>
    </div>
  );
};

export default Weather;
