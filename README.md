PubMed Research Agent
A Python-based research agent to query PubMed for peer-reviewed articles on clinical and disease-related topics, such as candidate drugs targeting specific mutations.
Features

Queries PubMed’s API for peer-reviewed articles.
Summarizes article abstracts using a lightweight distilbert model.
Saves results to a CSV file.
Runs on Google Colab’s free tier.

Setup
Google Colab Setup

Open Google Colab.
Import the repository: File > Open Notebook > GitHub > your-username/pubmed-research-agent.
Enable GPU: Runtime > Change runtime type > Hardware accelerator > T4 GPU.
Install dependencies:!pip install -r requirements.txt


Run the script in a cell:%run src/research_agent.py



Usage

Run the script and enter a query, e.g., "candidate drugs targeting mutation XXXX in PI3K".
The agent fetches up to 5 articles, summarizes their abstracts, and saves results to pubmed_results.csv.
Review the CSV or console output for article details.

Example
Enter your query: candidate drugs targeting mutation E545K in PI3K

Output: Summarized abstracts and article metadata saved to pubmed_results.csv.
Requirements
See requirements.txt for dependencies.
License
MIT License
