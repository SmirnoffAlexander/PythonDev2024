import cmd
import readline
import select
import shlex
import socket
import threading

import yaml


def load_yaml(path: str):
    with open(path, "r") as f:
        data = yaml.safe_load(f)

    return data


class CowClient(cmd.Cmd):
    intro = """Welcome to CowSay Chat!"""
    prompt = "(cowsay client)"

    def __init__(self, config: dict, locker: threading.Lock):
        super(CowClient, self).__init__()
        self.hostname = config["HOST"]
        self.port = config["PORT"]
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.hostname, self.port))
        self.login = None
        self.is_alive = True
        self.locker = locker

    def do_who(self, args):
        """List all logged users"""
        self.send_message("who")

    def do_cows(self, args):
        """List all possible login names"""
        self.send_message("cows")

    def do_login(self, args):
        """Login your client"""
        login, *trash = shlex.split(args)
        self.login = login
        self.send_message(f"login {login}")

    def complete_login(self, text, line, beidx, endidx):
        args = shlex.split(line)
        nargs = len(args)
        if nargs <= 2:
            with self.locker:
                self.send_message("cows")
                data = self.get_message(None)
                cows = [cow for cow in data.split("\n") if cow.startswith(text)]
                return cows

    def do_say(self, args):
        """Send message to specific user"""
        cow_name, *message = shlex.split(args)
        message = " ".join(message)
        self.send_message(f"say {cow_name} {message}")

    def complete_say(self, text, line, begidx, endidx):
        args = shlex.split(text)
        nargs = len(args)
        if nargs <= 2:
            with self.locker:
                self.send_message("who")
                data = self.get_message(None)
                cows = [cow for cow in data.split("\n") if cow.startswith(text)]
                return cows

    def do_yield(self, args):
        """Yield message to all users"""
        message = shlex.split(args)
        message = " ".join(message)
        self.send_message(f"yield {message}")

    def do_quit(self, args):
        """Quit cow client"""
        print(f"Bye {self.login}")
        self.send_message("quit")
        self.is_alive = False
        return True

    def get_message(self, timeout):
        ready = select.select([self.socket], [], [], timeout)
        if ready[0]:
            return self.socket.recv(1024).decode().strip()

    def send_message(self, message):
        return self.socket.send(f"{message}\n".encode())

    def receive(self):
        while True:
            with self.locker:
                data = self.get_message(0)
            if data:
                print(
                    f"\n{data.strip()}\n{self.prompt}{readline.get_line_buffer()}",
                    end="",
                    flush=True,
                )
            if not self.is_alive:
                break


if __name__ == "__main__":
    config = load_yaml("config.yaml")
    locker = threading.Lock()
    cow_client = CowClient(config, locker)
    thread = threading.Thread(target=cow_client.receive, args=())
    thread.start()
    cow_client.cmdloop()
