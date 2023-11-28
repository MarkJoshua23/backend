from flask import Flask, request, jsonify
from langchain.embeddings import GooglePalmEmbeddings
from langchain.llms.google_palm import GooglePalm
from langchain.vectorstores import Pinecone
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
import pinecone
import os
import sys

app = Flask(__name__)

os.environ['Google_API_KEY'] = 'AIzaSyDYC92z_C_Pl8uIbNv8U24DXqXHvnRFWPA'

embeddings = GooglePalmEmbeddings()

PINECONE_API_KEY = os.environ.get('PINECONE_API_KEY', 'b3d79b7c-e171-4cf7-8b22-7799d5e4e323')
PINECONE_API_ENV = os.environ.get('PINECONE_API_ENV', 'gcp-starter')

pinecone.init(
    api_key=PINECONE_API_KEY,
    environment=PINECONE_API_ENV
)
index_name = "myeucstudenthandbook"

docsearch = Pinecone.from_existing_index(index_name, embeddings)

llm = GooglePalm(temperature=0.1)
qa = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=docsearch.as_retriever(search_type="similarity",search_kwargs={"k": 4}),input_key="question")

@app.route('/query', methods=['POST'])
def answer_query():
    query = request.json.get('query')
    try:
        answer = qa.run(query)
    except Exception as e:
        answer = None

    if answer:
        return jsonify(answer)
    else:
        return jsonify({"query": query, "answer": "Sorry, I couldn't find an answer to the question. Please try another question."})

if __name__ == '__main__':
    app.run(debug=True)
