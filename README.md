# NeoSeek

The new and improved version of Seek Portal that integrates GenAI features.

## GenAI features:

1. Summaries of Weeks and Lectures
2. QnA generation for instructors
3. GenAI chat with course context for student and instructor

## Technologies Used

### Frontend

- Nuxt
  - VueJS
    - PrimeVue
    - Pinia
- Markdown It

### Backend

- Flask
  - Flask SQL Alchemy
  - Flask Migrate
  - Flask CORS
  - Flask RestX
  - Flask JWT Extended
- Google Generative AI
- Werkzeug

### Testing

- Postman / Insomnia
- PyTest
- requests

## Development

To develop, run the backend and the frontend server:

### Backend

- Go to `backend` folder
- Execute `./run`, it will
  - create virtual environment
  - copy env file from sample
  - activate venv
  - install requirements
  - run flask server

### Frontend

- Go to `frontend/nuxt-app` folder
- Run `npm i` to install dependencies
- Run `npm run dev` to run development server

### Testing

- Go to `testing` folder
- Run the `./run`, it will
  - create virtual environment
  - activate venv
  - install requirements
  - run tests using pytest
