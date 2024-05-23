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
import EmojiPicker, { EmojiClickData } from "emoji-picker-react";
import { useState } from "react";

export const AddFolderCard = () => {
  const [emoji, setEmoji] = useState("😊");
  const [isPickerVisible, setPickerVisible] = useState(false);

  const handleEmojiClick = (emojiData: EmojiClickData) => {
    setEmoji(emojiData.emoji);
    setPickerVisible(false);
  };
  return (
    <Dialog>
      <DialogTrigger asChild>
        <div className="w-1/5 gap-5 flex items-center flex-wrap p-4 rounded-xl hover:bg-gray-100 text-gray-500 border border-gray-200">
          <Plus />
          <h4 className="truncate font-semibold">Add a folder</h4>
        </div>
      </DialogTrigger>
      <DialogContent className="bg-white rounded-lg p-6 shadow-lg">
        <DialogHeader>
          <DialogTitle className="text-2xl font-bold">Add a folder</DialogTitle>
        </DialogHeader>
        <div className="flex flex-wrap gap-5">
          <div className="w-full flex flex-row items-center ">
            <div
              className="w-12 h-12 flex items-center justify-center border border-gray-200 hover:bg-gray-50 rounded-xl cursor-pointer"
              onClick={() => setPickerVisible(!isPickerVisible)}
            >
              <span role="img" aria-label="icon">
                {emoji}
              </span>
            </div>
            {isPickerVisible && (
              <div className="absolute z-10">
                <EmojiPicker
                  style={{
                    transform: "scale(0.7)",
                    transformOrigin: "bottom",
                  }}
                  width={"100%"}
                  onEmojiClick={handleEmojiClick}
                />
              </div>
            )}
            <span>
              <Input
                placeholder="Add a title..."
                className="flex-1 border-0 focus:ring-0"
              />
            </span>
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
