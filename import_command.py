# create_json.plで出力したァイル中のjsonデータからsingularityイメージの /usr/local/bin/ に
# インストールされているコマンドのリストを抽出し、sqlite3 DBに投入する。

import sqlite3
import sys
import re
import json

def main():
    args = sys.argv
    input_file = args[1]
    db_file = args[2]
    data = read_input_file(input_file)
    insert_data(data, db_file)

def read_input_file(json_file):
    data = []
    p1 = re.compile(r'\n')
    p2 = re.compile(r'null')
    with open(json_file) as f:
        for line in f:
            if p1.match(line) or p2.match(line):
                continue
            j = json.loads(line)
            if 'image' in j:
                image = j['image']
                filepath = j['dir'] + '/' + image
                commands = j['commands']
                for command in commands:
                    data.append([command, image, filepath])
    return(data)

def insert_data(data, db_file):
    con = sqlite3.connect(db_file)
    cur = con.cursor()
    cur.execute('CREATE TABLE IF NOT EXISTS COMMAND_IMAGE_FILEPATH(command text, image text, filepath text);')
    cur.execute('CREATE INDEX IF NOT EXISTS COMMAND_INDEX ON COMMAND_IMAGE_FILEPATH(command);')
    cur.execute('CREATE INDEX IF NOT EXISTS IMAGE_INDEX ON COMMAND_IMAGE_FILEPATH(image);')
    cur.execute('CREATE INDEX IF NOT EXISTS FILEPATH_INDEX ON COMMAND_IMAGE_FILEPATH(filepath);')
    sql = 'INSERT INTO COMMAND_IMAGE_FILEPATH(command, image, filepath) values (?,?,?)'
    cur.executemany(sql, data)
    con.commit()
    con.close()

if __name__ == '__main__':
    main()
