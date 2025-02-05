# EvalEasy MS Assess

This microservice is designed to handle image processing tasks for student assessments. It provides an API endpoint to upload an image of an answer sheet, processes it using an external service, and returns the assessment results. The microservice is built using Django and can be easily integrated into larger systems.

## Features

- Upload images via a POST request
- Process images using an external image processing service
- Retrieve correct answers from a test microservice
- Compare student answers with correct answers
- Compute and return the total score
- Save assessment results to the database

## Endpoints

- `POST /api/submit-assessment/`: Upload an image of an answer sheet and process it to get the assessment results.

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
    python manage.py runserver 8002
    ```

## Usage

1. Start the Django development server:
    ```sh
    python manage.py runserver 8002
    ```

2. Use a tool like `curl` or Postman to send a POST request to the `/api/process_image/` endpoint with an image file.

Example using `curl`:
```sh
curl -X POST -F "image=@path/to/your/image.jpg" http://127.0.0.1:8000/api/process_image/