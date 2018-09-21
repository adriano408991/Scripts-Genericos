import os.path
import time
from boto.s3.connection import S3Connection,Key #pip install boto==2.49.0
import threading
import hashlib
import sys

class Fila(object):
    def __init__(self):
        self.dados = []
 
    def insere(self, elemento):
        self.dados.append(elemento)
 
    def retira(self):
        try:
            return self.dados.pop(0)
        except IndexError as e:
            print("Lista Acabou!")
            sys.exit()       
 
    def vazia(self):
        return len(self.dados) == 0

class Upload(object):
    def __init__(self, quantidade,delay):            
        self.quantidadeDeArquivos = quantidade
        self.delay = delay
        self.pathToBackup = 'path\\path'
        self.bucket_name = 'my_bucket_name'
        self.AWS_ACCESS_KEY_ID = 'MY KEY ID'
        self.AWS_ACCESS_KEY_SECRET = 'MY KEY SECRET'
        self.utc_timestampp = time.time()
        self.f = Fila()

    def verifica(self):      
        for i in range(len(self.f.dados)):                       
                    if i >= self.quantidadeDeArquivos:
                        print "Delay de %s segundos" % self.delay
                        time.sleep(self.delay)                    
                        self.retira()
                    elif i <= self.quantidadeDeArquivos:                
                        fname=self.f.dados[i].replace("\\", "/")
                        t = threading.Thread(target = self.upload_file, args=(fname,)).start()
                        print "Subindo: "+fname
    def retira(self):    
        for i in range(0, self.quantidadeDeArquivos):
            self.f.retira()       
            self.verifica()

    def upload_file(self,file):
        conn = S3Connection(aws_access_key_id=self.AWS_ACCESS_KEY_ID, aws_secret_access_key=self.AWS_ACCESS_KEY_SECRET)	
        bucket = conn.get_bucket(self.bucket_name)
        key = bucket.new_key(file).set_contents_from_filename(file) 


    def carregaArquivos(self):
        print "Verificando Arquivos para Upload..."    
        for root, dirs, files in os.walk(self.pathToBackup, topdown=False):
            for name in files:
                fname=os.path.join(root, name)          
                self.f.insere(fname)
            print len(self.f.dados) , " Arquivos Encontrados"



up = Upload(100,10)# Quantidade de arquivos e tempo de delay
up.carregaArquivos()
up.verifica()
