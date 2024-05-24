import { ArrowRightToLine } from "lucide-react";
import {
  Sheet,
  SheetTrigger,
  SheetContent,
} from "../ui/sheet";
import { FolderCardProps } from "@/lib/types";
import { Avatar, AvatarFallback } from "../ui/avatar";
import { FolderMenuItem } from "./FolderMenuItem";
import { Separator } from "../ui/separator";

interface SidebarProps {
  folders: FolderCardProps[];
}

export const Sidebar: React.FC<SidebarProps> = ({ folders }) => {
  return (
    <Sheet>
      <SheetTrigger className="bg-white border-none active:outline-none focus:outline-none">
        <ArrowRightToLine className="w-5 transition-color text-gray-500 hover:text-gray-800" />
      </SheetTrigger>
      <SheetContent side="left" className="bg-white">
        <div className="flex flex-col gap-5">
          <div className="flex flex-row gap-5 items-center">
            <Avatar className="bg-customViolet text-white">
              <AvatarFallback>PN</AvatarFallback>
            </Avatar>
            <div className="flex flex-col">
              <h4 className="font-semibold text-lg">Pax Nguyen</h4>
              <p className="text-red-500 text-sm hover:underline">Logout</p>
            </div>
          </div>
          <Separator className="bg-gray-200" />
          <div className="h-full w-full">
            <div className="justify-center w-full flex flex-col">
              {folders.map((folder, index) => (
                <FolderMenuItem key={index} {...folder} />
              ))}
            </div>
          </div>
        </div>
      </SheetContent>
    </Sheet>
  );
};