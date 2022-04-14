import mcportscanner as mcps
import random as r
import time
import tqdm
mcps.init(False, 800)

def get_server(version, active=False):
    """
    Currently only has ApexMC's servers implemented. 
    Will get a random server of the minecraft version chosen. 
    Purpur/Paper servers will be found. Tries to avoid servers
    with mods, but if a server doesn't have Query on, it may not
    know that the server is modded. 
    """
    out = []
    results = get_passing()
    while not results[1]:
        results = get_passing()
        # print("Fetching Another Server")
        
    for i in results[1]:
       if version in i['status']['version']['name'].split():
           if active:
               if i['status']['players']['online'] == 0:
                   continue
           out.append(i)

    while not out:
        return get_server(version, active)
        
    server = r.choice(out)
    
    return (f"{results[0]}:{server['port']}", server['status']['version']['name'], f"{server['status']['players']['online']}/{server['status']['players']['max']}", server['status']['players']['online']/server['status']['players']['max'])


def get_passing():
    apex_server = r.randint(1, 9999)
    results = mcps.scan(f"{apex_server}.node.apexhosting.gdn", range(25000, 26000))

    return (f"{apex_server}.node.apexhosting.gdn", results['succeeded'])


if __name__ == "__main__":
    times = []
    results = []
    # for i in tqdm.trange(85):
    while True:
        active = input("active-only? \n?> ")
        start = time.time()
        if active == 'y':
            result = ' '.join(list(map(str, get_server("1.18.1", True))))
            print(result)
            results.append(result)
        else:
            result = ' '.join(list(map(str, get_server("1.18.1", True))))
            print(result)
            results.append(result)
        net_time = time.time() - start
        times.append(net_time)
        print(f"{round(net_time, 3)}s")
        print(f"Running Average: {sum(times)/len(times)}s")
    total = 0
    for i in times:
        total += i

    print('\n'.join(results))
        
    # print(f"Net Time: {total/len(times)}")

