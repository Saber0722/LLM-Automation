# LLM-Automation Agent

This is a collection of Python scripts and tools designed to automate various tasks using Large Language Models (LLMs). This project showcases practical applications of LLMs in data processing, natural language understanding, and automation workflows using openai-gpt-4 model.

## Features

- **Data Processing Utilities**: Scripts like `contacts_sorting.py` and `first_ten_logs.py` assist in organizing and analyzing data efficiently.
- **LLM-Powered Automation**: Leverage the power of LLMs for tasks such as email parsing (`email_passing.py`) and credit card data handling (`credit_card_llm.py`).
- **GitHub Data Integration**: Fetch and process data directly from GitHub repositories using `get_data_from_github.py`.
- **Text Embedding and Similarity**: Utilize `similar_text_embeddings.py` to compute text similarities, aiding in tasks like document clustering and semantic search.
- **Markdown Mapping**: Convert and map markdown content effectively with `markdown_mapping.py`.
- **SQLite Database Interactions**: Manage and query SQLite databases seamlessly using `sql_lite.py`.

## Installation

1. **Clone the Repository**:

   ```bash
   git clone https://github.com/Saber0722/LLM-Automation.git
   cd LLM-Automation
   ```


2. **Set Up a Virtual Environment**:

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```


3. **Install Dependencies**:

   ```bash
   pip install -r requirements.txt
   ```


   *Note*: Ensure you have Python 3.7 or higher installed.

## Usage

Each script in this repository serves a specific function. Here's a brief overview:

- **`contacts_sorting.py`**: Sorts and organizes contact information.
- **`email_passing.py`**: Parses and processes email content using LLMs.
- **`credit_card_llm.py`**: Handles credit card data analysis with LLM assistance.
- **`get_data_from_github.py`**: Fetches data from specified GitHub repositories.
- **`similar_text_embeddings.py`**: Calculates text embeddings and measures similarity.
- **`markdown_mapping.py`**: Maps and converts markdown files for various applications.
- **`sql_lite.py`**: Performs SQLite database operations.

To execute any script:

Make sure the content containt the task specific details and the content will be passed to the LLM to perform the desired function.

## License

This project is licensed under the [MIT License](LICENSE).

## Contact

For questions, suggestions, or collaborations, please open an issue or contact [Saber0722](https://github.com/Saber0722).
