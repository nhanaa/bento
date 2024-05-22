import React from "react";
import Weather from "../components/homepage/TimeAndWeather";

const Homepage: React.FC = () => {
  return (
    <div className="h-screen w-screen">
      <div className="flex flex-col justify-center items-center gap-5 p-10">
        <h1 className="font-bold ">Hello Pax!</h1>
        <Weather />
      </div>
      <div className="w-screen flex flex-wrap bg-gray-50 border-t border-gray-200">
        <p>Hola</p>
      </div>
    </div>
  );
};

export default Homepage;
