import React from "react";
import { File, Image } from "lucide-react";

interface LinkContent {
  name: string;
  favicon?: string;
  summary?: string;
}

interface FileContent {
  name: string;
  icon?: React.ReactNode;
  summary?: string;
  previewImg?: string;
}

interface AccordionItemProps {
  type: "link" | "screenshot" | "file";
  content: LinkContent | FileContent;
}

export const AccordionItem: React.FC<AccordionItemProps> = ({
  type,
  content,
}) => {
  if (type === "link") {
    const linkContent = content as LinkContent;
    return <LinkItem name={linkContent.name} favicon={linkContent.favicon} />;
  } else if (type === "screenshot") {
    const fileContent = content as FileContent;
    return <FileItem name={fileContent.name} icon={<Image className="w-4 h-4" />} />;
  } else {
    const fileContent = content as FileContent;
    return <FileItem name={fileContent.name} icon={<File className="w-4 h-4" />} />;
  }
};

interface LinkItemProps {
  name: string;
  favicon?: string;
  summary?: string;
}

const LinkItem: React.FC<LinkItemProps> = ({ name, favicon, summary }) => {
  return (
    <div className="w-full hover:bg-customViolet-200 transition-colors text-sm font-medium text-gray-500 items-center flex flex-row p-3 border border-gray-200 bg-customViolet-100 gap-2 rounded-xl truncate">
      {favicon && <img className="w-4 h-4" src={favicon} />}
      {name}
    </div>
  );
};

interface FileItemProps {
  name: string;
  icon?: React.ReactNode;
  summary?: string;
  previewImg?: string;
}

const FileItem: React.FC<FileItemProps> = ({
  name,
  icon,
  summary,
  previewImg,
}) => {
  return (
    <div className="w-1/4 aspect-square hover:bg-customViolet-200 transition-colors text-sm font-medium justify-center text-center text-gray-500 items-center flex flex-col p-3 border border-gray-200 bg-customViolet-100 gap-2 rounded-xl">
      <span className="text-gray-400">{icon}</span>
      <p className="text-ellipsis">{name}</p>
    </div>
  );
};
