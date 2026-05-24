import base64
import json
from typing import Dict

token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxIiwiZW1haWwiOiJ1c2VyQGV4YW1wbGUuY29tIiwidXNlcl9pZCI6IjEiLCJleHAiOjE3NjQwNzU4OTF9.Cr4GUWhKtIPwrM3s1a3NMZg5UvEktFfCdC_hm8ZzKmM"

def decode_jwt_str(input_str) -> bytes:
    padding = '=' * (len(input_str) % 4)
    return base64.urlsafe_b64decode(input_str + padding)

def decode_jwt_token(token: str) -> Dict:
    header_base64, payload_base64, sig = token.split(".")
    header = json.loads(decode_jwt_str(header_base64))
    payload = json.loads(decode_jwt_str(payload_base64))
    return {
        "header": header,
        "payload": payload,
        "sig": sig
    }