import requests
import os 
import concurrent.futures


class Repository():
    def __init__(self,repo_owner):
        self.repo_owner = repo_owner


    def create_folder(self):
        folder_name = input('tape the folder name: ')

        if not os.path.exists(folder_name):
            os.makedirs(folder_name)

        return folder_name
    

    def get_private_repository(self):
        folder_name = self.create_folder()
        repo_name = input("Please enter the name of the repository:")
        token = input('Please note that authentication tokens are required to access private repositories: ')

        check_owner = requests.get(f'https://api.github.com/users/{self.repo_owner}')
        
        if check_owner.status_code == 404 :
            print('We couldnt find a GitHub user with the provided username. Please ensure that the username was entered correctly and try again.')
        else: 
            url = f"https://api.github.com/repos/{self.repo_owner}/{repo_name}/contents"

            header = {
                'Authorization': f'Token {token}'
            }

            response = requests.get(url, headers=header)

            file_data = response.json()

            if 'download_url' in file_data and file_data['download_url'] is not None:
                file_name = file_data['name']
                file_url = file_data['download_url']
            
                
            
                if response.status_code == 200:
                    content = response.content
                    with open(os.path.join(folder_name, file_name), 'wb') as f:
                        f.write(content)
                    print(f'{file_name} has been downloaded.')
                else:
                    print(f'Error downloading {file_name}: {response.status_code}')
            else:
                print(f'Skipping file: {file_data.get("name")} (No valid download URL)')
    

        


    def get_public_repository(self):
        folder_name = self.create_folder()
        repo_name = input("Please enter the name of the repository:")

        owner = requests.get(f'https://api.github.com/users/{self.repo_owner}')
            
        url = f"https://api.github.com/repos/{self.repo_owner}/{repo_name}/contents"

        response = requests.get(url)

        file_data = response.json()

        for file_item in file_data:
            if 'download_url' in file_item and file_item['download_url'] is not None:
                file_name = file_item['name']
                
                if response.status_code == 200:
                    content = requests.get(file_item['download_url']).content
                    with open(os.path.join(folder_name, file_name), 'wb') as f:
                        f.write(content)
                    print(f'{file_name} has been downloaded.')
                else:
                    print(f'Error downloading {file_name}: {response.status_code}')
            else:
                print(f'Skipping file: {file_item.get("name")} (No valid download URL)')





r = Repository('Saikaisiham')

public_or_private = input('Public or Private? ')


if public_or_private == 'public' :
    r.get_public_repository()

else :
    r.get_private_repository()