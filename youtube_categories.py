import requests

def api_request(api_key):
    request_url = f"https://www.googleapis.com/youtube/v3/videoCategories?part=snippet&regionCode=US&key={api_key}"
    request = requests.get(request_url)
    request_json = request.json()

    category = []
    category.append("categoryId" + "," + "category_Name")
    for i in range(32):
        category.append(request_json['items'][i]['id'] + "," + request_json['items'][i]['snippet']['title'])

    with open(f"categories.csv", "w+", encoding='utf-8') as file:
        for row in category:
            file.write(f"{row}\n")


api_request('')
