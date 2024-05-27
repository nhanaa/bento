import Layout from "./Layout";
import { Header } from "@/components/folderView/Header";
import { mockFolder } from "@/lib/mocks";
import { SummaryView } from "@/components/folderView/SummaryView";
import { SearchView } from "@/components/folderView/SearchView/index";

const FolderView: React.FC = () => {
  return (
    <Layout>
      <div className="flex w-full h-full flex-col gap-5 p-10">
        <Header emoji={mockFolder.emoji} name={mockFolder.name} />
        <div className="flex w-full h-5/6 flex-wrap justify-between">
          <SummaryView description={mockFolder.description} />
          <SearchView items={mockFolder.items} />
        </div>
      </div>
    </Layout>
  );
};

export default FolderView;
