import os

def git_tool():
    """
    Enhanced terminal interface for Git commands:
    - Manages all projects within C:\dev.
    - Supports repository creation, selection, branch creation, committing, merging, and pushing.
    """
    dev_folder = "C:\\dev"

    while True:
        print("\nGit Tool Options:")
        print("1. Initialize Git in a Folder")
        print("2. Create a New Repository")
        print("3. Select an Existing Repository")
        print("4. Create a New Branch")
        print("5. Commit Changes")
        print("6. Merge a Branch")
        print("7. Push to Remote Repository")
        print("8. Show Git Status")
        print("9. Exit")

        choice = input("Choose an option (1-9): ").strip()

        if choice == "1":
            folder_path = input(f"Enter folder path (default: {dev_folder}): ").strip() or dev_folder
            os.chdir(folder_path)
            os.system("git init")
            print(f"Initialized Git in {folder_path}.")
        elif choice == "2":
            repo_name = input("Enter new repository name: ").strip()
            repo_path = os.path.join(dev_folder, repo_name)
            os.makedirs(repo_path, exist_ok=True)
            os.chdir(repo_path)
            os.system("git init")
            print(f"Repository '{repo_name}' created at {repo_path}.")
        elif choice == "3":
            # List all directories in dev_folder
            repos = [d for d in os.listdir(dev_folder) if os.path.isdir(os.path.join(dev_folder, d))]
            if not repos:
                print(f"No repositories found in {dev_folder}.")
            else:
                print("\nAvailable Repositories:")
                for idx, repo in enumerate(repos, start=1):
                    print(f"{idx}. {repo}")
                try:
                    repo_choice = int(input("Select a repository by number: ").strip())
                    if 1 <= repo_choice <= len(repos):
                        selected_repo = repos[repo_choice - 1]
                        repo_path = os.path.join(dev_folder, selected_repo)
                        os.chdir(repo_path)
                        print(f"Switched to repository '{selected_repo}' at {repo_path}.")
                    else:
                        print("Invalid selection. Please try again.")
                except ValueError:
                    print("Invalid input. Please enter a number.")
        elif choice == "4":
            branch_name = input("Enter new branch name: ").strip()
            os.system(f"git checkout -b {branch_name}")
            print(f"Branch '{branch_name}' created.")
        elif choice == "5":
            commit_message = input("Enter commit message: ").strip()
            os.system("git add .")
            os.system(f'git commit -m "{commit_message}"')
            print("Changes committed.")
        elif choice == "6":
            branch_to_merge = input("Enter branch name to merge: ").strip()
            os.system(f"git merge {branch_to_merge}")
            print(f"Branch '{branch_to_merge}' merged.")
        elif choice == "7":
            os.system("git push")
            print("Changes pushed to remote repository.")
        elif choice == "8":
            os.system("git status")
        elif choice == "9":
            print("Exiting Git Tool.")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    git_tool()