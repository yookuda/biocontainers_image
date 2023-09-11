# 引数はcreate_json.plで出力したファイル
# create_json.plで出力したファイル中のjsonデータからコマンドにRを持つsingularityイメージを抽出し、
# 該当するsingularityイメージ中にインストールされているRパッケージのリストをテキストファイルで出力する。

import sys
import json
import re
import subprocess
import os

SCRIPT = '/home/y-okuda/biocontainers/installed_packages.R'
OUTPUT_DIR = '/home/y-okuda/biocontainers/R_package_data'

def main():
    p1 = re.compile(r'\n')
    p2 = re.compile(r'null')
    args = sys.argv
    json_file = args[1]
    images = []
    with open(json_file) as f:
        for line in f:
            if p1.match(line) or p2.match(line):
                continue
            j = json.loads(line)
            if 'R' in j['commands']:
                dir = j['dir']
                image = j['image']
                images.append([dir, image])

    for image in images:
        subdir = re.sub('/usr/local/biotools/', '', image[0])
        IMAGE_PATH = image[0] + '/' + image[1]
        OUTPUT_FILE = OUTPUT_DIR + '/' + subdir + '/' + image[1] + '.txt'
        if not os.path.isfile(OUTPUT_FILE):
            #print(IMAGE_PATH)
            subprocess.run(["singularity", "exec", IMAGE_PATH, "Rscript", SCRIPT, OUTPUT_FILE])

if __name__ == '__main__':
    main()
    
