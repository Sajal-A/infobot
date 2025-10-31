# Echo – An InfoBot

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100%2B-009688.svg)](https://fastapi.tiangolo.com/)
[![LangChain](https://img.shields.io/badge/LangChain-Latest-green.svg)](https://www.langchain.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

A powerful Retrieval-Augmented Generation (RAG) chatbot designed to provide real-time organizational knowledge assistance. Echo streamlines employee onboarding and knowledge management by enabling intelligent document search and conversational AI capabilities.

## 🌟 Features

- **Intelligent RAG Architecture**: Combines retrieval and generation for accurate, context-aware responses
- **Real-time Knowledge Assistance**: Instant access to organizational information through conversational interface
- **Dynamic Document Management**: Upload, index, and retrieve documents seamlessly
- **Efficient Indexing**: Fast document processing and vector storage for quick retrieval
- **Production-Ready**: Robust error handling, structured logging, and scalable architecture
- **RESTful API**: Clean, well-documented FastAPI endpoints for easy integration
- **20% Improved Onboarding Efficiency**: Reduces time to productivity for new employees

## 🏗️ Architecture

Echo uses a modern RAG (Retrieval-Augmented Generation) pipeline:

1. **Document Upload**: Users upload organizational documents (PDF, DOCX, TXT, etc.)
2. **Indexing**: Documents are processed, chunked, and converted to vector embeddings
3. **Storage**: Embeddings stored in a vector database for efficient retrieval
4. **Query Processing**: User questions are converted to embeddings and matched against the knowledge base
5. **Response Generation**: Relevant context is retrieved and passed to LLM for generating accurate answers

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- pip package manager
- Virtual environment (recommended)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/Sajal-A/infobot.git
cd infobot
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your configuration
```

Required environment variables:
```env
OPENAI_API_KEY=your_openai_api_key
VECTOR_DB_PATH=./data/vector_store
UPLOAD_DIR=./data/uploads
LOG_LEVEL=INFO
```

### Running the Application

Start the FastAPI server:
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`

Access the interactive API documentation at `http://localhost:8000/docs`

## 📚 API Endpoints

### Document Management

#### Upload Document
```http
POST /api/v1/documents/upload
Content-Type: multipart/form-data

Parameters:
- file: Document file (PDF, DOCX, TXT)
- metadata: Optional JSON metadata

Response:
{
  "document_id": "uuid",
  "filename": "document.pdf",
  "status": "indexed",
  "chunks": 45
}
```

#### List Documents
```http
GET /api/v1/documents

Response:
{
  "documents": [
    {
      "id": "uuid",
      "filename": "document.pdf",
      "uploaded_at": "2025-10-31T10:30:00Z",
      "chunks": 45
    }
  ]
}
```

#### Delete Document
```http
DELETE /api/v1/documents/{document_id}

Response:
{
  "status": "deleted",
  "document_id": "uuid"
}
```

### Chat Interface

#### Query Knowledge Base
```http
POST /api/v1/chat/query
Content-Type: application/json

{
  "question": "What is the company's vacation policy?",
  "session_id": "optional-session-id"
}

Response:
{
  "answer": "According to the employee handbook...",
  "sources": [
    {
      "document": "employee_handbook.pdf",
      "page": 12,
      "relevance_score": 0.95
    }
  ],
  "session_id": "uuid"
}
```

#### Get Chat History
```http
GET /api/v1/chat/history/{session_id}

Response:
{
  "session_id": "uuid",
  "messages": [
    {
      "role": "user",
      "content": "What is the vacation policy?",
      "timestamp": "2025-10-31T10:30:00Z"
    },
    {
      "role": "assistant",
      "content": "According to the handbook...",
      "timestamp": "2025-10-31T10:30:05Z"
    }
  ]
}
```

### System

#### Health Check
```http
GET /api/v1/health

Response:
{
  "status": "healthy",
  "version": "1.0.0",
  "vector_db_status": "connected"
}
```

## 🛠️ Technology Stack

- **FastAPI**: Modern, fast web framework for building APIs
- **LangChain**: Framework for developing LLM-powered applications
- **OpenAI GPT**: Language model for response generation
- **Chroma/FAISS**: Vector database for efficient similarity search
- **Pydantic**: Data validation using Python type annotations
- **Uvicorn**: ASGI server for running FastAPI applications

## 📁 Project Structure

```
infobot/
├── main.py                 # Application entry point
├── requirements.txt        # Python dependencies
├── .env.example           # Environment variables template
├── README.md              # Project documentation
├── app/
│   ├── __init__.py
│   ├── api/
│   │   ├── __init__.py
│   │   ├── routes/
│   │   │   ├── documents.py    # Document management endpoints
│   │   │   ├── chat.py         # Chat interface endpoints
│   │   │   └── health.py       # Health check endpoints
│   │   └── dependencies.py     # Shared dependencies
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py          # Configuration management
│   │   ├── logging.py         # Logging setup
│   │   └── exceptions.py      # Custom exceptions
│   ├── services/
│   │   ├── __init__.py
│   │   ├── document_processor.py  # Document parsing & chunking
│   │   ├── vector_store.py        # Vector DB operations
│   │   ├── retriever.py           # Document retrieval logic
│   │   └── chat_engine.py         # RAG pipeline orchestration
│   ├── models/
│   │   ├── __init__.py
│   │   ├── document.py        # Document models
│   │   └── chat.py            # Chat models
│   └── utils/
│       ├── __init__.py
│       └── helpers.py         # Utility functions
├── data/
│   ├── uploads/              # Uploaded documents
│   └── vector_store/         # Vector database files
├── logs/                     # Application logs
└── tests/
    ├── __init__.py
    ├── test_api.py
    ├── test_services.py
    └── conftest.py
```

## 📈 Monitoring & Logging

Echo includes comprehensive logging:

- **Structured JSON logs** for easy parsing and analysis
- **Log levels**: DEBUG, INFO, WARNING, ERROR, CRITICAL
- **Request/Response logging** for API calls
- **Performance metrics** tracking
- **Error tracking** with stack traces

## 👥 Authors

- **Sajal A** - *Initial work* - [Sajal-A](https://github.com/Sajal-A)


**Echo** - Making organizational knowledge accessible, one conversation at a time. 🚀
