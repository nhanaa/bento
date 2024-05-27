import { BlockNoteSchema, defaultBlockSpecs } from "@blocknote/core";
import { ToggleBlock } from "./ToggleBlock";

export const schema = BlockNoteSchema.create({
  blockSpecs: {
    ...defaultBlockSpecs,
    toggle: ToggleBlock,
  },
});
