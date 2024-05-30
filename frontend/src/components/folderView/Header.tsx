import { Button } from "../Button";
import React from "react";
import { Chatbot } from "./Chatbot";

interface HeaderProps {
  emoji: string;
  name: string;
}

export const Header: React.FC<HeaderProps> = ({ emoji, name }) => {
  return (
    <div className="flex flex-wrap justify-between">
      <div className="flex flex-row gap-5 font-semibold text-3xl">
        <h2>{emoji}</h2>
        <h2>{name}</h2>
      </div>
      <div className="flex flex-row gap-2">
        <Chatbot />
        <Button>Share</Button>
      </div>
    </div>
  );
};
