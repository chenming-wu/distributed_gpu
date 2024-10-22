import subprocess
import time

def execute_commands_in_batches_nonblock(file_path, batch_size=4, n_proc_per_gpu=4):
    with open(file_path, 'r') as file:
        commands = file.readlines()

    processes = []
    gpu_count = 4  # 假设你有 4 个 GPU

    while commands or processes:
        # 填充空闲的 GPU
        for gpu_id in range(gpu_count):
            # 计算当前 GPU 上正在运行的进程数量
            current_processes = [p for p in processes if p.gpu_id == gpu_id]
            if len(current_processes) < n_proc_per_gpu and commands:
                command = commands.pop(0).strip()  # 从命令列表中取出一个命令
                full_command = f"CUDA_VISIBLE_DEVICES={gpu_id} {command}"
                print(f"Executing on GPU {gpu_id}: {full_command}")
                process = subprocess.Popen(full_command, shell=True)
                process.gpu_id = gpu_id  # 将 GPU ID 关联到进程
                processes.append(process)

        # 检查已完成的进程
        for process in processes[:]:  # 使用切片来避免修改列表时出错
            if process.poll() is not None:  # 如果进程已完成
                print(f"Process {process.pid} on GPU {process.gpu_id} finished.")
                processes.remove(process)  # 从进程列表中移除

        time.sleep(0.5)  # 每隔一段时间检查进程状态

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
