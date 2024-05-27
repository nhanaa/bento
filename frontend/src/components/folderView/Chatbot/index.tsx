import {
  Dialog,
  DialogContent,
  DialogFooter,
  DialogTrigger,
} from "@/components/ui/dialog";
import { mockMessages } from "@/lib/mocks";
import { Message } from "./Message";
import { Separator } from "@/components/ui/separator";
import { Chatbox } from "./Chatbox";

export const Chatbot = () => {
  return (
    <Dialog>
      <DialogTrigger asChild>
        <button className="bg-customViolet-100 border border-customViolet text-customViolet transition-colors active:border-none focus:border-none font-semibold hover:text-white hover:bg-purple-500 active:text-white active:bg-purple-500 gap-2 items-center">
          💬 Chat
        </button>
      </DialogTrigger>
      <DialogContent className="aspect-video h-screen bg-customViolet-100 border border-customViolet rounded-xl p-6">
        <div className="flex flex-col gap-5 overflow-scroll">
          {mockMessages.map((msg, index) => (
            <>
              <Message key={index} user={msg.user} message={msg.message} />
              {index < mockMessages.length - 1 && (
                <Separator className="bg-gray-200" />
              )}
            </>
          ))}
        </div>
        <div className="absolute bottom-0 left-0 w-full pointer-events-none bg-gradient-to-t from-gray-50 to-transparent"></div>
        <div className="absolute bottom-0 left-0 w-full pointer-events-auto p-4">
          <Chatbox />
        </div>
      </DialogContent>
    </Dialog>
  );
};
