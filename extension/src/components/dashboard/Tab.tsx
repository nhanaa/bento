interface TabButtonProps {
  isActive: boolean;
  onClick: () => void;
  icon: React.ReactNode;
}

export const Tab = ({ isActive, onClick, icon }: TabButtonProps) => {
  return (
    <button
      onClick={onClick}
      className={`w-1/2 flex items-center justify-center py-2 px-4 rounded-none transition-colors border-0 focus:outline-none ${
        isActive
          ? "border-t-2 border-customViolet"
          : "border-t-2 border-transparent"
      }`}
    >
      {icon}
    </button>
  );
};
