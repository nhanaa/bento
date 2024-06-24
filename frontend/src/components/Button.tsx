import React, { ButtonHTMLAttributes, DetailedHTMLProps } from "react";
import { Spinner } from "./Spinner";

interface ButtonProps
  extends DetailedHTMLProps<
    ButtonHTMLAttributes<HTMLButtonElement>,
    HTMLButtonElement
  > {
  children: React.ReactNode;
  isLoading?: boolean;
}

export const Button: React.FC<ButtonProps> = ({ children, isLoading = false, ...props }) => {
  return (
    <button
      className="bg-customViolet border-none text-white transition-colors font-semibold hover:bg-purple-500  active:bg-purple-500"
      {...props}
    >
      { isLoading && <Spinner />}
      {children}
    </button>
  );
};
