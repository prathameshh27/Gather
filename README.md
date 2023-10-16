# Gather - Django REST API

Gather is a Django-based REST API for managing users and meetings. This API provides endpoints to create, update, describe, list, and delete users and meetings. It is useful for applications that require user and meeting management. This README provides a comprehensive guide to the API, its endpoints, and how to interact with it using Postman.

## Summary

- [Getting Started](#getting-started)
- [Installation](#installation)
- [API Endpoints](#api-endpoints)
  - [User Operations](#user-operations)
    - [Create a User](#create-a-user)
    - [Update User](#update-user)
    - [Describe User](#describe-user)
    - [List Users](#list-users)
  - [Meeting Operations](#meeting-operations)
    - [Create a Meeting](#create-a-meeting)
    - [Update Meeting](#update-meeting)
    - [Describe Meeting](#describe-meeting)
    - [List Meetings](#list-meetings)
    - [Delete Meeting](#delete-meeting)
    - [Manage Users (Add or Remove)](#manage-users-add-or-remove)
- [Testing with Postman](#testing-with-postman)
- [Author](#author)
- [License](#license)

## Getting Started

These instructions will help you understand the available API endpoints and how to use them.

### Prerequisites

- Python 3.x
- Django
- Django REST framework
- Postman (for testing the API)

## Installation

1. **Clone this repository to your local machine.**

   ```shell
   git clone https://github.com/prathameshh27/Gather.git
   ```

2. **Activate the virtual environment to isolate dependencies:**
   
   ```shell
   cd Gather

   source env/bin/activate   # On macOS/Linux
   env\Scripts\activate      # On Windows
   ```

3. **Install the required Python packages (Not required):**

Navigate to the project folder and install the dependencies using pip:

```shell
pip install -r requirements.txt     # skip
```

4. **Create a super user (Mandatory)**
    ```shell
    python manage.py createsuperuser
    ```

5. **Run the Django application:**

Start the Django development server:

```shell
python manage.py runserver
```
The application will be accessible at http://127.0.0.1:8000/.

6. **Setup user tokens:**
login and go to the tokens page: http://localhost:8000/admin/authtoken/tokenproxy/  
Generate a token for each user you create.

## API Endpoints
This section describes the available API endpoints, their purposes, and the expected input and output data for each operation.

### User Operations  
#### ** Please note that on SuperUsers can access the User APIs **
  
**Create a User**
- HTTP Method: POST
- Endpoint: /api/v1/user/create
- Headers: Authorization:Token user_token   (from Installation step 6)
- Description: Create a new user by providing user details in the request body.

#### ** Please follow Installation - step 6 to setup a token **

***Input Data (Request Body):***

```json
{
    "username": "user_username",
    "first_name": "user_first_name",
    "last_name": "user_last_name",
    "email": "user_email"
}
```

***Output Data (Response):***

```json
{
    "id": "['unique_user_id']"
}
```

**Update User**
- HTTP Method: PATCH
- Endpoint: /api/v1/user/update
- Headers: Authorization:Token user_token   (from Installation step 6)
- Description: Update an existing user's information by specifying the user ID and updated details in the request body.

***Input Data (Request Body):***  
Use required fields only.
```json
{
    "id": "existing_user_id",
    "username": "new_username",
    "first_name": "new_first_name",
    "last_name": "new_last_name",
    "email": "new_email"
}
```

***Output Data (Response):***

```json
{
    "id": "existing_user_id",
    "username": "new_username",
    "first_name": "new_first_name",
    "last_name": "new_last_name",
    "display_name": "new_first_name new_last_name",
    "email": "new_email",
    "date_joined": "existing join_date"
}
```

**Describe User**
- HTTP Method: GET
- Endpoint: /api/v1/user/describe
- Headers: Authorization:Token user_token   (from Installation step 6)
- Description: Retrieve details of a specific user by providing the user ID in the request.

***Input Data (Request Body):***

```json
{
    "id": "user_id"
}
```

***Output Data (Response):***

```json
{
    "id": "user_id_to_retrieve",
    "username": "user_username",
    "first_name": "user_first_name",
    "last_name": "user_last_name",
    "display_name": "first_name last_name",
    "email": "user_email",
    "date_joined": "user_join_date"
}
```

**List Users**
- HTTP Method: GET
- Endpoint: /api/v1/user/list
- Headers: Authorization:Token user_token   (from Installation step 6)
- Description: List all users in the system.

***Output Data (Response):***

```json
[
    {
        "id": "user_id_1",
        "username": "username_1",
        "first_name": "first_name_1",
        "last_name": "last_name_1",
        "display_name": "first_name_1 last_name_1",
        "email": "email_1",
        "date_joined": "join_date_1"
    },
    {
        "id": "user_id_2",
        "username": "username_2",
        "first_name": "first_name_2",
        "last_name": "last_name_2",
        "display_name": "first_name_2 last_name_2",
        "email": "email_2",
        "date_joined": "join_date_2"
    },
    ...
]
```

## Meeting Operations

**Create a Meeting**
- HTTP Method: POST
- Endpoint: /api/v1/meeting/create
- Headers: Authorization:Token user_token   (from Installation step 6)
- Description: Create a new meeting by providing meeting details in the request body.

***Input Data (Request Body):***

```json
{
    "title": "meeting_title",
    "description": "meeting_description",
    "created_by": "meeting_creator",
    "attendees": ["username_1", "username_2", ...],
    "starts_at": "meeting_start_datetime",
    "ends_at": "meeting_end_datetime"
}
```

***Output Data (Response):***

```json
{
    "id": "unique_meeting_id",
    "unavailable_users": {
        "users": ["username_1", "username_2"],
        "message": "Some users might not be added due to scheduling conflict"
    }
}
```

**Update Meeting**

- HTTP Method: PATCH
- Endpoint: /api/v1/meeting/update
- Headers: Authorization:Token user_token   (from Installation step 6)
- Description: Update an existing meeting's information by specifying the meeting ID and updated details in the request body.

***Input Data (Request Body):***

```json
{
    "id": "existing_meeting_id",
    "title": "new_meeting_title",
    "description": "new_meeting_description",
    "attendees": ["username_1", "username_2", ...],
    "starts_at": "new_meeting_start_datetime",
    "ends_at": "new_meeting_end_datetime"
}
```

***Output Data (Response):***

```json
{
    "id": "existing_meeting_id",
    "title": "new_meeting_title",
    "description": "new_meeting_description",
    "created_by": "meeting_creator",
    "attendees": ["username_1", "username_2", ...],
    "starts_at": "new_meeting_start_datetime",
    "ends_at": "new_meeting_end_datetime",
    "unavailable_users": {
        "users": [],
        "message": "Some users might not be added due to scheduling conflict"
    }
}
```

**Describe Meeting**

- HTTP Method: GET
- Endpoint: /api/v1/meeting/describe
- Headers: Authorization:Token user_token   (from Installation step 6)
- Description: Retrieve details of a specific meeting by providing the meeting ID in the request.

***Input Data (Request Body):***

```json
{
    "id": "meeting_id"
}
```

***Output Data (Response):***

```json
{
    "id": "meeting_id_to_retrieve",
    "title": "meeting_title",
    "description": "meeting_description",
    "created_by": "meeting_creator",
    "attendees": ["username_1", "username_2", ...],
    "starts_at": "meeting_start_datetime",
    "ends_at": "meeting_end_datetime"
}
```

**List Meetings**
- HTTP Method: GET
- Endpoint: /api/v1/meeting/list
- Headers: Authorization:Token user_token   (from Installation step 6)
- Description: List all meetings in the system.

***Output Data (Response):***

```json
[
    {
        "id": "meeting_id_1",
        "title": "meeting_title_1",
        "description": "meeting_description_1",
        "created_by": "meeting_creator_1",
        "attendees": ["username_1", "username_2", ...],
        "starts_at": "meeting_start_datetime_1",
        "ends_at": "meeting_end_datetime_1"
    },
    {
        "id": "meeting_id_2",
        "title": "meeting_title_2",
        "description": "meeting_description_2",
        "created_by": "meeting_creator_2",
        "attendees": ["username_1", "username_2", ...],
        "starts_at": "meeting_start_datetime_2",
        "ends_at": "meeting_end_datetime_2"
    },
    ...
]
```

**Delete Meeting**
- HTTP Method: DELETE
- Endpoint: /api/v1/meeting/delete
- Headers: Authorization:Token user_token   (from Installation step 6)
- Description: Delete a specific meeting by providing the meeting ID in the request.

***Input Data (Request Body):***

```json
{
    "id": "meeting_id"
}
```

***Output Data (Response):***

```json
{
    "message": "Meeting deleted."
}
```

**Manage Users (Add or Remove)**
- HTTP Method: POST
- Endpoint: /api/v1/meeting/manage_users
- Headers: Authorization:Token user_token   (from Installation step 6)
- Description: Add or remove attendees from a specific meeting by providing the meeting ID, a list of attendees, and the operation as "add" or 
"remove" in the request body.

***Input Data (Request Body):***

```json
{
    "id": "meeting_id",
    "attendees": ["username_1", "username_2", ...],
    "operation": "add"  // or "remove"
}
```

***Output Data (Response):***

```json
{
    "message": "Attendees added/removed successfully."
}
```

## Testing with Postman
To test the API endpoints, you can use the provided Postman collection. Import the collection into Postman, and you can easily interact with your Django application by sending requests to the defined endpoints.

## Author
Prathamesh Pavnoji
