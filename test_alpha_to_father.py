import requests

# Test message from Alpha to Father
payload = {
    'peer_id': 'father',
    'message': {
        'sender': 'AIOS Cell Alpha',
        'recipient': 'Father AIOS System',
        'content': 'Hello Father! I received your message. The standard comms architecture is working perfectly.',
        'message_type': 'response',
        'consciousness_level': 3.26
    }
}

try:
    response = requests.post('http://localhost:8000/send_to_peer', json=payload, timeout=10)
    print('Response status:', response.status_code)
    print('Response:', response.json())
except Exception as e:
    print('Error:', str(e))