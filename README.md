# Chatbot


## Description
The NIKLES Chatbot is an AI-powered knowledge-based chatbot application designed to provide information about NIKLES. It leverages natural language processing techniques to understand user queries and retrieve relevant information from a knowledge base.

## "Why?" 
The goal of the NIKLES Chatbot is to enhance customer experience by providing quick and accurate responses to inquiries about NIKLES products, history, technologies, luxury finishes, news, and more. By automating responses to common questions, the chatbot aims to streamline customer support and improve overall satisfaction.


## Project Structure
```bash
CHATBOT/
├── app/
│ ├── app.py
│ └── main.py
├── chroma_db/
├── data/
│ ├── InformationFromWeb.pdf
│ └── Warranty.pdf
├──- models/
│ ├── dataprocessor.py
│ ├── get_from_chromaDB_and_general_Chat.py
│ ├── get_from_mysqlDB.py
│ ├── scraper1.py
│ ├── scraper2.py
│ └── userlib.py
├── .env
├── .gitignore
├── requirements.txt
└── README.md
```

## Setup Instructions

1. Clone the repository and navigate to the project directory.

2. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

3. Run the FastAPI:
    ```bash
    fastapi dev .\app\main:app --reload
    ```

4. Run the Streamlit frontend:
    ```bash
    streamlit run app.py
    ```
6. Open the frontend in your browser and ask your questions.

## Notes
- Adjust the `.env` file if needed to point to your database.
- Make sure your mysql server is up and running and adjust the database 

