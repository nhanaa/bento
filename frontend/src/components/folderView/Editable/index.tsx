import "@blocknote/core/fonts/inter.css";
import {
  DragHandleButton,
  SideMenu,
  SideMenuController,
  useCreateBlockNote,
} from "@blocknote/react";
import { BlockNoteView } from "@blocknote/shadcn";
import "@blocknote/shadcn/style.css";
import { schema } from "./schema";
import { Rewrite } from "./Rewrite";
import { useRef, useEffect, useState } from "react";
import { processContent } from "@/lib/utils";
import "../../../assets/editable.css";

interface EditableProps {
  description: string;
}

export function Editable({ description }: EditableProps) {
  const initialContent = processContent(description);
  const editor = useCreateBlockNote({
    schema,
    initialContent,
  });
  const containerRef = useRef<HTMLDivElement>(null);
  const [containerWidth, setContainerWidth] = useState(0);

  useEffect(() => {
    if (containerRef.current) {
      setContainerWidth(containerRef.current.offsetWidth);
    }
  }, []);

  return (
    <div
      ref={containerRef}
      className="relative w-full h-full bg-white border border-gray-200 dark:bg-customEditor-dark rounded-xl py-1"
    >
      <BlockNoteView editor={editor} data-theming-css-demo>
        <SideMenuController
          sideMenu={(props) => (
            <SideMenu {...props}>
              <DragHandleButton {...props} />
            </SideMenu>
          )}
        />
      </BlockNoteView>
      <div className="absolute right-4 bottom-4">
        <Rewrite containerWidth={containerWidth} />
      </div>
    </div>
  );
}
