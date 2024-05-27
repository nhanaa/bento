import "@blocknote/core/fonts/inter.css";
import { useCreateBlockNote } from "@blocknote/react";
import { BlockNoteView } from "@blocknote/shadcn";
import "@blocknote/shadcn/style.css";
import { schema } from "./schema";
import { Rewrite } from "./Rewrite";
import { useRef, useEffect, useState } from "react";

export function Editable() {
  const editor = useCreateBlockNote({
    schema,
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
      <BlockNoteView
        editor={editor}
        style={{ width: "100%", height: "100%" }}
      />
      <div className="absolute right-4 bottom-4">
        <Rewrite containerWidth={containerWidth} />
      </div>
    </div>
  );
}
