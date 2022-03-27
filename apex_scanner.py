import mcportscanner as mcps
import termcolor as tc
import json
import requests
from pythonping import ping

mcps.init(print_out=True, thread_count=1000)

servers = {}

# scan all <number>.node.apexhosting.gdn IPs
for i in range(0, 10000):
    print(tc.colored(f"Scanning Apex Server {i} ({i}.node.apexhosting.gdn)", 'blue'))
    try:
        ping_result = ping(f"{i}.node.apexhosting.gdn", size=1, count=1)
        print(ping_result._responses[0].error_message)
    except RuntimeError:
        print(tc.colored(f"Apex Server {i}'s address cannot be resolved. ", 'red'))
        with open("apex_unreachable.txt", 'w+') as f:
            f.write(f.read() + f"\n{i}.node.apexhosting.gdn")
    except PermissionError:
        servers[f'{i}.node.apexhosting.gdn'] = mcps.scan(f"{i}.node.apexhosting.gdn", range(25000, 26000))['succeeded']

with open("apex_servers.json", 'w') as f:
    f.write(json.dumps(servers, indent=4))
