import { PlusIcon } from "@radix-ui/react-icons";

export const AddFolder = () => {
  return (
    <div className="w-3/4 justify-between flex items-center flex-wrap p-4 rounded-xl shadow bg-transparent transition-colors hover:bg-gray-100 border border-gray-200 text-base text-gray-800 font-semibold">
      <div className="w-full flex flex-wrap items-center gap-5">
        <PlusIcon className="w-5 h-5 text-gray-500" />
        <h4 className="w-3/5 truncate text-gray-500 font-semibold">Add a folder</h4>
      </div>
    </div>
  );
};
