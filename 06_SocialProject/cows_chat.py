#!/usr/bin/env python3
import asyncio

import cowsay

clients = {}
client_to_cow = {}
cow_to_client = {}
allowed_cows = set(cowsay.list_cows())


async def chat(reader, writer):
    me = "{}:{}".format(*writer.get_extra_info("peername"))
    clients[me] = asyncio.Queue()
    send = asyncio.create_task(reader.readline())
    receive = asyncio.create_task(clients[me].get())
    while not reader.at_eof():
        done, pending = await asyncio.wait(
            [send, receive], return_when=asyncio.FIRST_COMPLETED
        )
        for q in done:
            if q is send:
                send = asyncio.create_task(reader.readline())
                command = q.result().decode().strip()
                if command == "who":
                    for client in clients:
                        if client != me and client in client_to_cow:
                            client_cow = client_to_cow[client]
                            await clients[me].put(f"{client_cow}")
                elif command.split(" ")[0] == "login":
                    cow_name = " ".join(command.split(" ")[1:])
                    if cow_name in allowed_cows:
                        allowed_cows.remove(cow_name)
                        cow_to_client[cow_name] = me
                        client_to_cow[me] = cow_name
                        await clients[me].put(
                            f"New user with name {cow_name} was logged in!"
                        )
                    elif me in client_to_cow:
                        await clients[me].put("You are already logged in!")
                    else:
                        await clients[me].put(
                            f"Name {cow_name} is not in allowed cow names!"
                        )
                elif command == "cows":
                    await clients[me].put("\n".join(allowed_cows))
                elif command == "quit":
                    if me in client_to_cow:
                        allowed_cows.add(client_to_cow[me])
                        cow_name = client_to_cow[me]
                        client_to_cow.pop(me)
                        cow_to_client.pop(cow_name)
                        await clients[me].put(f"User with name {cow_name} quited!")
                        clients.remove(me)
                    else:
                        await clients[me].put("You were not logged in!")
                elif command.split(" ")[0] == "say":
                    receiver = command.split(" ")[1]
                    message = " ".join(command.split(" ")[2:])
                    if receiver in cow_to_client:
                        receiver_id = cow_to_client[receiver]
                        res = cowsay.cowsay(message, cow=client_to_cow[me])
                        await clients[receiver_id].put(res)
                    else:
                        await clients[me].put(f"No such user: {receiver}!")
                elif command.split(" ")[0] == "yield":
                    message = " ".join(command.split(" ")[1:])
                    res = cowsay.cowsay(message, cow=client_to_cow[me])
                    for client_id in client_to_cow:
                        if client_id is not me:
                            await clients[client_id].put(res)
                else:
                    await clients[me].put("No such command!")

            elif q is receive:
                receive = asyncio.create_task(clients[me].get())
                writer.write(f"{q.result()}\n".encode())
                await writer.drain()

    send.cancel()
    receive.cancel()
    del clients[me]
    writer.close()
    await writer.wait_closed()


async def main():
    server = await asyncio.start_server(chat, "0.0.0.0", 1337)
    async with server:
        await server.serve_forever()


asyncio.run(main())
