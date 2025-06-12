# Multimodal RAG System

## Project Description 

This project implements a **Multimodal Retrieval-Augmented Generation (RAG)** system that combines text and image data to retrieve relevant articles from **The Batch**. The system allows you to:
- Retrieve data based on user queries using text **and** visual embeddings.
- Perform **Classical RAG** (text-based search) and **Multimodal RAG** (combined text + image search).
- Generate AI-powered answers to queries utilizing **Large Language Models (LLMs)**.
- Provide users with an interactive interface for exploring results.

 **Key Feature**: By combining textual and visual content, this system enhances the relevance of search results and elevates user experience.

---
## How to Run the Project

Follow these steps to set up and run the system locally on your machine.

### **1. Clone the Repository**
Start by cloning the project repository into your local machine:
```bash
git clone https://github.com/DolAr1610/Multimodal_RAG.git
cd multimodal_rag
```

### **2. Install Dependencies**
Install all the required Python libraries specified in requirements.txt:
```bash
pip install -r requirements.txt
```

### **3. Prepare the Data**
Ensure that the parsed articles are saved as a JSON file (data/articles_export.json) before running the system.

#### **Option 1: Generate Data**
If the articles are not yet parsed, you can run the parser:
```bash
python -m data.parser
```
#### **Option 2: Use Pre-Generated Data**
Alternatively, use the pre-generated articles_export.json located in the data/ directory.

### **4. Generate Vector Databases (First-Time Setup)**
If this is your first run, you need to create the vector databases for text and images:
```bash
python -m ingestion.ingest_run      # Create vector databases for text and image embeddings
```
This step ensures Chroma vector databases are properly initialized and indexed.

### **5. Launch the Application**
Run the Streamlit application to access the interactive user interface:
```bash
streamlit run main.py
```


## Key Features

### **1. Parsing Articles and Metadata**

The system collects articles, including text, metadata, and associated images, from **The Batch** using web-scraping techniques.

- **Objective:** Extract text content (title, description, publication date), metadata, and associated images.
- **How it Works**:
  - **Selenium:** Handles dynamic website elements like pagination ("Load More", "Older Posts").
  - **BeautifulSoup:** Extracts article text, metadata, and image URLs from HTML.
- **Output:** Articles stored in a structured JSON format as follows:
    ```json
    {
      "title": "Article Title",
      "description": "Short Description",
      "image_url": "https://example.com/image.jpg",
      "date": "2024-10-11",
      "content": "The main content of the article...",
      "source_url": "https://thebatch.org/example-article"
    }
    ```
**Scripts**:
- `initialize_driver()`: Configures the Selenium WebDriver for site interaction.
- `parse_article(url)`: Extracts title, description, metadata, and images of an article.
- `run_parser_and_save_to_json()`: Performs entire filtering and parsing process.

---

### **2. Building Vector Databases**

To enable efficient multimodal retrieval, the system creates **two separate vector databases**: one for text and one for images.

#### **Text Index** 
- **Model:** The text index leverages **SentenceTransformer (E5)** for generating embeddings.
- **Process:**
  - Articles are preprocessed using `chunk_text()` to split larger texts into smaller chunks (400 words with a 50-word overlap).
  - Chunks and embeddings are stored in a **Chroma** database.
  
#### **Image Index** 
- **Model:** Image embeddings are generated using **OpenAI CLIP** (`clip-vit-large-patch14-336`).
- **Process:**
  - Images are accessed via URLs and transformed into embeddings.
  - Embeddings and metadata are stored in a **Chroma** database.

---

### **3. Embedding Integration**

The text and image embeddings are created independently to enhance retrieval performance.

- **Text Integration:** Articles are preprocessed, converted into embeddings using **E5**, and indexed.
- **Image Integration:** Image URLs are retrieved, processed, and added to the image index using embeddings from **CLIP**.

  **Why Separate Databases?**: This ensures that powerful text and image-specific models can be used without sacrificing independence or performance. Each database is optimized for its respective modality.

---

### **4. Search System**

The system provides two types of searches: text-only or multimodal.

#### **1. Classical Search (Text-Based RAG)**
- Focuses exclusively on the text database.
- Finds articles that are highly relevant to the user query.
- Always provides accompanying images from relevant articles.
- **Implementation:** `classical_search()`.

#### **2. Multimodal Search (Text + Image RAG)**
- Leverages both text and image databases.
- Locates the best-matching text and independent image:
  - Finds relevant text embeddings for the query in the text index.
  - Simultaneously searches for image embeddings matching the query in the image index.
  - Combines the results into multimodal pairs.
- **Implementation:** `best_pair_search()`.

  **Output Example**:
```json
{
  "title": "AI in Healthcare",
  "description": "How AI is revolutionizing medicine.",
  "image_url": "https://thebatch.org/healthcare-ai.jpg",
  "date": "2024-10-11",
  "source_url": "https://thebatch.org/ai-healthcare",
  "content": "Artificial intelligence is transforming healthcare with personalized approaches..."
}
```
---

### **5. Answer Generation Using LLM** 

The system integrates a **Large Language Model (LLM)** to generate responses based on the content of retrieved articles.

#### **Model**
- The system uses **meta-llama/llama-3-8b-instruct**, integrated via the **OpenRouter API**.

#### **Process**
1. Retrieved article context (text fragments) is passed to the LLM model.
2. The model generates detailed answers while adhering strictly to the provided context.
3. If the query cannot be addressed due to insufficient context, the system returns a fallback response:
   > **"Sorry, I could not find the answer in the provided context."**

#### **Implementation**
- The function `generate_response()` is responsible for:
  - Extracting text from articles as context.
  - Sending the context to an LLM.
  - Generating user-facing responses.

---

### **6. Interactive User Interface** 

The system includes an interactive **Streamlit-based UI**, designed for a smooth user experience when exploring data.

#### **Features**
1. **Query Input:**
   - Users can input text queries.
   - They can choose between **Classical RAG** (text-only search) or **Multimodal RAG** (text + image search).
2. **Result Display:**
   - Lists retrieved articles with:
     - Metadata (title, description, publication date).
     - Accompanying images.
     - Key fragments of text content.
   - Includes a button to generate detailed responses from the LLM.
## **Summary**

This project explores the integration of multimodal content (text + images) and retrieval-augmented generation (RAG), incorporating cutting-edge NLP and computer vision models to provide users with:

**Contextual Search Results:** Retrieve precise matches using text and visual embeddings seamlessly.

**LLM Responses:** Generate detailed answers with OpenAI LLMs.

**Interactive UI:** Streamlined user interaction through Streamlit.

---
## **Demo Video**

Below is a quick demonstration of how the system works:

Watch the demo video on [Google Drive](https://drive.google.com/file/d/1wd8QJfZYaPdwYy7qyCH4NeuQ0ZFNbW-K/view?usp=sharing).