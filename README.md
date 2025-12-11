**Mastercard Intelligence Agent**

The Mastercard Intelligence Agent is a retrieval augmented chatbot designed to answer questions about Mastercard using information from three key documents: the company’s 10K filing, its Sustainability Bond Report, and a news article announcing Mastercard Threat Intelligence. 
The system extracts, cleans, and chunks PDF text, retrieves the most relevant sections for each query, and generates grounded responses using a locally hosted LLM through Ollama. A Streamlit interface provides an easy way to interact with the agent.



**Features**

* PDF text extraction and cleaning using `pdfplumber` and regular expressions
* Chunking pipeline for accurate document retrieval
* Local LLM inference powered by **Ollama**
* Streamlit based chat interface
* Answers include traceable source context from the underlying documents

**Project Structure**

/data                 Original PDF documents  
/extraction           Extraction and cleaning scripts  
/chunks               Generated text chunks  
streamlit_app.py      Frontend interface  
extract.py            PDF processing logic  

**How It Works**

1. Extract text from PDFs using `pdfplumber`
2. Clean and normalize the text
3. Chunk the documents into overlapping segments for retrieval
4. Retrieve relevant chunks based on user queries
5. Generate responses using an Ollama hosted LLM
6. Display results through a Streamlit chatbot interface


**Installation**
* Python 3.10 or later
* Ollama installed locally
* Streamlit

**Running the App**

Make sure Ollama is running, then launch the Streamlit interface:

"streamlit run streamlit_app.py"

A local browser window will open where you can interact with the agent.

**Usage**

Ask natural language questions such as:

What does Mastercard do?
What risks does Mastercard face?
What ESG goals are mentioned?
Summarize their financial performance.

The agent retrieves relevant text chunks and generates grounded answers based on the content.

**Limitations**

* The agent is trained only on the three provided PDFs
* Retrieval quality depends on chunking and document cleanliness
* Not designed to answer questions outside the scope of the source material

**Future Enhancements**

* Expand training data with more Mastercard filings and reports
* Improve chunking accuracy and cleaning rules
* Integrate vector databases for more robust retrieval

