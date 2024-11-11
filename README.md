# File Manager Web Service

A Flask web service to upload files and access various file-based functionalities.

## Features
- **Upload File**: Upload a text file to be stored in MongoDB.
- **Random Line**: Retrieve a random line from a file.
- **Random Line Backward**: Retrieve a random line in reverse.
- **Longest Lines**: Get the longest lines from all files or a single file.

## Setup

1. Clone the repository.
2. Install [Docker](https://docs.docker.com/get-docker/) and [Docker Compose](https://docs.docker.com/compose/install/) if not already installed.
3. Run `docker-compose up --build` to start the services.
4. Access the endpoints at `http://localhost:5000`.

## Endpoints

- **POST /file/upload**: Uploads a text file.
  - **Request**: Requires a file upload in `multipart/form-data` format.
  - **Response**:
    - **201 Created**: File uploaded successfully.
    - **400 Bad Request**: File already exists or there was an issue with the upload.
  - **Example**:
    ```bash
    curl -X POST -F 'file=@/path/to/yourfile.txt' http://localhost:5000/file/upload
    ```

- **GET /file/random**: Returns a random line from a file.
  - Accepts `text/plain`, `application/json`, or `application/xml` response format.
  
- **GET /file/random-backward**: Returns a random line in reverse.

- **GET /file/longest**: Returns the longest lines from all files or a single file.
  - **Query Parameters**:
    - `number`: Number of longest lines to return (default is 100).
    - `single`: If `true`, retrieves lines from a single file (default is all files).
  - **Example**:
    ```bash
    curl http://localhost:5000/file/longest?number=20&single=true
    ```

This setup should help you quickly test and explore the functionality of the File Manager Web Service.
