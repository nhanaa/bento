import React from "react";
import { Avatar, AvatarFallback } from "../ui/avatar";

interface HeaderProps {
  name: string;
}

export const Header: React.FC<HeaderProps> = ({ name }) => {
  function getInitials(name: string): string {
    const nameParts = name.split(" ");
    const initials = nameParts
      .map((part) => part.charAt(0).toUpperCase())
      .join("");

    return initials;
  }

  return (
    <div className="flex flex-row gap-5 items-center">
      <Avatar className="bg-customViolet text-white">
        <AvatarFallback>{getInitials(name)}</AvatarFallback>
      </Avatar>
      <div className="flex flex-col">
        <h4 className="font-semibold text-gray-800 text-lg">{name}</h4>
        <p className="text-red-500 text-sm hover:underline">Logout</p>
      </div>
    </div>
  );
};
