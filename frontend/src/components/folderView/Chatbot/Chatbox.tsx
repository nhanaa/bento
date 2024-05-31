import { Input } from "@/components/ui/input";
import { Send } from "lucide-react";

export const Chatbox = () => {
  return (
    <div className="w-full flex flex-row justify-between items-center px-5 py-3 bg-white rounded-xl border border-gray-200 shadow">
      <Input
        placeholder="Ask me anything..."
        className="border-0 text-sm focus:ring-0 text-gray-500 placeholder-gray-500"
        style={{ padding: 0 }}
      />
      <span><Send className="w-4 h-4 text-customViolet hover:text-customViolet-500 transition-colors" /></span>
    </div>
  );
};
