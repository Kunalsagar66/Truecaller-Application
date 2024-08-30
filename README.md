I designed and developed a REST API for a web/mobile application that provides functionalities similar to popular caller identification apps. 

The API enables users to:
    Identify Spam Numbers: The API checks if a given phone number is marked as spam or has been reported as such by other users. It provides a spam likelihood score, helping users decide whether to answer unknown calls.
    Find People by Phone Number: Users can search for a person's name using their phone number. The API retrieves and displays matching results, ensuring accuracy and privacy.



To Run the Django project, first install the requirement.txt file by below command
    (env)$ pip install -r requirements.txt

After succesfully installing the packages run command to start the django server:
    (env)$ cd project
    (env)$ python manage.py runserver

Admin portal user creds:
    username: admin 
    password: admin

Below are the required API's:

1. Register User API:
This API registers a unique new user and return error message if user is already present with same username/phone_number

url: http://127.0.0.1:8000/account/register
method: POST
data: {
        "username":"john",
        "name":"John Bell",
        "phone_number":6547891230,
        "email":"",
        "password":"12345"
    }

2.Get User Token API:
This API creates token for particular user by taking username and password in data, this token is used for further authentication.

url: http://127.0.0.1:8000/account/get-user-token
method: POST
data: {
        "username":"john",
        "password":"12345"
    }

3. Verify Token API:
This API is a get API which takes token in header and return if the token is valid or not.

url: http://127.0.0.1:8000/account/verify-token
method: GET
headers: 
    key:"token", value:"string"

4. Mark phone numbers spam API:
This is will takes token as header and verify the token and if token is verified then only mark the given phone_number as spam in the global database.

url: http://127.0.0.1:8000/contact/mark-spam
method: POST
headers: 
    key:"token", value:"string"
data: {
        "phone_number":"7896541230"
    }

5. Search user details by NAME:
This API is will takes token as header and verify the token and if token is verified then only return the searched user from the database

url: http://127.0.0.1:8000/contact/search-name
method: GET
headers: 
    key:"token", value:"string"
param:
    key:"name", value:"string"

6. Search by phone number:
This is will takes token as header and verify the token and if token is verified then only provide the matching results with user searched phone_number

url: http://127.0.0.1:8000/contact/search-number
method: GET
headers: 
    key:"token", value:"string"
param:
    key:"phone_number", value:"int"

