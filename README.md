# geolocation-api
This is the application created as an interview assignment for Sofomo. Below one will find some information
to get the high-level overview about the app:

- The app is available under [this url](https://sofomo-geolocation-api.herokuapp.com/)
- It consists of database client, and the actual API
- Using the API is the correct way to communicate with the database
- API is secured by JWT token
- The dependencies are managed by `poetry`
- The application is packed into Docker container

## Table of contents
1. Usage
2. Availability
3. How to test
4. Running the app locally

### 1. Usage
Before sending requests on all the endpoints, one must be authorized by obtaining JWT token.
To obtain JWT token one must first send the request under `/token` URL. If the credentials for test user 
are correct then API will respond with JWT Token. Test user credentials are stored in the config file.

After obtaining JWT token and putting it to authorization header of the request, one is good to go and use
the application and send the requests.

### 2. Availability
The application is deployed as Heroku App, and is available under following [URL](https://sofomo-geolocation-api.herokuapp.com/). To view supported endpoints
and more detailed information please see the [documentation](https://sofomo-geolocation-api.herokuapp.com/docs).

### 3. How to test
The repository comes with Postman collection that was used during the development. Here one can find example
requests on different endpoints.

### 4. Running the app locally
To run the application locally, one will need the environment file with the database credentials.
Because of the security issues this file does not come with Git repository by default (however in the 
repository one can find the template environment file that must be filled with correct credentials).
The environment file with credentials will be sent via email.

In case of creating custom environmen file, please note that the file must be named `local.env` and placed in `env/` directory of the application.

After that, the only command needed to run the application is `docker-compose up`.
