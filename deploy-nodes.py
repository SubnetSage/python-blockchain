import subprocess

def launch_flask_servers(number_of_servers, base_port=5000, difficulty=4):
    for i in range(number_of_servers):
        port = base_port + i
        command = f"python blockchain_node.py --port={port} --difficulty={difficulty}"
        subprocess.Popen(command, shell=True)
        print(f"Launched server on port {port} with difficulty {difficulty}")

if __name__ == "__main__":
    number_of_servers = int(input("Enter the number of Flask servers to launch: "))
    base_port = int(input("Enter the base port number (default is 5000): ") or 5000)
    difficulty = int(input("Enter the difficulty level (default is 4): ") or 4)
    launch_flask_servers(number_of_servers, base_port, difficulty)
