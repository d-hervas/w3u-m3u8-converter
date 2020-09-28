import json
import glob
import os.path
import sys
from operator import itemgetter

def writeln(file, ln: str):
    # There has to be a built-in way to do this...right?
    return file.write(ln + '\n')

def createm3uEntry(file, tvg_id, tvg_logo, group_title, tvg_name, m3u8_link, extra_flags, user_agent):
    if (not m3u8_link):
        print("Station without url link parsed. Skipping...")
        return
    # if not tvg_id: tvg_id = tvg_name # Set default value for tvg_id. Maybe we actually don't want this though?....
    string_format = f'#EXTINF: -1 tvg-id="{tvg_id}" tvg-logo="{tvg_logo}" group-title="{group_title}" tvg-name="{tvg_name}",{tvg_name}'
    writeln(file, string_format)
    writeln(file, m3u8_link)
    if (extra_flags and user_agent):
        writeln(file, f'#EXTVLCOPT:http-user-agent={user_agent}')

print("w3u to m3u converter")
extra_flags = False
if "--extra-flags" in sys.argv:
    extra_flags = True
w3u_filenames = glob.glob("*.w3u")
if (len(w3u_filenames)):
    print("w3u files detected. Starting conversion...")
    for w3u_filename in w3u_filenames:
        print(f'Transforming {w3u_filename} ...')
        with open(w3u_filename, "r", encoding='utf-8') as w3u_file:
            m3u_filename = w3u_filename.replace("w3u", "m3u8")
            w3u = json.load(w3u_file)
            with open(m3u_filename, "w", encoding='utf-8') as m3u_file:
                # Initialize m3u file
                writeln(m3u_file, "#EXTM3U")
                for group in w3u["groups"]:
                    if (group.get("stations")):
                        group_title = group["name"]
                        for station in group["stations"]:
                            createm3uEntry(
                                m3u_file,
                                station.get("epgId"),
                                station.get("image"),
                                group_title,
                                station.get("name"),
                                station.get("url"),
                                extra_flags,
                                station.get("userAgent")
                            )
                    else:
                        createm3uEntry(
                            m3u_file,
                            group.get("epgId"),
                            group.get("image"),
                            group.get("title"),
                            group.get("name"),
                            group.get("url"),
                            extra_flags,
                            group.get("userAgent")
                        )
        print("Done!")
    print("No more files. Exiting...")
else:
    print("No w3u files detected in this folder. Exiting...")