import { BlockNoteSchema, defaultBlockSpecs } from "@blocknote/core";

export const schema = BlockNoteSchema.create({
  blockSpecs: {
    ...defaultBlockSpecs,
  },
});
