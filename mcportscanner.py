# Scans all ports of a particular minecraft server.
import time

from mcstatus import JavaServer
import threading
import json
import termcolor as tc
import colorama
from pythonping import ping

colorama.init()

threads = 100
do_print = False


def init(print_out=False, thread_count=10_000):
    global do_print, threads
    do_print = print_out
    threads = thread_count


def ts_print(text):
    print(f"{text}\n", end='')


def print_notice(text):
    if __name__ == "__main__" or do_print:
        ts_print(tc.colored(text, 'blue'))


def print_success(text):
    if __name__ == "__main__" or do_print:
        ts_print(tc.colored(text, 'green', attrs=['bold']))


def print_warn(text):
    if __name__ == "__main__" or do_print:
        ts_print(tc.colored(text, 'yellow'))


class MyThread(threading.Thread):
    def __init__(self, thread_id, output_dict, function):
        threading.Thread.__init__(self)
        self.threadID = thread_id
        self.out = output_dict
        self.func = function

    def run(self):
        # print_notice("Starting Thread " + self.name)
        query_outs = self.func(self.threadID)
        self.out['failed'].extend(query_outs['failed'])
        self.out['succeeded'].extend(query_outs['succeeded'])
        # print_notice("Exiting Thread " + self.name)


def split_array(in_list, end):
    return [in_list[i::end] for i in range(end)]


def scan(ip, ports):
    try:
        ping(ip, count=1)
    except RuntimeError as e:
        if str(e).startswith('Cannot resolve address'):
            return {"failed": [], "succeeded": []}
    except:
        pass
    
    start_time = time.time()

    ports = split_array(ports, threads)

    total_out = {"failed": [], "succeeded": []}

    def query(port):
        try:
            out = {
                "success": True,
                "status": JavaServer(ip, port).status().raw,
                "error": None,
                "port": port
            }
            s = out['status']
            ver = s['version']
            print_success(
                f"Connection succeeded on port {port} ({ver['name']}) [{s['players']['online']}/{s['players']['max']}]"
            )
            return out
        except Exception as e:
            # print_notice(f"Failed to connect to port {port} with error {e}")
            return {
                "success": False,
                "status": None,
                "error": str(e),
                "port": port
            }

    def do_queries(thread_id):
        if not ports[thread_id]:
            print_warn(
                f"Thread {thread_id} has no work! Consider decreasing the thread count?"
            )
        out = {"failed": [], "succeeded": []}
        for i in ports[thread_id]:
            query_out = query(i)
            if query_out['success']:
                out['succeeded'].append(query_out)
            else:
                out['failed'].append(query_out)

        return out

    print_notice(f"Initializing {threads} threads")
    threadlist = []
    for x in range(threads):
        thread = MyThread(x, total_out, do_queries)
        threadlist.append(thread)
        thread.start()

    print_notice(f"Joining {threads} threads")
    for x in threadlist:
        x.join()

    print_notice(f"Exiting {threads} threads")
    print_notice(
        f"Scan took {round(time.time() - start_time, 3)}s to complete")

    return total_out


if __name__ == "__main__":
    target_server = input("Target Server: ")
    long_mode = input(
        "Search All? (Y is 65536 ports, N is 32767 ports) [Y/n]: ")

    if long_mode == 'n':
        print_notice("Scanning 32767 ports")
    else:
        print_notice("Scanning 65536 ports")

    if long_mode == 'n':
        scan_out = scan(target_server, range(0, 32767))
    else:
        scan_out = scan(target_server, range(0, 65536))

    with open("out.json", 'w') as f:
        f.write(json.dumps(scan_out, indent=4))

    print_notice("Wrote out.json")
