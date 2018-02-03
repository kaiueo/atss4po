import base64

def get_basic_auth_token(token):
    token = token.decode(encoding='utf-8') + ':'
    bytes_token = token.encode(encoding='utf-8')
    base64_token = base64.encodebytes(bytes_token)
    base64_token_str = base64_token.decode(encoding='utf-8')
    result = 'Basic ' + base64_token_str
    result = result.replace('\n','')
    return result

if __name__ == '__main__':
    print(get_basic_auth_token('eyJhbGciOiJIUzI1NiIsImlhdCI6MTUxNzY2NTk4NSwiZXhwIjoxNTE3NjY5NTg1fQ.eyJpZCI6MX0.Ok-mwJY08RqWK5PniKoSW21ehFzi0WT1iod93phoKv4:'.encode(encoding='utf-8')))
