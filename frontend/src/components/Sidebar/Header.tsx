import React from "react";
import { Avatar, AvatarFallback } from "../ui/avatar";
import useLogout from "@/hooks/useLogout";
import { useUser } from "@/contexts/UserContext";

interface HeaderProps {
  name: string;
}

export const Header: React.FC<HeaderProps> = () => {
  const { logout } = useLogout();
  const { user } = useUser();

  function getInitials(name: string): string {
    const nameParts = name.split(" ");
    const initials = nameParts
      .map((part) => part.charAt(0).toUpperCase())
      .join("");

    return initials;
  }

  if (!user) {
    return;
  } else {
    return (
      <div className="flex flex-row gap-5 items-center">
        <Avatar className="bg-customViolet text-white">
          <AvatarFallback>{getInitials(user["name"])}</AvatarFallback>
        </Avatar>
        <div className="flex flex-col">
          <h4 className="font-semibold text-gray-800 text-lg">
            {user["name"]}
          </h4>
          <p className="text-red-500 text-sm hover:underline" onClick={logout}>
            Logout
          </p>
        </div>
      </div>
    );
  }
};
