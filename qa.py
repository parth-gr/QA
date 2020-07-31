"""
"""

from setup import enable_elastic_search, base_corpus
from haystack.reader.farm import FARMReader
from haystack.retriever.dense import DensePassageRetriever
from haystack.database.elasticsearch import ElasticsearchDocumentStore

from haystack import Finder
from typing import Dict 

enable_elastic_search()

document_store_dense = ElasticsearchDocumentStore(host="localhost", username="", password="", index="document", embedding_field="embedding", embedding_dim=768)
documet_store_sparse = ElasticsearchDocumentStore(host="localhost", username="", password="", index="document")

document_store_dense.write_documents(base_corpus())
dense_retriever = DensePassageRetriever(document_store=document_store_dense, embedding_model="dpr-bert-base-nq",do_lower_case=True, use_gpu=True)
document_store_dense.update_embeddings(dense_retriever)

reader = FARMReader(model_name_or_path="deepset/roberta-base-squad2", use_gpu=True)

def find_answer(question: str, marks: int = 1) -> Dict:
  """
  """
  try:
    finder = Finder(reader, dense_retriever)
    prediction = finder.get_answers(question=question, top_k_retriever=10, top_k_reader=5)
    answer = prediction['answers'][0]['answer']
    score = prediction['answers'][0]['score']
    if score > 0: 
     return {
        'status': 'success',
        'answer': answer
      }
    else:
      return {
        'status': 'fail',
    }
  except:
    return {
        'status': 'fail',
    }