import { createReactBlockSpec } from "@blocknote/react";
import { useState } from "react";

export const ToggleBlock = createReactBlockSpec(
  {
    type: "toggle",
    propSchema: {
      title: { default: "Toggle", values: [] },
      content: { default: "", values: [] },
    },
    content: "inline",
  },
  {
    render: ({ block, contentRef }) => {
      const [isOpen, setIsOpen] = useState(false);
      return (
        <div className="toggle-block">
          <div className="toggle-header" onClick={() => setIsOpen(!isOpen)}>
            <h4>{block.props.title}</h4>
          </div>
          {isOpen && (
            <div className="toggle-content" ref={contentRef}>
              {block.props.content ||
                "Empty toggle. Click or drop blocks inside."}
            </div>
          )}
        </div>
      );
    },
  }
);
