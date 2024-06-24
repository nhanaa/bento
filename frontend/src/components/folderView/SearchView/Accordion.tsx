import { ChevronDown, ChevronUp } from "lucide-react";
import React, { useState } from "react";
import { AccordionItem } from "./AccordionItem";
import { motion } from "framer-motion";

interface AccordionProps {
  emoji: string;
  name: string;
  type: string;
  content: any[]; // Define content as an array of items
}

export const Accordion: React.FC<AccordionProps> = ({
  emoji,
  name,
  type,
  content,
}) => {
  const [isOpen, setIsOpen] = useState(false);
  function handleClick() {
    setIsOpen(!isOpen);
  }

  return (
    <div>
      <div
        onClick={handleClick}
        className="w-full bg-white hover:bg-gray-100 transition-colors rounded-xl border border-gray-200 p-3"
      >
        <div className="flex items-center flex-row text-sm text-gray-600 justify-between font-semibold">
          <div className="flex flex-row gap-2 ">
            <span>{emoji}</span>
            <span>{name}</span>
          </div>
          <div className="items-center flex flex-row gap-2 ">
            <span className="text-xs text-gray-500">
              {content ? content.length : 0}
            </span>
            {isOpen ? (
              <ChevronUp className="w-4 h-4" />
            ) : (
              <ChevronDown className="w-4 h-4" />
            )}
          </div>
        </div>
      </div>
      <motion.div
        initial={false}
        animate={{ height: isOpen ? "auto" : 0 }}
        style={{ overflow: "hidden" }}
      >
        {isOpen && content && (
          <div className="flex flex-wrap gap-1 p-2">
            {content.map((item, index) => (
              <AccordionItem key={index} type={type} content={item} />
            ))}
          </div>
        )}
      </motion.div>
    </div>
  );
};
