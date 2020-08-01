"""
"""

from setup import enable_elastic_search, base_corpus
from haystack.reader.farm import FARMReader
from haystack.retriever.dense import DensePassageRetriever
from haystack.database.elasticsearch import ElasticsearchDocumentStore

from haystack import Finder
from typing import Dict, List

enable_elastic_search()

document_store_dense = ElasticsearchDocumentStore(host="localhost", username="", password="", index="document", embedding_field="embedding", embedding_dim=768)
documet_store_sparse = ElasticsearchDocumentStore(host="localhost", username="", password="", index="document")

document_store_dense.write_documents(base_corpus())
dense_retriever = DensePassageRetriever(document_store=document_store_dense, embedding_model="dpr-bert-base-nq",do_lower_case=True, use_gpu=True)
document_store_dense.update_embeddings(dense_retriever)

reader = FARMReader(model_name_or_path="deepset/roberta-base-squad2", use_gpu=True)

def prepare_answer_with_granularity(results: List) -> Dict:
  """
  """
  if len(results) == 0: 
    return {'status': 'fail'}
  
  answers = [results[0]['answer']]  
  content = results[0]['context']
  content = split_into_sentences(content)
  answer = results[0]['answer']
  for sen in content:
    if results[0]['answer'] in sen:
        answer = sen
        break 
  answers.append(answer)
  answers.append(results[0]['para'])
  
  answer = results[0]['para']
  details = ""
  done = set()
  done.add(results[0]['para'])
  for result in results[1:]:
    if result['para'] in done: continue
    details += '\n' + result['para']
    if len(details.split()) > 30: break 
    done.add(result['para'])
  answers.append(answer + details)

  answer = results[0]['para']
  if len(results) > 1: answer += '\n'+ results[1]['para']
  details = ""
  done = set()
  done.add(results[0]['para'])
  if len(results) > 1: done.add(results[1]['para'])
  for result in results[1:]:
    if result['para'] in done: continue
    details += '\n' + result['para']
    if len(details.split()) > 50: break 
    done.add(result['para'])
  answers.append(answer + details)
  
  return {
      'status': 'success',
      'answer': answers
    }


def qa_with_dense_retrieval(question: str) -> List[dict]:
  """
  """
  finder = Finder(reader, dense_retriever)
  prediction = finder.get_answers(question=question, top_k_retriever=10, top_k_reader=5)
  paras = {para.id : para.text for para in dense_retriever.retrieve(question)}
  results = []
  for result in prediction['answers']:
    if result['score'] > 0:
      results.append({'answer': result['answer'], 'context': result['context'], 'para': paras[result['document_id']]})
  return results 


def find_answer(question: str) -> List[dict]:
  """
  """
  try:
    question = question.strip()
    if question[-1] == '?' and question[-2] != ' ': question = question.replace('?', ' ')
    content = qa_with_dense_retrieval(question)
    return prepare_answer_with_granularity(content)
  except:
    return {'status': 'fail'}
    return {
        'status': 'fail',
    }
