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
import { Button } from "../Button";
import { EmojiSelector } from "./EmojiSelector";
import { useState } from "react";
import { useUser } from "@/contexts/UserContext";
import { useQueryClient } from "react-query";
import { addFolder } from "@/hooks/useFolder";
import { AddFolderData } from "@/lib/types";
interface AddFolderCardProps {
  triggerProps?: string;
  textHidden?: boolean;
}

export const AddFolderCard: React.FC<AddFolderCardProps> = ({
  triggerProps,
  textHidden = false,
}) => {
  const [ title, setTitle ] = useState('');
  const [ emoji, setEmoji ] = useState('😊');
  const [summary, setSummary] = useState('');
  const queryClient = useQueryClient();
  const { user } = useUser()
  const { mutate, isLoading, isError, error, isSuccess } = addFolder();

  const handleAddFolder = () => {
    if (!user) {
      console.error("User is not logged in");
      return;
    }

    const data: AddFolderData = {
      user_id: user.id,
      name: `${emoji}_${title}`,
      summary,
    };
    mutate(data, {
      onSuccess: () => {
        queryClient.invalidateQueries(["folders", user.id]);
        setTitle("");
        setSummary("");
        setEmoji("😊"); 
      },
    });
  };
  return (
    <Dialog>
      <DialogTrigger asChild>
        <div className={triggerProps}>
          <Plus />
          {!textHidden && (
            <h4 className="truncate font-semibold">Add a folder</h4>
          )}
        </div>
      </DialogTrigger>
      <DialogContent className="bg-white text-gray-500 rounded-xl p-6 shadow-lg">
        <DialogHeader>
          <DialogTitle className="text-2xl text-gray-800 font-bold">
            Add a folder
          </DialogTitle>
        </DialogHeader>
        <div className="flex flex-wrap gap-5">
          <div className="w-full flex flex-row items-center ">
            <EmojiSelector onEmojiSelect={setEmoji} />
            <Input
              placeholder="Add a title..."
              value={title}
              onChange={(e) => setTitle(e.target.value)}
              className="flex-1 border-0 focus:ring-0 placeholder-gray-500"
            />
          </div>
          <div className="w-full h-40 text-start">
            <Textarea
              placeholder="Outline what this folder will contain"
              onChange={(e) => setSummary(e.target.value)}
              className="resize-none h-full text-start border border-gray-200 rounded-xl pt-2 placeholder-gray-500"
            />
          </div>
        </div>
        <DialogFooter>
          <Button isLoading={isLoading} onClick={handleAddFolder}>Confirm</Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
};
