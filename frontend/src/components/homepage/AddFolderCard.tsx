import { Plus } from "lucide-react";
import {
  Dialog,
  DialogContent,
  DialogFooter,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "../ui/dialog";
import { Input } from "../ui/input";
import { Textarea } from "../ui/textarea";
import { Button } from "./Button";
import { EmojiSelector } from "./EmojiSelector";

export const AddFolderCard = () => {
  return (
    <Dialog>
      <DialogTrigger asChild>
        <div className="w-1/5 gap-5 flex items-center flex-wrap p-4 rounded-xl transition-colors hover:bg-gray-100 text-gray-500 border border-gray-200">
          <Plus />
          <h4 className="truncate font-semibold">Add a folder</h4>
        </div>
      </DialogTrigger>
      <DialogContent className="bg-white rounded-xl p-6 shadow-lg">
        <DialogHeader>
          <DialogTitle className="text-2xl font-bold">Add a folder</DialogTitle>
        </DialogHeader>
        <div className="flex flex-wrap gap-5">
          <div className="w-full flex flex-row items-center ">
            <EmojiSelector />
            <Input
              placeholder="Add a title..."
              className="flex-1 border-0 focus:ring-0"
            />
          </div>
          <div className="w-full h-40 text-start">
            <Textarea
              placeholder="Outline what this folder will contain"
              className="resize-none h-full text-start border border-gray-200 rounded-xl pt-2"
            />
          </div>
        </div>
        <DialogFooter>
          <Button>Confirm</Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
};
