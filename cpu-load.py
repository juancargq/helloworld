import multiprocessing
import time

def cpu_load():
    while True:
        pass

if __name__ == "__main__":
    processes = []
    for _ in range(4):  # Usa todos los ejecutores de los agentes
        p = multiprocessing.Process(target=cpu_load)
        processes.append(p)
        p.start()

    time.sleep(15)  # Generar carga durante 15 segundos
    for p in processes:
        p.terminate()