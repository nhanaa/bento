import { ArrowRightToLine } from "lucide-react";
import { Sheet, SheetTrigger, SheetContent } from "../ui/sheet";
import { FolderCardProps } from "@/lib/types";
import { FolderMenuItem } from "../homepage/FolderMenuItem";
import { AddFolderCard } from "../homepage/AddFolderCard";
import { Header } from "./Header";
import { FolderMenu } from "./FolderMenu";

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
          <Header name="Pax Nguyen" />
          <div className="flex flex-col py-5">
            <FolderMenuItem name="Home" emoji="🏠" noMenu={true} link={""} />
            <FolderMenu folders={folders} />
          </div>
        </div>
      </SheetContent>
    </Sheet>
  );
};
