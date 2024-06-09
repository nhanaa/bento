import React, { ReactNode } from "react";
import logo from "/icon.svg";
import { Avatar, AvatarImage, AvatarFallback } from "@/components/ui/avatar";

interface MessageProps {
  user: string;
  message: string;
  isPending?: boolean;
  children?: ReactNode;
}

export const Message: React.FC<MessageProps> = ({ user, message }) => {
  const sender = user === "Bento" ? "Bento" : "You";
  const imageSrc = user === "Bento" ? logo : null;
  const altText = user === "Bento" ? "@Bento" : "@You";
  const fallbackText = "PN";

  const formatMessage = (text: string) => {
    return text.split("\n").map((line, index) => {
      if (line.startsWith("- ")) {
        return <li key={index}>{line.replace("- ", "")}</li>;
      }
      return <p key={index}>{line}</p>;
    });
  };

  return (
    <div className="flex flex-row space-x-5 p-5 items-start text-xs text-gray-500">
      <Avatar>
        {imageSrc && <AvatarImage src={imageSrc} alt={altText} />}
        <AvatarFallback className="bg-customViolet-500 text-white">
          {fallbackText}
        </AvatarFallback>
      </Avatar>
      <div className="w-full space-y-2 flex flex-col">
        <h1 className="text-gray-800 text-sm font-semibold">{sender}</h1>
        <div className="list-disc space-y-2">{formatMessage(message)}</div>
      </div>
    </div>
  );
};
