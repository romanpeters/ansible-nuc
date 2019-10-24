"""
This script automatically starts and stops a Minecraft server's Docker container.
If someone tries to join the container is started.
If no players are online anymore the container is stopped.
"""
import socket
import time
import subprocess
import logging
import sys
import fileinput

# adjust these variables as needed
HOST = "minecraft.romanpeters.nl"
PORT = 1337
CONTAINER = "minecraft-server"


logger = logging.getLogger()
logging.basicConfig(level=logging.DEBUG)


def start_server():
    command = f"docker start {CONTAINER}"
    subprocess.run(command.split())
    logger.info("Started server")

def stop_server():
    command = f"docker stop {CONTAINER}"
    try:
        subprocess.check_output(command.split())
    except subprocess.CalledProcessError:
        logger.warn(f"Failed to stop server, assuming {CONTAINER} is not running")
    logger.info("Stopped server")

def players_online():
    command = f"docker exec {CONTAINER} mcstatus localhost status"
    try:
        status = subprocess.check_output(command.split())
    except subprocess.CalledProcessError:
        logger.warn(f"Failed to check mcstatus, assuming {CONTAINER} is not running")
        return False
    else:
        if "players: 0" in str(status):
            return False
    return True

def wait_for_connection():
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serversocket.bind((HOST, PORT))
    serversocket.listen(5)

    logger.info("Waiting for connection...")
    (clientsocket, address) = serversocket.accept()

    logger.info(f"Got a connection from {address}")

    clientsocket.send("Server is starting".encode("utf-8"))

    logger.debug("Closing sockets")
    clientsocket.close()
    serversocket.close()


def wait_for_empty_server():
    while players_online():
        logger.debug("Minecraft Server is active, sleeping for 300 seconds")
        time.sleep(300)
    logger.debug("Minecraft Server is not active")

def edit_motd():
    for line in fileinput.input("server.properties", inplace=True):
        if "motd=" in line:

            sys.stdout.write(f"motd=Server started at {time.strftime('%H:%M')}")


if __name__=="__main__":

    # Start the main flow
    while True:
        wait_for_empty_server()
        sys.stdout.flush()  # show log in systemd service

        stop_server()
        sys.stdout.flush()

        wait_for_connection()
        sys.stdout.flush()

        logger.debug("Wait 1 second for the port to become available")
        time.sleep(1)

        logger.debug("Editing motd")
        edit_motd()

        start_server()
        sys.stdout.flush()

        logger.debug("Wait 90 seconds for the player to join")
        time.sleep(90)
