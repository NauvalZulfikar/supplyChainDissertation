import hashlib
import json

def hash_(block):
      encoded_block = json.dumps(block, sort_keys=True).encode()
      return hashlib.sha256(encoded_block).hexdigest()
