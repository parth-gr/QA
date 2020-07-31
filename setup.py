"""
"""

import os
from subprocess import Popen, PIPE, STDOUT

from indexing.utils import split_multiple_documents_in_paras

def enable_elastic_search(forced: bool = False):

  print('Enable Elastic search...')

  if forced: 
    os.system('rm -r elasticsearch-7.6.2')
    os.system('rm -r elasticsearch-7.6.2-linux-x86_64.tar.gz')
  
  if 'elasticsearch-7.6.2-linux-x86_64.tar.gz' not in os.listdir() or forced:
    os.system('wget https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-7.6.2-linux-x86_64.tar.gz -q')
    os.system('tar -xzf elasticsearch-7.6.2-linux-x86_64.tar.gz')
    os.system('chown -R daemon:daemon elasticsearch-7.6.2')

  es_server = Popen(['elasticsearch-7.6.2/bin/elasticsearch'],
                   stdout=PIPE, stderr=STDOUT,
                    preexec_fn=lambda: os.setuid(1)  # as daemon
                  )
  # wait until ES has started
  os.system('sleep 30')


def base_corpus():
  """
  """
  files = ['files/base/'+file for file in os.listdir('files/base')]
  return split_multiple_documents_in_paras(files)