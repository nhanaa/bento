import { Input } from "@/components/ui/input";
import React, { useState } from "react";
import { motion } from "framer-motion";

interface RewriteProps {
  containerWidth: number;
}

export const Rewrite: React.FC<RewriteProps> = ({ containerWidth }) => {
  const [open, setOpen] = useState(false);

  function handleClick() {
    setOpen(!open);
  }

  return (
    <div
      onClick={handleClick}
      className="inline-flex items-center space-x-2 text-gray-800 font-semibold text-sm px-3 z-10 bg-white transition-colors hover:bg-gray-100 border-gray-200 border rounded-xl shadow cursor-pointer"
    >
      <span>✍️</span>
      {open ? (
        <motion.div
          initial={{ width: 0, opacity: 0 }}
          animate={{ width: containerWidth * 0.85, opacity: 1 }}
          transition={{ duration: 0.3 }}
          className="overflow-hidden"
        >
          <Input
            placeholder="Tell AI how to rewrite this..."
            className="border-0 focus:ring-0 font-medium text-gray-500 placeholder-gray-500"
            style={{ padding: 0 }}
          />
        </motion.div>
      ) : (
        <motion.span
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ duration: 0.3 }}
          className="transition-all py-2 duration-300"
        >
          Rewrite
        </motion.span>
      )}
    </div>
  );
};
