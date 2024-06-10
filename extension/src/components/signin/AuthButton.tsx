import React from 'react';
import { Button } from '../ui/button';

interface AuthButtonProps {
  brand: string;
  imgUrl: string;
}

export const AuthButton: React.FC<AuthButtonProps> = ({
  brand,
  imgUrl,
}) => {
  return (
    <Button className="w-full border-gray-200 hover:border-gray-200 focus:border-gray-200 shadow-md font-semibold text-gray-600 bg-white hover:bg-gray-200">
      <img
        className="w-5 h-5 mr-2"
        src={imgUrl}
        alt={`${brand} icon`}
      />
      Continue with {brand}
    </Button>
  );
};
