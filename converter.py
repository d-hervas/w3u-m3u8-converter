import json
import glob
import os.path
from operator import itemgetter

def writeln(file, ln: str):
    # There has to be a built-in way to do this...right?
    return file.write(ln + '\n')

def createm3uEntry(file, tvg_id, tvg_logo, group_title, tvg_name, m3u8_link):
    string_format = f'#EXTINF: -1 tvg-id="{tvg_id}" tvg-logo="{tvg_logo}" group-title="{group_title}" tvg-name="{tvg_name}",{tvg_name}'
    writeln(file, string_format)
    writeln(file, m3u8_link)

print("w3u to m3u converter")
w3u_filenames = glob.glob("*.w3u")
if (len(w3u_filenames)):
    print("w3u files detected. Starting conversion...")
    for w3u_filename in w3u_filenames:
        print(f'Transforming {w3u_filename} ...')
        with open(w3u_filename, "r") as w3u_file:
            m3u_filename = w3u_filename.replace("w3u", "m3u")
            w3u = json.load(w3u_file)
            with open(m3u_filename, "w") as m3u_file:
                writeln(m3u_file, "#EXTM3U")
                for group in w3u["groups"]:
                    group_title = group["name"]
                    for station in group["stations"]:
                        createm3uEntry(m3u_file, station.get("epgId"), station.get("image"), group_title, station.get("name"), station.get("url"))
        print("Done!")
    print("No more files. Exiting...")
else:
    print("No w3u files detected in this folder. Exiting...")