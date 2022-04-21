import requests
import json
def postapi():
    api_url = "http://fit-lab.vlu.edu.vn:6789/add_one"
    todo = {'_id': 17, 'title': "todo title call api 12", 'body': "todo body api "}
    headers =  {"Content-Type":"application/json"}
    response = requests.post(api_url, data=json.dumps(todo), headers=headers)
    print (response.json())
    print(response.status_code)
def getapi():
    api_url = "http://fit-lab.vlu.edu.vn:6789/get_todo/17"
    response = requests.get(api_url)
    result = response.json()
    statuscode = response.status_code
    headers = response.headers["Content-Type"]
    print(result)
    print('status code: ', statuscode)
    print('headers: ', headers)
if __name__ == "__main__":
    getapi()
    #postapi()