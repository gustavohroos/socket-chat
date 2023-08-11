import struct
import time

def create_chat_message(message_data, username, type=100):
    protocol_version = 1
    message_type = type
    username_data = username.encode('utf-8')
    message_data_encoded = message_data.encode('utf-8')
    username_length = min(len(username_data), 10)
    message_length = len(message_data_encoded)
    timestamp = int(time.time())

    header = struct.pack('!BIII', protocol_version, message_type, username_length, message_length)

    return (
        header
        + username_data[:10].ljust(10, b'\x00')
        + struct.pack('!I', timestamp)
        + message_data_encoded
    )

def parse_chat_message(data):
    protocol_version, message_type, username_length, message_length = struct.unpack('!BIII', data[:13])
    username_data = data[13:23]
    timestamp = struct.unpack('!I', data[23:27])
    message_data = data[27:]
    username = username_data.decode('utf-8').rstrip('\x00')
    content = message_data.decode('utf-8')
    timestamp_readable = time.strftime('%H:%M:%S', time.localtime(timestamp[0]))

    return {
        'protocol_version': protocol_version,
        'message_type': message_type,
        'timestamp': timestamp_readable,
        'username': username,
        'username_length': username_length,
        'content': content,
        'message_length': message_length,
    }