import { ArrowRightToLine } from "lucide-react";
import { Sheet, SheetTrigger, SheetContent, SheetHeader, SheetTitle, SheetDescription } from "../ui/sheet";

export const Sidebar = () => {
  return (
    <Sheet>
      <SheetTrigger className="bg-white w-5 border-none active:outline-none focus:outline-none">
        <span>
          <ArrowRightToLine className="w-5 transition-color text-gray-500 hover:text-gray-800" />
        </span>
      </SheetTrigger>
      <SheetContent side="left" className="bg-white">
        <SheetHeader>
          <SheetTitle>Are you absolutely sure?</SheetTitle>
          <SheetDescription>
            This action cannot be undone. This will permanently delete your
            account and remove your data from our servers.
          </SheetDescription>
        </SheetHeader>
      </SheetContent>
    </Sheet>
  );
};
