import React from 'react'
import { Avatar, AvatarFallback } from '../ui/avatar';

interface AvatarProps {
  name: string;
}

export const Profile = ({ name }: AvatarProps) => {
  return (
    <div className="flex flex-col items-center justify-center gap-2">
      <Avatar className="w-8 h-8 bg-customViolet text-white">
        <AvatarFallback>
          {name.split(' ').map(word => word.charAt(0).toUpperCase()).join('')}
        </AvatarFallback>
      </Avatar>
      <h4 className="text-base font-semibold">{name}</h4>
    </div>
  );
};
