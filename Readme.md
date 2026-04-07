# 📚 LocalRAG: A Retrieval-Augmented Generation Q&A System

A powerful Retrieval-Augmented Generation (RAG) system that combines document ingestion, semantic search, and AI-powered answer generation. This project provides a complete pipeline for building intelligent Q&A systems with support for multiple search strategies and streaming responses.

## ✨ Features

- **Multi-Modal Document Support**: Ingest and process various document formats using the Unstructured library
- **Smart Document Chunking**: Intelligent text chunking with token counting and overlap handling
- **Advanced Search Capabilities**:
  - 🔍 **Keyword Search**: Traditional BM25-style keyword matching
  - 🧠 **Semantic Search**: Vector-based similarity search using embeddings
  - 🔀 **Hybrid Search**: Combines keyword and semantic search for best results
- **Vector Embeddings**: Google Generative AI embeddings with OpenSearch vector database
- **Streaming Responses**: Real-time response generation with streaming support
- **Web Interface**: Interactive Gradio-based UI for easy querying
- **RAG-Powered Generation**: Context-aware answers using Google's Generative AI (Gemini)

## 🛠️ Tech Stack

- **Vector Database**: OpenSearch
- **Embeddings**: Google Generative AI
- **LLM**: Google Gemini API
- **Frontend**: Gradio
- **Search Libraries**: LangChain, TikToken
- **Data Processing**: Unstructured, Requests
- **Environment**: Python 3.8+

## 📋 Prerequisites

Before you begin, ensure you have the following installed:
- Python 3.8 or higher
- OpenSearch instance running (default: localhost:9200)
- Google Cloud API credentials with Generative AI enabled

## 🚀 Installation

### 1. Clone the Repository
```bash
git clone <repository-url>
cd multimodal_rag
```

### 2. Create Virtual Environment
```bash
python -m venv venv
# On Windows
venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Set Up Environment Variables
Create a `.env` file in the project root:
```env
GEMINI_API_KEY=your_google_generative_ai_api_key
OPENSEARCH_HOST=localhost
OPENSEARCH_PORT=9200
```

## 📁 Project Structure

```
multimodal_rag/
├── Readme.md                 # This file
├── requirements.txt          # Python dependencies
├── .env                      # Environment variables (create this)
├── files/                    # Directory for source documents
│   └── *.pdf, *.txt, etc.   # Add your documents here
└── src/
    ├── app.py              # Gradio web interface
    ├── ingestion.py        # Document ingestion & OpenSearch setup
    ├── chunking.py         # Document chunking logic
    ├── retrieval.py        # Multi-strategy search implementation
    ├── generation.py       # Response generation with RAG
    └── helper.py           # Utility functions (embeddings, client initialization)
```

## 🔧 Configuration

### OpenSearch Setup
The system automatically creates an index named `localrag` with proper vector mappings when you run the ingestion pipeline.

### Search Methods

**Hybrid Search** (Default):
Combines keyword and semantic search with weighted results for optimal retrieval.

**Semantic Search**:
Pure vector similarity search for conceptual matches.

**Keyword Search**:
Traditional text matching for exact term searches.

## 📖 Usage

### 1. Prepare Your Documents
Place your documents (PDF, TXT, etc.) in the `files/` directory:
```bash
# Example
cp /path/to/documents/* ./files/
```

### 2. Ingest Documents
Run the ingestion pipeline to process documents and build the vector index:
```bash
cd src
python ingestion.py
```

This will:
- Load documents from the `files/` directory
- Split them into chunks
- Generate embeddings
- Store them in OpenSearch

### 3. Launch the Web Interface
Start the Gradio application:
```bash
python app.py
```

The interface will be available at `http://localhost:7860` (or the URL shown in console).

### 4. Ask Questions
Use the web interface to:
- Enter your question
- Select search method (keyword, semantic, or hybrid)
- Choose response generation (streaming or normal)
- Get RAG-powered answers with source documents

## 🔑 Key Components

### Document Ingestion (`ingestion.py`)
- Loads documents from the `files/` directory
- Creates/updates OpenSearch index with vector field mappings
- Orchestrates the chunking and embedding pipeline

### Chunking (`chunking.py`)
- Splits documents into manageable chunks
- Counts tokens to ensure optimal chunk sizes
- Handles text overlap for better context preservation

### Retrieval (`retrieval.py`)
- **keyword_search()**: BM25-style text search
- **semantic_search()**: Vector similarity search
- **hybrid_search()**: Combined weighted search strategy

### Generation (`generation.py`)
- Implements RAG pipeline
- Retrieves relevant context from vector database
- Generates answers using Google Gemini API
- Supports streaming and regular response modes

### Helper Functions (`helper.py`)
- `get_embedding()`: Generates embeddings using Google Generative AI
- `get_opensearch_client()`: Initializes OpenSearch connection

## 📊 Example Workflow

```python
# The system automatically handles this through the UI:
1. User enters: "What is Retrieval-Augmented Generation?"
2. System retrieves relevant chunks using hybrid search
3. System generates context-aware answer from chunks
4. Response streamed to user in real-time
```

## 🔐 Security Notes

- **API Keys**: Never commit `.env` files with real API keys to version control
- **OpenSearch**: Consider authentication and network security for production deployments
- **Rate Limiting**: Be mindful of Google Generative AI API rate limits

## 🐛 Troubleshooting

### OpenSearch Connection Error
```
Error: Couldn't resolve host
```
Ensure OpenSearch is running on localhost:9200:
```bash
# Check OpenSearch status
curl http://localhost:9200
```

### API Key Error
```
ERROR: GEMINI_API_KEY not found in environment variables
```
Verify your `.env` file is in the project root and contains the correct API key.

### Embedding Dimension Mismatch
The system auto-detects embedding dimensions during setup. If you change embedding models, delete the OpenSearch index to recreate it.

## 📈 Performance Tips

- **Batch Processing**: For large document collections, the ingestion process may take time
- **Chunk Size**: Adjust chunk sizes in `chunking.py` based on your use case
- **Vector Search**: Semantic search is slower but more accurate than keyword search
- **Hybrid Search**: Provides the best balance between speed and accuracy

## 🤝 Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues for bugs and feature requests.

## 📝 License

This project is available as-is. Please check if Google's APIs require specific licensing in your use case.

## 📚 Resources

- [Google Generative AI Documentation](https://ai.google.dev/)
- [OpenSearch Documentation](https://opensearch.org/docs/)
- [LangChain Documentation](https://python.langchain.com/)
- [Gradio Documentation](https://gradio.app/)

## 🎯 Future Enhancements

- [ ] Support for image and multimodal content
- [ ] Caching layer for frequently asked questions
- [ ] Fine-tuning on custom document sets
- [ ] Advanced filtering and metadata management
- [ ] Conversation history and context management
- [ ] Performance metrics and logging dashboard

---

**Created**: 2026 | **Status**: Active Development
