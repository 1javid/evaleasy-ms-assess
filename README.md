# EvalEasy MS Assess

This microservice is designed to handle image processing tasks. It provides an API endpoint to upload an image and process it using an external service. The microservice is built using Django and can be easily integrated into larger systems.

## Features

- Upload images via a POST request
- Process images using an external service
- Return student exam report as a JSON response

## Endpoints

### `POST /api/process_image/`

- **Description**: Upload an image to be processed.
- **Request**: 
  - Method: `POST`
  - Content-Type: `multipart/form-data`
  - Body: 
    - `image`: The image file to be processed.
- **Response**:
  - Status: `200 OK` if successful, `400 Bad Request` if no image is provided, `405 Method Not Allowed` if the request method is not POST.
  - Body: JSON response from the external service.

## Requirements

- Python 3.8+
- Django 5.1.5
- requests

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/1javid/evaleasy-ms-assess.git
    cd evaleasy-ms-assess/ms_assess
    ```

2. Install the dependencies:
    ```sh
    pip install -r requirements.txt
    ```

3. Apply the migrations:
    ```sh
    python manage.py migrate
    ```

4. Run the development server:
    ```sh
    python manage.py runserver
    ```

## Usage

1. Start the Django development server:
    ```sh
    python manage.py runserver
    ```

2. Use a tool like `curl` or Postman to send a POST request to the `/api/process_image/` endpoint with an image file.

Example using `curl`:
```sh
curl -X POST -F "image=@path/to/your/image.jpg" http://127.0.0.1:8000/api/process_image/