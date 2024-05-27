import { ChevronDown, ChevronUp } from "lucide-react";
import React, { useState } from "react";
import { AccordionItem } from "./AccordionItem";
import { motion } from "framer-motion";

interface AccordionProps {
  emoji: string;
  name: string;
  content: { type: "link" | "screenshot" | "file"; content: any }[]; // Define content as an array of items
}

export const Accordion: React.FC<AccordionProps> = ({
  emoji,
  name,
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
          {isOpen ? (
            <ChevronUp className="w-4 h-4" />
          ) : (
            <ChevronDown className="w-4 h-4" />
          )}
        </div>
      </div>
      <motion.div
        initial={false}
        animate={{ height: isOpen ? "auto" : 0 }}
        style={{ overflow: "hidden" }}
      >
        {isOpen && (
          <div className="flex flex-wrap gap-1 p-2">
            {content.map((item, index) => (
              <AccordionItem
                key={index}
                type={item.type}
                content={item.content}
              />
            ))}
          </div>
        )}
      </motion.div>
    </div>
  );
};
