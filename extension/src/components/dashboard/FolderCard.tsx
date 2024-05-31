import { truncateString } from "@/lib/utils";
import { ExternalLinkIcon } from "@radix-ui/react-icons";

export type FolderCardProps = {
  emoji: string;
  name: string;
  link?: string;
};

export const FolderCard = ({ emoji, name, link }: FolderCardProps) => {
  return (
    <div className="w-3/4 justify-between flex items-center flex-wrap p-4 rounded-xl shadow bg-white transition-colors hover:bg-gray-100 border border-gray-200 text-base text-gray-800 font-semibold">
      <div className="w-full flex flex-wrap items-center gap-5">
        <h4>{emoji}</h4>
        <h4 className="w-3/5 truncate text-gray-800 font-semibold">{truncateString(name, 12)}</h4>
        <ExternalLinkIcon className="w-4 h-4 text-gray-500" />
      </div>
    </div>
  );
};
