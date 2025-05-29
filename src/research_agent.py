from Bio import Entrez
from transformers import pipeline
import pandas as pd
import torch
import re

def setup_entrez(email):
    """Set up Entrez with user email for PubMed API access."""
    Entrez.email = email  # Required by NCBI
    return Entrez

def search_pubmed(query, max_results=5):
    """Search PubMed for articles based on the query."""
    handle = Entrez.esearch(db="pubmed", term=query, retmax=max_results)
    record = Entrez.read(handle)
    handle.close()
    return record["IdList"]

def fetch_article_details(pmids):
    """Fetch article details (title, abstract, authors) for given PMIDs."""
    handle = Entrez.efetch(db="pubmed", id=",".join(pmids), retmode="xml")
    records = Entrez.read(handle)
    handle.close()
    
    articles = []
    for article in records["PubmedArticle"]:
        try:
            title = article["MedlineCitation"]["Article"]["ArticleTitle"]
            abstract = article["MedlineCitation"]["Article"].get("Abstract", {}).get("AbstractText", [""])[0]
            authors = ", ".join([author.get("LastName", "") + " " + author.get("Initials", "") 
                                 for author in article["MedlineCitation"]["Article"].get("AuthorList", [])])
            articles.append({"title": title, "abstract": abstract, "authors": authors})
        except Exception as e:
            print(f"Error processing article: {e}")
    return articles

def summarize_text(text, summarizer, max_length=150):
    """Summarize text using a lightweight transformer model."""
    # Truncate text to avoid memory issues
    text = text[:512]  # DistilBERT has a max token limit
    summary = summarizer(text, max_length=max_length, min_length=30, do_sample=False)
    return summary[0]["summary_text"]

def main():
    # Initialize Entrez with your email (replace with your email)
    setup_entrez("your.email@example.com")
    
    # Check for GPU availability
    device = 0 if torch.cuda.is_available() else -1
    print(f"Using device: {'GPU' if device == 0 else 'CPU'}")
    
    # Initialize lightweight summarizer
    summarizer = pipeline("summarization", model="distilbert-base-uncased", device=device)
    
    # Example query
    query = input("Enter your query (e.g., 'candidate drugs targeting mutation XXXX in PI3K'): ")
    clean_query = re.sub(r"XXXX", "specific mutation", query)  # Replace placeholder
    
    # Search PubMed
    pmids = search_pubmed(clean_query)
    if not pmids:
        print("No articles found.")
        return
    
    # Fetch articles
    articles = fetch_article_details(pmids)
    
    # Process and summarize
    results = []
    for article in articles:
        summary = summarize_text(article["abstract"], summarizer) if article["abstract"] else "No abstract available."
        results.append({
            "Title": article["title"],
            "Authors": article["authors"],
            "Abstract": article["abstract"],
            "Summary": summary
        })
    
    # Save to CSV
    df = pd.DataFrame(results)
    df.to_csv("pubmed_results.csv", index=False)
    print("Results saved to pubmed_results.csv")
    
    # Display results
    for idx, row in df.iterrows():
        print(f"\nArticle {idx + 1}:")
        print(f"Title: {row['Title']}")
        print(f"Authors: {row['Authors']}")
        print(f"Summary: {row['Summary']}")

if __name__ == "__main__":
    main()