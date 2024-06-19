import subprocess

def launch_flask_servers(number_of_servers):
    base_port = 5000

    for i in range(number_of_servers):
        port = base_port + i
        command = f"python blockchain_node.py --port={port}"
        subprocess.Popen(command, shell=True)
        print(f"Launched server on port {port}")

if __name__ == "__main__":
    number_of_servers = int(input("Enter the number of Flask servers to launch: "))
    launch_flask_servers(number_of_servers)
