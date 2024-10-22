import subprocess
import time

def execute_commands_in_batches_nonblock(file_path, batch_size=8):
    with open(file_path, 'r') as file:
        commands = file.readlines()

    processes = []

    for i in range(0, len(commands), batch_size):
        batch = commands[i:i + batch_size]

        for index, command in enumerate(batch):
            gpu_id = index % batch_size
            full_command = f"CUDA_VISIBLE_DEVICES={gpu_id % 4} {command.strip()}"
            print(f"Executing: {full_command}")
            process = subprocess.Popen(full_command, shell=True)
            processes.append(process)

        # Check and clean up completed processes
        while processes:
            for process in processes[:]:  # Iterate over a copy of the list
                if process.poll() is not None:  # Process has finished
                    processes.remove(process)  # Remove it from the list
            time.sleep(1)  # Sleep a bit before checking again

    # Ensure all processes are finished before exiting the function
    for process in processes:
        process.wait()

def execute_commands_in_batches(file_path, batch_size=16):
    with open(file_path, 'r') as file:
        commands = file.readlines()

    for i in range(0, len(commands), batch_size):
        batch = commands[i:i + batch_size]
        processes = []

        for index, command in enumerate(batch):
            gpu_id = index % batch_size
            full_command = f"NPU_VISIBLE_DEVICES={gpu_id} {command.strip()}"
            print(f"Executing: {full_command}") 
            process = subprocess.Popen(full_command, shell=True)
            processes.append(process)

        for process in processes:
            process.wait()

if __name__ == "__main__":
    execute_commands_in_batches('commands.txt')
