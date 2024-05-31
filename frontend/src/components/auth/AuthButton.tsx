import React from "react";

interface AuthButtonProps {
  brand: string;
  imgUrl: string
}

function capitalize(word: string): string {
  return word.charAt(0).toUpperCase() + word.slice(1);
}

export const AuthButton: React.FC<AuthButtonProps> = ({ brand, imgUrl }) => {
  return (
    <div className="flex flex-row items-center text-gray-500 bg-white hover:bg-gray-50 transition-colors font-medium border border-gray-200 rounded-xl shadow px-5 py-3 gap-5">
      <img className="w-4 h-4" src={imgUrl} />
      Continue with {capitalize(brand)}
    </div>
  );
};
