def search(fp, key):
    with open(fp, 'r') as f:
        for line in f:
            i, j = line.rstrip("\n").split(";")
            if i==key:
                return j
            if i>key:
                break 
    return None

def dfs(nd, f):
    if not nd:
        return
    dfs(nd.left, f)
    f.write(nd.key+";"+nd.val+"\n")
    dfs(nd.right, f)

def save(n, fp):
    with open(fp, 'w') as f:
        dfs(n, f)
    return True    