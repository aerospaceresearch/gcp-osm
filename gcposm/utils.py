from base64 import b64decode, b64encode
import os

def decode_base64_id(base64: str):
    int_as_bytes = b64decode(base64) 
    return str(int.from_bytes(int_as_bytes, 'big'))
    
def encode_id_as_base64(id):
    id_as_bytes = int.to_bytes(int(id), 8, 'big')
    return b64encode(id_as_bytes).decode()

def get_all_files(filename):
    processing_files = []
    for root, dirs, files in os.walk(filename):
        for file in files:
            filepath = os.path.join(root, file)
            if os.path.isfile(filepath):
                #print("file", filepath)
                processing_files.append(filepath)

    return processing_files


def get_one_file(filename):
    return [filename]

if __name__ == '__main__':
    '''nothn'''
