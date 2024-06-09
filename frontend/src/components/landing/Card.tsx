export const Card = ({ emoji, title, description }) => {
  return (
    <div className="w-1/5 flex items-center flex-col gap-5 p-2 py-5 rounded-xl transition-colors border border-gray-200 hover:bg-gray-50 shadow">
      <div className="flex flex-col gap-1">
        <span className="text-2xl">{emoji}</span>
        <span className="text-sm  font-semibold">{title}</span>
      </div>
      <span className="text-xs text-gray-500">{description}</span>
    </div>
  );
};
