import json
import os
import platform
import shutil
import threading

MC_ASSETS = ""
MC_VERSION = ""
OUTPUT_PATH = ""
MC_OBJECT_INDEX = f""
MC_OBJECTS_PATH = f""
MC_SOUNDS = r""
threads = []


def extract_files(work):
    for fpath, fhash in work.items():
        src_fpath = os.path.normpath(f"{MC_OBJECTS_PATH}/{fhash[:2]}/{fhash}")
        dest_fpath = os.path.normpath(f"{OUTPUT_PATH}/sounds/{fpath}")
        os.makedirs(os.path.dirname(dest_fpath), exist_ok=True)
        shutil.copyfile(src_fpath, dest_fpath)


if platform.system() == "Windows":
    MC_ASSETS = os.path.expandvars(r"%APPDATA%/.minecraft/assets")
elif platform.system() == "Darwin":
    MC_ASSETS = os.path.expanduser("~/Library/Application Support/minecraft/assets")
else:
    MC_ASSETS = os.path.expanduser(r"~/.minecraft/assets")


for name in os.listdir(MC_ASSETS+"/indexes/"):
    print(name, end=", ")
inp = input("\nChoose the minecraft version to extract from: ")

if inp in os.listdir(MC_ASSETS+"/indexes"):
    MC_VERSION = inp
else:
    exit(-1)
    
threadCount = input("Enter the thread count to use for extracting: ")
threadCount = int(threadCount)

OUTPUT_PATH = os.path.normpath(os.path.expandvars(os.path.expanduser(f"~/Desktop/MC_Sounds_{MC_VERSION[:-5]}/")))


MC_OBJECT_INDEX = f"{MC_ASSETS}/indexes/{MC_VERSION}"
MC_OBJECTS_PATH = f"{MC_ASSETS}/objects"
MC_SOUNDS = r"minecraft/sounds/"


with open(MC_OBJECT_INDEX, "r") as read_file:
    data = json.load(read_file)
    sounds = {k[len(MC_SOUNDS):]: v["hash"] for (k, v) in data["objects"].items() if k.startswith(MC_SOUNDS)}
    print(f"Extracting {len(sounds)} items into {OUTPUT_PATH}.")
    thread = 0
    threadWork = [{} for i in range(threadCount)]
    print(f"Starting {threadCount} threads...")
    
    for a, b in sounds.items():
        threadWork[thread][a] = b
        
        if thread == threadCount - 1:
            thread = 0
        else:
            thread += 1
    
    for i in range(threadCount):
        t = threading.Thread(target=extract_files, args=[threadWork[i]])
        t.setDaemon(False)
        t.start()
        threads.append(t)
