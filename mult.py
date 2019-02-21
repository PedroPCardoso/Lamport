from multiprocessing import Process, Pipe
from os import getpid
from datetime import datetime

# primeiro imprime o timestamp Lamport local 
def local_time(counter):
    return ' (LAMPORT_TIME={}, LOCAL_TIME={})'.format(counter,
                                                     datetime.now())
 # calcula o novo timestamp quando um processo recebe uma mensagem . A função registra a data e hora recebido e seu contador local e incrementa.
def calc_recv_timestamp(recv_time_stamp, counter):
    return max(recv_time_stamp, counter) + 1
   #imprimi
def event(pid, counter):
    counter += 1
    print('Algo Aconteceu em {} !'.\
          format(pid) + local_time(counter))
    return counter
    #enviar nova mensagem
def send_message(pipe, pid, counter):
    counter += 1
    pipe.send(('Empty shell', counter))
    print('Mensagem enviada de' + str(pid) + local_time(counter))
    return counter
'''O evento send_message também recebe o pid e o contador como entrada, 
mas requer adicionalmente um pipe . Um Pipe é um objeto da biblioteca de multiprocessamento que representa uma conexão bidirecional entre dois processos.'''
def recv_message(pipe, pid, counter):
    message, timestamp = pipe.recv()
    counter = calc_recv_timestamp(timestamp, counter)
    print('Mensagem recebida de' + str(pid)  + local_time(counter))
    return counter

    # obtenção de seu ID de processo exclusivo 
def process_one(pipe12):
    pid = getpid()
    counter = 0
    counter = event(pid, counter)
    counter = send_message(pipe12, pid, counter)
    counter  = event(pid, counter)
    counter = recv_message(pipe12, pid, counter)
    counter  = event(pid, counter)

def process_two(pipe21, pipe23):
    pid = getpid()
    counter = 0
    counter = recv_message(pipe21, pid, counter)
    counter = send_message(pipe21, pid, counter)
    counter = send_message(pipe23, pid, counter)
    counter = recv_message(pipe23, pid, counter)


def process_three(pipe32):
    pid = getpid()
    counter = 0
    counter = recv_message(pipe32, pid, counter)
    counter = send_message(pipe32, pid, counter)

if __name__ == '__main__':
    oneandtwo, twoandone = Pipe()
    twoandthree, threeandtwo = Pipe()

    process1 = Process(target=process_one, 
                       args=(oneandtwo,))
    process2 = Process(target=process_two, 
                       args=(twoandone, twoandthree))
    process3 = Process(target=process_three, 
                       args=(threeandtwo,))

    process1.start()
    process2.start()
    process3.start()

    process1.join()
    process2.join()
    process3.join()