from mcstatus import MinecraftServer
import sys
import os
import threading
import time

masscan = []

print('Multithreaded mass minecraft server status checker originally by Footsiefat/Deathmonger. \
Fork by FlareStormGaming')

# time.sleep(1)
in_file = input('What is the name of the text file with the server ips? (Including the .txt): ')
out_file = input('What is the name of the text file you want to add the ips to? (Including the .txt): ')
pub_servers = input('What is the name of the text file with the public server ips? (Including the .txt): ')
target_version = input('What version are you targeting? (Leave blank for targeting all servers): ')

outfile = open(out_file, 'a+')
outfile.close()

with open(in_file, 'r') as f:
    list_of_lines = f.readlines()

for line in list_of_lines:
    if line.strip()[0] != "#":
        masscan.append(line.strip().split(' ',4)[3])


def split_array(in_list, end):
    return [in_list[i::end] for i in range(end)]


try:
    threads = sys.argv[1]
except IndexError:
    threads = 20
    print("Using Default Thread Count (20)")

if len(masscan) < int(threads):
    threads = len(masscan)


split = list(split_array(masscan, threads))

exitFlag = 0


class MyThread (threading.Thread):
    def __init__(self, threadID, name):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name

    def run(self):
        print("Starting Thread " + self.name)
        print_time(self.name)
        print("Exiting Thread " + self.name)


def print_time(thread_name):
    for z in split[int(thread_name)]:
        if exitFlag:
            thread_name.exit()
        ip = z
        try:
            server = MinecraftServer(ip,25565)
            status = server.status()
        except Exception as e:
            print(f"Failed to get status of: {ip} with error: \n{e}")
        else:
            print("Found server: " + ip + " " + status.version.name + " " + str(status.players.online))
            if target_version in status.version.name:
                with open(out_file) as f:
                    if ip not in f.read():
                        with open(pub_servers) as g:
                            if ip not in g.read():
                                text_file = open(out_file, "a")
                                text_file.write(ip + " " + status.version.name.replace(" ", "_") + " " + str(status.players.online))
                                text_file.write(os.linesep)
                                text_file.close()


for x in range(threads):
    thread = MyThread(x, str(x)).start()
