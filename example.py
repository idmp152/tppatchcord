import asyncio
from time import ctime

from tppatchcord.websockets import main_loop, next_event


def get_token(token_file: str) -> str:
    token: str
    with open(token_file, "r") as f:
        token = f.read()
    return token


async def my_handler():
    try:
        print("Initializing...")
        while True:
            event = await next_event()
            if event["t"] == "MESSAGE_CREATE":
                message = event["d"]
                print(f"{ctime()} | {message["member"]["nick"]} < {message["content"]}")
    except asyncio.CancelledError:
        print("Exiting my_handler...")


TOKEN_FILENAME = "secret.txt"
async def main():
    main_loop_task = asyncio.create_task(main_loop(get_token(TOKEN_FILENAME)))
    my_handler_task = asyncio.create_task(my_handler())

    # Will wait for termination of one of the tasks: my_handler or main_loop, then send a cancellation signal to the other task
    # tppatchcord already handles the cancellation of the main loop for you
    _, pending = await asyncio.wait([main_loop_task, my_handler_task], return_when=asyncio.FIRST_COMPLETED)
    for task in pending:
        task.cancel()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Exiting...")