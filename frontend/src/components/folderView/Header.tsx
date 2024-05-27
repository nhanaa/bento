import { Button } from "../homepage/Button";
import React from "react";

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
      <div>
        {/* chatbot  */}
        <Button>Share</Button>
      </div>
    </div>
  );
};
