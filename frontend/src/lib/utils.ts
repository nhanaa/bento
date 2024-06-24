import { type ClassValue, clsx } from "clsx"
import { twMerge } from "tailwind-merge"
import { ContentType } from "./types";

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}

export const processContent = (input: string): ContentType[] => {

  const sections = input.split("-").filter(section => section.trim() !== "");

  const mockInitialContent = sections.map(section => ({
    type: "heading",
    props: {
      level: 3,
    },
    content: section.trim().replace("-",""),
  }));

  return mockInitialContent;
};
