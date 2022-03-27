from mcstatus import MinecraftServer
import sys
import os
import threading

masscan = []

print('Multithreaded mass minecraft server status checker originally by Footsiefat/Deathmonger. \
Fork by FlareStormGaming')

# time.sleep(1)
in_file = "masscan.txt"  # input('What is the name of the text file with the server ips? (Including the .txt): ')
out_file = "out.txt"  # input('What is the name of the text file you want to add the ips to? (Including the .txt): ')
pub_servers = "public.txt"  # input('What is the name of the text file with the public server ips? (Including the .txt): ')
target_version = input('What version are you targeting? (Leave blank to target all servers): ')

outfile = open(out_file, 'a+')
outfile.close()

with open(in_file, 'r') as f:
    list_of_lines = f.readlines()

for line in list_of_lines:
    if line.strip()[0] != "#":
        masscan.append(line.strip().split(' ', 4)[3])


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


class MyThread(threading.Thread):
    def __init__(self, threadID, name):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name

    def run(self):
        print("Starting Thread " + self.name)
        print_time(self.name)
        print("Exiting Thread " + self.name)


with open(pub_servers) as f:
    public_servers = f.read()


def print_time(thread_name):
    for z in split[int(thread_name)]:
        if exitFlag:
            thread_name.exit()
        ip = z
        try:
            # Create Server using mcstatus.MinecraftServer class
            server = MinecraftServer(ip, 25565)

            # Attempt to obtain the status of the server.
            status = server.status()
        except Exception as e:
            # Print error when fail to obtain server's status.
            print(f"Failed to get status of: {ip} with error: \n{e}")
        else:
            # If the server's status was found without an exception, print it.
            print("Found server.",
                  f"\n    IP: {ip}\n    Version: {status.version.name}\n    {status.players.online} Players Online",
                  "\n----")

            # Checking whether the server matches specified options, and if yes writing it to out_file.
            if target_version in status.version.name:
                with open(out_file, 'r') as f:
                    if ip in f.read() or ip in public_servers:
                        continue

                with open(out_file, 'a') as f:
                    f.write(ip + " " + status.version.name.replace(" ", "_") + " " +
                            str(status.players.online))
                    f.write(os.linesep)


for x in range(threads):
    thread = MyThread(x, str(x)).start()
