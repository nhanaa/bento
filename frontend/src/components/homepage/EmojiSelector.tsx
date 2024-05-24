import EmojiPicker, { EmojiClickData } from "emoji-picker-react";
import { useState } from "react";
import { Input } from "../ui/input";

export const EmojiSelector = () => {
  const [emoji, setEmoji] = useState("😊");
  const [isPickerVisible, setPickerVisible] = useState(false);

  const handleEmojiClick = (emojiData: EmojiClickData) => {
    setEmoji(emojiData.emoji);
    setPickerVisible(false);
  };
  return (
    <>
      <div
        className="w-12 h-12 transition-colors flex items-center justify-center border border-gray-200 hover:bg-gray-50 rounded-xl cursor-pointer"
        onClick={() => setPickerVisible(!isPickerVisible)}
      >
        <span role="img" aria-label="icon">
          {emoji}
        </span>
      </div>
      {isPickerVisible && (
        <div className="absolute z-10">
          <EmojiPicker
            style={{
              transform: "scale(0.7)",
              transformOrigin: "bottom",
            }}
            width={"100%"}
            onEmojiClick={handleEmojiClick}
          />
        </div>
      )}
    </>
  );
};
