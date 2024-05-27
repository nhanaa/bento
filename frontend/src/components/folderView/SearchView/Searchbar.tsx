import { Input } from "@/components/ui/input";
import { Search } from "lucide-react"

export const Searchbar = () => {
    return (
      <div className="flex flex-row gap-2 items-center px-2">
        <Search className="w-4 h-4 text-gray-500" />
        <Input
          placeholder="Search..."
          className="border-0 text-md focus:ring-0 text-gray-500 placeholder-gray-500"
          style={{ padding: 0 }}
        />
      </div>
    );
}