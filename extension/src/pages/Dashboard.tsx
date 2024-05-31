import React from 'react';
import { mockFolders } from '@/lib/mocks';
import { FolderCard } from '@/components/dashboard/FolderCard';
import Header from '@/components/dashboard/Header';
import { AddFolder } from '@/components/dashboard/AddFolder';
import { Tabs } from '@/components/dashboard/Tabs';
import { Profile } from '@/components/dashboard/Profile';
import { DropdownMenuIcon } from '@radix-ui/react-icons';
import { Button } from '@/components/ui/button';

function Dashboard() {
  const [tab, setTab] = React.useState<'folders' | 'settings'>('folders');

  return (
    <div className="w-full h-full flex flex-col bg-customWhite space-y-5">
      {tab === 'folders' ? (
        <div className="w-full h-full flex flex-col space-y-5">
          <Header title="Folders" />
          <div className="w-full flex flex-col flex-grow items-center justify-center space-y-2">
            {mockFolders.map((folder) => (
              <FolderCard key={folder.name} {...folder} />
            ))}
          <AddFolder />
          </div>
        </div>
      ) : (
        <div className="w-full h-full flex flex-col items-center justify-center space-y-5">
          <Header title="Settings" />
          <div className="w-full flex flex-col flex-grow items-center justify-center space-y-2">
            <Profile name="Pax Nguyen" />
            <div className="w-full flex flex-col items-center justify-center space-y-2">
              <div className="w-3/4 justify-between flex items-center flex-wrap p-4 rounded-xl shadow bg-white transition-colors hover:bg-gray-100 border border-gray-200 text-base text-gray-800 font-semibold">
                <div className="w-full flex flex-wrap items-center gap-5">
                  <h4 className="w-4/5 truncate text-gray-800 font-semibold">Devices</h4>
                  <DropdownMenuIcon className="w-4 h-4 text-gray-500" />
                </div>
              </div>
              <div className="w-3/4 justify-between flex items-center flex-wrap p-4 rounded-xl shadow bg-white transition-colors hover:bg-gray-100 border border-gray-200 text-base text-gray-800 font-semibold">
                <div className="w-full flex flex-wrap items-center gap-5">
                  <h4 className="w-4/5 truncate text-gray-800 font-semibold">Access</h4>
                  <DropdownMenuIcon className="w-4 h-4 text-gray-500" />
                </div>
              </div>
              <Button className="w-3/4 bg-transparent border-0 text-center font-semibold text-red-500">Logout</Button>
            </div>
          </div>
        </div>
      )}
      <Tabs tab={tab} setTab={setTab} />
    </div>
  );
}

export default Dashboard;
