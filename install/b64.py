import base64
import sys

if len(sys.argv)==2:
    with open(sys.argv[1], "rb") as f:
        with open(sys.argv[1]+".b64", "wb") as f2:
            base64.encode(f, f2)
        
