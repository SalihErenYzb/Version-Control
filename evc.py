import os
import hashlib
import shutil
import ctypes
import sys
# iter , hashing 
# helper functions
def hashAll(sha256_hash,path):
    for file in sorted(os.listdir(path)):
        if file == ".EVC":
            continue
        sha256_hash.update(file.encode())
        new = path + "/" + file
        if os.path.isdir(new):
            sha256_hash = hashAll(sha256_hash,new)
        else:
            with open(new,"rb") as f:
                for chunk in iter(lambda: f.read(4096),b""):
                    sha256_hash.update(chunk)
    return sha256_hash
def hashEveryFile(path):
    sha256_hash = hashlib.sha256()
    sha256_hash = hashAll(sha256_hash,path)
    return sha256_hash.hexdigest()
def copyDir(main,toCopy):
    for file in sorted(os.listdir(main)):
        if file == ".EVC":
            continue
        new =  main + "/" + file
        newCopy = toCopy+"/"+file
        if os.path.isdir(new):
            if not(file in os.listdir(toCopy)):
                os.mkdir(newCopy)
            copyDir(new,newCopy)
        else:
            shutil.copy2(new,newCopy)
def deleteDir(path):
    for file in sorted(os.listdir(path)):
        if file == ".EVC":
            continue
        new =  path + "/" + file
        if os.path.isdir(new):
            deleteDir(new)
            os.rmdir(new)
        else:
            os.remove(new)
#main functions
def init():
    # if .EVC exists give error
    #create .EVC  and data.txt and put head: None inside data.txt
    curr = os.getcwd()
    repo = curr+"/.EVC"
    assert not(".EVC" in os.listdir() and os.path.isdir(repo)) , "Current directory is already initiliazed!"
    os.mkdir(repo)
    data = repo + "/data.txt"
    with open(data,"w") as f:
        f.write("head: None\n")
        f.close()
    # make it hidden
    ab = os.path.abspath(repo)
    FILE_ATTRIBUTE_HIDDEN = 0x02
    ctypes.windll.kernel32.SetFileAttributesW(ab, FILE_ATTRIBUTE_HIDDEN)
    print("Succesfully initiliazed a repository!")
def commit(message = "no message"):
    # check if .EVC exists
    # first hash every file and every file inside folders except .EVS and make sure it is not the same hash as head
    # then just copy every file and folder to a folder with hash name inside .EVC
    curr = os.getcwd()
    repo = curr+"/.EVC"
    assert (".EVC" in os.listdir() and os.path.isdir(repo)) , "Current directory is not initiliazed!"
    hash = hashEveryFile(curr)
    assert not(hash in os.listdir(repo)) , f"A commit with hash {hash} already exists!" 
    os.mkdir(repo+"/"+hash)
    copyDir(curr,repo+"/"+hash)
    #shutil.make_archive(repo+"/"+hash,"zip",repo+"/"+hash)
    with open(repo+"/data.txt","r") as f:
        f.readline()
        data  = f.read()
    with open(repo+"/data.txt","w") as f:
        f.write("head: "+ hash+"\n")
        f.write(hash+" " +message+"\n")
        f.write(data)
    print("Succesfully committed with hash: ",hash)
def jump(hash):
    # check if .EVC exists
    # delete every file and folder except .EVS and move inside of folder with name hash to current dir
    curr = os.getcwd()
    repo = curr+"/.EVC"
    assert (".EVC" in os.listdir() and os.path.isdir(repo)) , "Current directory is not initiliazed!"
    assert (hash in os.listdir(repo)) , "Given hash does not exist in current repo"
    deleteDir(curr)
    copyDir(repo+"/"+hash,curr)
    print("Succesfully jumped to commit with hash: ",hash)
def head():
    # goes to head hash
    curr = os.getcwd()
    repo = curr+"/.EVC"
    assert (".EVC" in os.listdir() and os.path.isdir(repo)) , "Current directory is not initiliazed!"
    data = repo + "/data.txt"
    with open(data,"r") as f:
        line = f.readline().split()
        assert line[1] != None,"This repository has no commits!"
        jump(line[1])
    print("Succesfully jumped to head commit with hash: ",line[1])
def info(limit = 10):
    curr = os.getcwd()
    repo = curr+"/.EVC"
    assert (".EVC" in os.listdir() and os.path.isdir(repo)) , "Current directory is not initiliazed!"
    with open(os.getcwd()+"/.EVC/data.txt","r") as f:
        print(f.readline(),end="")
        for i in range(limit):
            data = f.readline()
            print(data,end="")
            if data == "":
                break
def delRepo():
    curr = os.getcwd()
    repo = curr+"/.EVC"
    assert (".EVC" in os.listdir() and os.path.isdir(repo)) , "Can not delete non-existing repo"
    deleteDir(repo)
    os.rmdir(repo)
    print("Succesfully deleted existing repo!")
def randomCommit():
    # makes a commit that is different than last by changing the inside of random.txt
    # purely for testing
    curr = os.getcwd()
    repo = curr+"/.EVC"
    assert (".EVC" in os.listdir() and os.path.isdir(repo)) , "Current directory is not initiliazed!"
    if "random.txt" not in os.listdir(curr):
        with open("random.txt","w") as f:
            f.write("random")
    with open("random.txt","r") as f:
        data = str(f.read())
        sha256_hash = hashlib.sha256()
        sha256_hash.update(data.encode())
    with open("random.txt","w") as f:
        f.write(sha256_hash.hexdigest())
    commit("random")
if __name__ == "__main__":
    first = sys.argv[1]
    if first == "random":
        randomCommit()
    elif first == "delRepo":
        delRepo()
    elif first == "info":
        if len(sys.argv)>2:
            limit = sys.argv[2]
            limit = int(limit)
            info(limit)
        else:
            info()
    elif first == "head":
        head()
    elif first == "init":
        init()
    elif first == "jump":
        hash = sys.argv[2]
        jump(hash)
    elif first == "commit":
        if len(sys.argv) > 2:
            message = sys.argv[2]
            commit(message)
        else:
            commit()
    else:
        print("Error: '"+first + "'is not a valid command!")
