import { ArrowRightToLine } from "lucide-react";
import {
  Sheet,
  SheetTrigger,
  SheetContent,
} from "./ui/sheet";
import { FolderCardProps } from "@/lib/types";
import { Avatar, AvatarFallback } from "./ui/avatar";
import { FolderMenuItem } from "./homepage/FolderMenuItem";
import { AddFolderCard } from "./homepage/AddFolderCard";

interface SidebarProps {
  folders: FolderCardProps[];
}

export const Sidebar: React.FC<SidebarProps> = ({ folders }) => {
  return (
    <Sheet>
      <SheetTrigger className="bg-foreground border-none active:outline-none focus:outline-none">
        <ArrowRightToLine className="w-5 transition-color text-gray-500 hover:text-gray-800" />
      </SheetTrigger>
      <SheetContent side="left" className="bg-white">
        <div className="flex flex-col gap-5">
          <div className="flex flex-row gap-5 items-center">
            <Avatar className="bg-customViolet text-white">
              <AvatarFallback>PN</AvatarFallback>
            </Avatar>
            <div className="flex flex-col">
              <h4 className="font-semibold text-gray-800 text-lg">
                Pax Nguyen
              </h4>
              <p className="text-red-500 text-sm hover:underline">Logout</p>
            </div>
          </div>
          <div className="flex flex-col py-5">
            <div className="group flex flex-row justify-between items-center rounded-xl px-1 transition-colors hover:bg-gray-100">
              <p className="font-semibold text-sm text-gray-400">Folders</p>
              <AddFolderCard
                triggerProps={
                  "scale-75 p-1 text-gray-500 justify-center rounded-xl opacity-0 group-hover:opacity-100 transition-opacity transition-colors hover:bg-gray-200"
                }
                textHidden={true}
              />
            </div>
            <div className="h-full w-full">
              <div className="justify-center w-full flex flex-col">
                {folders.map((folder, index) => (
                  <FolderMenuItem key={index} {...folder} />
                ))}
              </div>
            </div>
          </div>
        </div>
      </SheetContent>
    </Sheet>
  );
};