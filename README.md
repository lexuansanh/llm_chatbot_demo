# **AI-Powered LLM Chat bot** 🚀

## Code structure
project
├── src
│   ├── agents               # AI agents handling different tasks
│   │   ├── active.py        # Active learning strategies
│   │   ├── ask_again.py     # Handling unclear queries
│   │   ├── get_answer_from_context.py  # Fetching answers from knowledge base
│   │   ├── greeting.py      # Greeting agent
│   │   ├── search_internet.py  # Web search agent
│   ├── data
│   │   ├── preprocessing.py # Data cleaning & normalization
│   │   ├── ingestion.py     # Data ingestion pipelines
│   ├── retriever
│   │   ├── vector_store.py      # Vector database interactions
│   │   ├── embedding_manager.py # Embedding management
│   ├── llm
│   │   ├── chain_builder.py     # LLM pipeline construction
│   │   ├── llm.py               # LLM model management
│   │   ├── response_handler.py  # Validating & processing responses
│   ├── pipelines
│   │   ├── query_pipeline.py    # End-to-end RAG pipeline
│   │   ├── evaluation.py        # Performance evaluation & feedback loop
│   ├── schemas                  # Data validation schemas
│   ├── service                  # API services
│   ├── tools                    # AI agent tools & utilities
│   ├── utils
│   │   ├── utils.py             # Helper functions
│   │   ├── logger.py            # Logging and monitoring
│   ├── tests                    # Unit & integration tests
│   ├── config
│   │   ├── settings.yaml        # Environment settings
│   │   ├── configs.py           # Configuration management
│   │   ├── constants.py         # Global constants
│   │   ├── prompts.py           # Predefined LLM prompts
│   ├── server.py                # FastAPI server entry point
├── Dockerfile                   # Containerization for production
├── .gitignore                   # Files to ignore in Git
├── .pre-commit-config.yaml      # Code linting & formatting rules
├── pyproject.toml               # Python project configuration
├── requirements.txt             # Required dependencies
├── README.md                    # Documentation
└── .env                         # Environment variables

## **Installation & Running the Project** 🚀  

### **1. Clone the Repository**
```bash
git clone https://github.com/lexuansanh/llm_chatbot_demo.git
cd chat-api
```

### **2. Create a Virtual Environment**
```bash
python -m venv venv
```

### **3. Activate the Virtual Environment**
```bash
source venv/bin/activate
```

### **4. Install Dependencies**
```bash
pip install -r requirements.txt
```

### **5. Add Environment Variables**
```bash
PROJECT_NAME=project_name
BOT_ID=your_bot_id
...
```
### **6. Run the Server**
```bash
python -m src.server
```


## **Build and Run Instructions**🚀
### **1. Build the Docker Image**
```bash
docker build -t llm_chatbot_demo .
...
```
### **2. Run the Docker Containerr**
```bash
docker run -p 8000:8000 --env-file .env llm_chatbot_demo
```