import { Button } from "@/components/Button";
import { Card } from "@/components/landing/Card";
import React from "react";
import { useNavigate } from "react-router-dom";

export const Landing: React.FC = () => {
  const navigate = useNavigate();

  const handleGetStarted = () => {
    navigate("/auth");
  };
  return (
    <div className="h-screen w-screen flex flex-col justify-center text-center items-center">
      <div className="flex flex-col gap-2 justify-center w-full h-1/2 items-center bg-customViolet-100 border-b border-gray-200">
        <h1 className="font-bold text-3xl mb-4 text-gray-800">
          Bento: Your Digital Organizer
        </h1>
        <Button onClick={handleGetStarted}>Get started</Button>
      </div>
      <div className="h-1/2 w-full py-10">
        <div className="flex flex-wrap justify-center gap-5">
          <Card
            emoji="📁"
            title="Create custom folders"
            description="Save what matters to you by creating folders with personalized titles, tags, and descriptions."
          />
          <Card
            emoji="🤖"
            title="Stay organized"
            description="Bento organizes your browsing history, downloads, and screenshots into your folders, renaming them for better readability."
          />
          <Card
            emoji="📝"
            title="AI-powered enhancements"
            description="Refresh your memory with our AI-generated summaries and chatbot, and further your discovery with our AI-generated recommendations."
          />
          <Card
            emoji="📱"
            title="Accessible anywhere"
            description="Manage your digital life from any device, anytime."
          />
        </div>
      </div>
    </div>
  );
};
