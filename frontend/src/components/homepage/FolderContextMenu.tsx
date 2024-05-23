import { EllipsisVertical } from "lucide-react";
import {
  ContextMenu,
  ContextMenuContent,
  ContextMenuItem,
  ContextMenuTrigger,
  ContextMenuSeparator,
} from "../ui/context-menu";

export const FolderContextMenu = () => {
  return (
    <ContextMenu>
      <ContextMenuTrigger>
        <EllipsisVertical className="text-gray-500 w-4" />
      </ContextMenuTrigger>
      <ContextMenuContent className="bg-white  rounded-xl">
        <ContextMenuItem>Open in new tab</ContextMenuItem>
        <ContextMenuItem>Rename</ContextMenuItem>
        <ContextMenuSeparator className="bg-gray-200" />
        <ContextMenuItem className="text-red-500">Delete</ContextMenuItem>
      </ContextMenuContent>
    </ContextMenu>
  );
};
