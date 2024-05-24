import React, { ButtonHTMLAttributes, DetailedHTMLProps } from "react";

interface ButtonProps
  extends DetailedHTMLProps<
    ButtonHTMLAttributes<HTMLButtonElement>,
    HTMLButtonElement
  > {
  children: React.ReactNode;
}

export const Button: React.FC<ButtonProps> = ({ children, ...props }) => {
  return (
    <button
      className="bg-customViolet border-none text-white transition-colors font-semibold hover:bg-purple-500 active:bg-purple-500"
      {...props}
    >
      {children}
    </button>
  );
};
