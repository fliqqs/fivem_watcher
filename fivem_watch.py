import keyboard
import sys
import socket
import struct

def send_command(message):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ip_address = "127.0.0.1"
    port = 29200  # fx console

    b_header = bytes.fromhex("434d4e4400d20000")  # CMND 0x00d20000
    b_command = ("restart "+ message + "\n").encode('utf-8')
    b_padding = bytes([0, 0])
    b_length = struct.pack('>I', len(message) + 13)
    b_terminator = bytes([0])

    data = b_header + b_length + b_padding + b_command + b_terminator

    try:
        s.connect((ip_address, port))
        s.sendall(data)
        s.close()
    except ConnectionRefusedError:
        print("Connection refused")

def on_ctrl_s(event):
    if event.event_type == keyboard.KEY_DOWN and keyboard.is_pressed('ctrl') and keyboard.is_pressed('s'):
        packages_to_watch = []
        if len(sys.argv) > 1:
            for arg in sys.argv:
                if arg != sys.argv[0]:

                    packages_to_watch.append(arg)

        for package in packages_to_watch:
            print(f'restarting  {package}')
            send_command(package)

def main():
    keyboard.hook(on_ctrl_s)
    keyboard.wait()

if __name__ == '__main__':
    main()
