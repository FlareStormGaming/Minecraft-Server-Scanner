import requests
import termcolor as tc
import threading


def ts_print(text):
  print(f"{text}\n", end='')


def print_notice(text):
  ts_print(tc.colored(text, "blue"))


def print_success(text):
  ts_print(tc.colored(text, "green", attrs=['bold']))


def print_err(text):
  ts_print(tc.colored(text, "red"))
  

def scan(ip, ports):
  out = {
    "succeeded": [],
    "failed": []
  }
  for port in ports:
    try:
      x = requests.get(f"http://{ip}:{port}")
      print_success(f"[SUCCESS] ({port}) {x}")
      out['succeeded'].append((port, x))
    except Exception as e:
      # print_err(f"[ERR] ({port}) {e}")
      # out['failed'].append((port, e))
      pass
  return out


def split_array(in_list, end):
    return [in_list[i::end] for i in range(end)]
  

class MyThread(threading.Thread):
  def __init__(self, id, ports, out, ip):
    self.id = id
    self.ports = ports
    self.out = out
    self.ip = ip
    super(MyThread, self).__init__()

  def run(self):
    # print_notice(f"[INFO] Thread {self.id} starting")
    result = scan(self.ip, self.ports)
    self.out['succeeded'].extend(result['succeeded'])
    # self.out['failed'].extend(result['failed'])
    # print_notice(f"[INFO] Thread {self.id} completed")

    
if __name__ == "__main__":
  ip = input("server: ")
  ports = split_array(range(0, 65536), 500)
  threads = []
  out = {
    "succeeded": [],
    "failed": []
  }
  for n, i in enumerate(ports):
    threads.append(MyThread(n, i, out, ip))
    threads[-1].start()

  for x in threads:
    x.join()

  print_success(f"[INFO] Connection succeeded on {len(out['succeeded'])} ports")