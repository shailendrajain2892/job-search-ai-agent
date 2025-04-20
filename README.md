# Job Search AI Agent 🤖

An intelligent AI-powered assistant that helps streamline your job search process using advanced language models and automation.

## Features

- 🔍 **Smart Job Search**: Automatically searches for relevant job listings based on your title and location preferences
- 📝 **AI Cover Letter Generator**: Creates tailored cover letters using your resume and skills
- 📄 **Resume Enhancer**: Automatically improves and tailors your resume based on job descriptions
- 🎯 **Application Simulator**: Provides a complete application package with updated resume and cover letter

## Prerequisites

- Python 3.13 or higher
- Poetry for dependency management
- OpenAI API key
- SerpAPI key

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/job-search-ai-agent.git
cd job-search-ai-agent
```

2. Install dependencies using Poetry:
```bash
poetry install
```

3. Create a `.env` file in the root directory with your API keys:
```
OPEN_API_KEY=your_openai_api_key
SERP_API_KEY=your_serpapi_key
```

## Usage

1. Start the application:
```bash
poetry run streamlit run starter_code.py
```

2. Access the web interface at `http://localhost:8501`

3. To use the application:
   - Enter your desired job title and location
   - Upload your resume (PDF format)
   - List your key skills
   - Click "Find Jobs" to start the search
   - Generate AI-powered cover letters and enhanced resumes
   - Use the simulated application feature to prepare your application package

## Dependencies

- streamlit: Web interface
- langchain: AI/LLM orchestration
- openapi: OpenAI API integration
- pypdf: PDF processing
- python-dotenv: Environment variable management

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

[MIT License](LICENSE)

## Author

Shailendra Jain (shailendrajain28@gmail.com)