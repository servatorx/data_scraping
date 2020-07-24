
import requests

main_link = 'https://api.github.com/users/servatorx/repos'


response = requests.get(main_link)
data = response.json()


print(f"Пользователь: {data[0]['full_name'].split('/')[0]}")
print("Репозитории:")
for i in data:
    print(i['full_name'].split("/")[1])
