import base64

def encrypt_string(input_string):
    # 第一轮Base64编码
    encoded_bytes = base64.b64encode(input_string.encode('utf-8'))
    encoded_string = encoded_bytes.decode('utf-8')

    # 反转字符串
    reversed_string = encoded_string[::-1]

    # 再进行一轮Base64编码
    second_encoded_bytes = base64.b64encode(reversed_string.encode('utf-8'))
    encrypted_string = second_encoded_bytes.decode('utf-8')

    return encrypted_string

def decrypt_string(encrypted_string):
    # 解码第二轮Base64
    second_encoded_bytes = encrypted_string.encode('utf-8')
    reversed_string = base64.b64decode(second_encoded_bytes).decode('utf-8')

    # 反转字符串
    encoded_string = reversed_string[::-1]

    # 解码第一轮Base64
    encoded_bytes = base64.b64decode(encoded_string.encode('utf-8'))
    decrypted_string = encoded_bytes.decode('utf-8')

    return decrypted_string