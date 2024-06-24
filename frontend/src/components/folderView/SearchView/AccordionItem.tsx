import React from "react";
import { File, Image } from "lucide-react";

interface LinkContent {
  name: string;
  link: string;
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
  content: any;
}

export const AccordionItem: React.FC<AccordionItemProps> = ({
  type,
  content,
}) => {
  if (type === "link") {
    const linkContent = content as LinkContent;
    return <LinkItem link={linkContent.link} name={linkContent.name} favicon={linkContent.favicon} />;
  } else if (type === "screenshot") {
    const fileContent = content as FileContent;
    return <FileItem name={fileContent.name} icon={<Image className="w-4 h-4" />} />;
  } else {
    const fileContent = content as FileContent;
    return <FileItem name={fileContent.name} icon={<File className="w-4 h-4" />} />;
  }
};


const LinkItem: React.FC<LinkContent> = ({ link, name, favicon }) => {
  return (
    <a
      href={link}
      className="w-full hover:bg-customViolet-200 transition-colors text-sm font-medium text-gray-500 items-center flex flex-row p-3 border border-gray-200 bg-customViolet-100 gap-2 rounded-xl truncate"
    >
      {favicon && <img className="w-4 h-4" src={favicon} alt="favicon" />}
      {name}
    </a>
  );
};

const FileItem: React.FC<FileContent> = ({
  name,
  icon,
}) => {
  return (
    <div className="w-1/4 aspect-square hover:bg-customViolet-200 transition-colors text-sm font-medium justify-center text-center text-gray-500 items-center flex flex-col p-3 border border-gray-200 bg-customViolet-100 gap-2 rounded-xl">
      <span className="text-gray-400">{icon}</span>
      <p className="text-ellipsis">{name}</p>
    </div>
  );
};
