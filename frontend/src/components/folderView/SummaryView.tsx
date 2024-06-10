import React from "react";
import { Editable } from "./Editable";

interface SummaryViewProps {
  description: string;
}

export const SummaryView: React.FC<SummaryViewProps> = ({ description }) => {
  return (
    <div className="w-2/3 h-full flex flex-col gap-5 px-5">
      <p className="text-gray-500">{description}</p>
      <Editable />
    </div>
  );
};
