"""
"""

import fitz 
import logging

from typing import List
from pathlib import Path

from indexing import *


def is_significant(text: str) -> bool:
  """
  """
  words = [word for word in text.split() if len(word) > 3 and word not in STOPWORDS and word.isalpha()]
  if len(words) > MINIMUM_WORD_IN_PARA: return True
  else: return False


def split_pdf_in_paras(file: str) -> List[dict]:
  """
  """
  paras = []
  doc = fitz.open(file)
  
  for page in doc:
    for block in page.getText('blocks'):
      text = block[4].replace('-\n', '').replace('\n', ' ')
      if is_significant(text): 
        paras.append({"text": text, "meta": {"name": Path(file).name}})

  return paras


def split_docx_in_paras(file: str) -> List[dict]:
  """
  """
  pass


def split_handwritten_in_paras(file: str) -> List[dict]:
  """
  """
  pass


def split_document_in_paras(file: str) -> List[dict]:
  """
  """
  paras = []

  try:
    if file.endswith('.pdf'): paras = split_pdf_in_paras(file)
    if file.endswith('.docx'): paras = split_docx_in_paras(file)
    if file.endswith('.jpg'): paras = split_handwritten_in_paras(file)
  except Exception as e:
    logging.warn(e)
  
  return paras


def split_multiple_documents_in_paras(files: List[str]) -> List[dict]:
  """
  """
  paras = []
  
  for file in files:
    paras.extend(split_document_in_paras('./' + file))

  return paras