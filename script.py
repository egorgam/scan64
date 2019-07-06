import subprocess, json

def arpscan(param):
    l = []
    for i in param[0]:
        if i.split()[-1] == "FAILED":
            d = {"addr" + str(param[1]): i.split()[0], "interface": i.split()[2], "macaddr": None, "type": None, "status": i.split()[3]}
        else:
            d = {"addr" + str(param[1]): i.split()[0], "interface": i.split()[2], "macaddr": i.split()[4], "type": i.split()[3], "status": i.split()[5]}

        l.append(d)

    return(l)

def proc(ipv):
   return(subprocess.run(["ip", "-" + str(ipv), "neigh"], stdout=subprocess.PIPE).stdout.decode('utf-8').strip().split('\n'), ipv)

def local(ipv):
   return(subprocess.run(["ip", "-" + str(ipv), "addr"], stdout=subprocess.PIPE).stdout.decode('utf-8').strip().replace("forever", "").split('preferred_lft'), ipv)


try:
    dev4 = local(4)
    dev6 = local(6)

    list4 = arpscan(proc(4))
    list6 = arpscan(proc(6))

    for i in dev6[0]:
        if len(i.split()) > 0:
            print(i.split()[10])

except Exception as e:
    print(e)
    print('no ipv4 both ipv6 addresses founded')


result = []
for i in list6:
    if i["status"] != "FAILED":
        for k in list4:
            if k["status"] != "FAILED":
                if k["macaddr"] == i["macaddr"]:
                    result.append({**i, **{"addr4": k["addr4"]}})
    else:
        result.append({**i, **{"addr4": None}})


h = []
for i in set([u["interface"] for u in result]):
    f = []
    for r in result:
        if r["interface"] == i:
            f.append({"addr4": r["addr4"], "addr6": r["addr6"], "macaddr": r["macaddr"], "type":r["type"], "status": r["status"]})
    h.append({i: f})

for z in h:
    print(json.dumps(z, indent=4, sort_keys=True))
