import os

class LocalFileAccess():
    @classmethod
    def print_downloads_contents(folder_name):
        # Get the path to the user's Downloads directory
        folder_path = os.path.join(os.path.expanduser('~'), folder_name)

        # Check if the path exists and is a directory
        if os.path.exists(folder_path) and os.path.isdir(folder_path):
            # List all files and directories in the Downloads directory
            contents = os.listdir(folder_path)
            
            if contents:
                print(f"Contents of {folder_name} directory:")
                for item in contents:
                    print(item)
            else:
                print(f"{folder_name} is empty.")
        else:
            print(f"{folder_name} directory does not exist.")