# QnAChatBot Documentation

## Features

- **Document Upload**: Users can upload PDF/txt files which are then processed and indexed.
- **Contextual Chatbot**: Interact with a chatbot that provides answers based on the uploaded documents.
- **Session Management**: Each user session maintains its own document context.
- **Clear Session**: Users can clear their session data to upload new documents or reset the chatbot.

---

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/Sonugupta2001/QnAChatBot.git
cd QnAChatBot
```

### 2. Create and Activate a Virtual Environment

```bash
python3.12 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Set Up Environment Variables

Create a `.env` file in the project's root directory and add the following:

```env
SECRET_KEY=your_django_secret_key
OPENAI_API_KEY=your_openai_api_key
HUGGINGFACEHUB_API_TOKEN=your_huggingface_api_token
```

### 5. Apply Migrations

```bash
python manage.py migrate
```

### 6. Collect Static Files

```bash
python manage.py collectstatic
```

### 7. Run the Development Server

```bash
python manage.py runserver
```

---

## API endpoints
- GET /
- POST /upload/
- GET /chat/
- POST /chat/
- POST /clear_session/

---

## Configuration

### `settings.py`

The `settings.py` file contains all the configuration for the Django project. Key configurations include:

- **Environment Variables**: Managed using `python-dotenv` to keep sensitive information secure.
- **Installed Apps**:
    - `chatBot`: The main application.
    - `material` and `material.frontend`: For Material Design components.
- **Database**: Configured to use SQLite for simplicity. For production, consider using PostgreSQL or another robust database system.
- **Static and Media Files**:
    - **Static**: Served from `/static/` URL.
    - **Media**: Uploaded files are stored in the `media/` directory.
- **API Keys**:
    - `OPENAI_API_KEY`: For OpenAI's language models.
    - `HUGGINGFACEHUB_API_TOKEN`: For Hugging Face models (optional).

---

## Key Components

### Settings

#### `QnAChatBot/QnAChatbot/settings.py`

Key settings include:

- **Environment Variables**: Loaded using `dotenv`.
- **Installed Apps**: Includes default Django apps and third-party apps like `material`.
- **Middleware**: Standard Django middleware stack.
- **Templates**: Configured to use Django templates with directories specified.
- **Database**: Uses SQLite by default.
- **Static and Media Files**: Configured paths for serving static and media files.
- **API Keys**: OpenAI and Hugging Face tokens are loaded from environment variables.


### Views

#### `QnAChatBot/chatBot/views.py`

Handles the core functionality of the chatbot application.

- **Index View**: Renders the homepage where users can upload documents.
- **Upload Document View**:
    - Handles PDF/txt uploads.
    - Processes the PDF/txt into text chunks.
    - Generates embeddings using Hugging Face models.
    - Stores embeddings using FAISS for efficient retrieval.
    - Saves the vector store path in the user session.
- **Chat View**:
    - Processes user queries.
    - Retrieves relevant documents based on the query.
    - Uses OpenAI's GPT-3.5-Turbo model to generate answers.
    - Returns responses in JSON format for asynchronous updates.
- **Clear Session View**: Flushes the user session to clear uploaded documents and related data.


### Templates

#### `QnAChatBot/chatBot/templates/chatBot/index.html`

The homepage template where users can upload PDF documents. It includes:

- A form for uploading PDF/txt files.
- A button to clear the current session.
- Display of success or error messages using Django's messaging framework.
- Utilizes Materialize CSS for styling.

#### `QnAChatBot/chatBot/templates/chatBot/chat.html`

The chat interface template where users can interact with the chatbot. It includes:

- A chat box to display the conversation.
- An input field for users to enter their questions.
- JavaScript to handle asynchronous submission of queries and dynamic updating of the chat box.
- Buttons to navigate back to the upload page.

---

## API Integration

### OpenAI Integration

- **Library**: Utilizes OpenAI's `ChatOpenAI` model (`gpt-3.5-turbo`) for generating responses.
- **Configuration**:
    - The OpenAI API key is loaded from the `.env` file.
    - Model parameters such as `temperature` and `model_name` are set in `views.py`.

### Hugging Face Integration

- **Embeddings**: Uses `HuggingFaceEmbeddings` with the `all-MiniLM-L6-v2` model to generate text embeddings.
- **Vector Store**: Employs FAISS (Facebook AI Similarity Search) to store and retrieve embeddings efficiently.
- **API Token**: Optionally, a Hugging Face API token can be provided for enhanced functionalities.
---

## License

This project is licensed under the [MIT License](LICENSE).
