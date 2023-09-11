import sqlite3
import sys
import re

def main():
    args = sys.argv
    input_file = args[1]
    db_file = args[2]
    #dir_name = args[3]
    data = read_input_file(input_file)
    insert_data(data, db_file)

def read_input_file(input_file):
    p1 = re.compile(r'\s+')
    p2 = re.compile(r'\s+.*Version')
    p3 = re.compile(r'"(.*)"')
    p4 = re.compile(r'^R_package_data/(.*)/[^/]+.txt$')
    dir_name = ''
    if p4.match(input_file):
        m = p4.match(input_file)
        dir_name = m.group(1)
    #print(dir_name)
    flag = 0
    data = []
    package_data = {}
    with open(input_file) as f:
        for line in f:
            if flag == 0 and p1.match(line):
                flag = 1
                if p2.match(line):
                    flag = 2
                continue
            if flag == 1 and p2.match(line):
                flag = 2
                continue
            if flag == 1 and p1.match(line):
                continue
            if flag == 2 and p1.match(line):
                break
            if flag:
                line_data = re.split(r'\s+', line)
                package = line_data[0]
                if package not in package_data:
                    package_data[package] = []
                for each_data in line_data:
                    if p3.match(each_data):
                        m = p3.match(each_data)
                        package_data[package].append(m.group(1))
    for package in package_data:
        image = re.sub('.*/', '', input_file)
        image = re.sub('\.txt', '', image)
        filepath = '/usr/local/biotools/' + dir_name + '/' + image
        data.append([package_data[package][0], package_data[package][2], image, filepath])
    return(data)

def insert_data(data, db_file):
    data1 = []
    for each_data in data:
        data1.append([each_data[0], each_data[1]])
    con = sqlite3.connect(db_file)
    cur = con.cursor()
    cur.execute('CREATE TABLE IF NOT EXISTS PACKAGE_VERSION(package text, version text, PRIMARY KEY(package, version));')
    cur.execute('CREATE TABLE IF NOT EXISTS PACKAGE_VERSION_IMAGE_FILEPATH(package text, version text, image text, filepath text, PRIMARY KEY(package, image));')
    cur.execute('CREATE INDEX IF NOT EXISTS PACKAGE_INDEX ON PACKAGE_VERSION_IMAGE_FILEPATH(package);')
    cur.execute('CREATE INDEX IF NOT EXISTS IMAGE_INDEX ON PACKAGE_VERSION_IMAGE_FILEPATH(image);')
    cur.execute('CREATE INDEX IF NOT EXISTS FILEPATH_INDEX ON PACKAGE_VERSION_IMAGE_FILEPATH(filepath);')
    sql1 = 'INSERT OR IGNORE INTO PACKAGE_VERSION(package, version) values (?,?)'
    sql2 = 'INSERT OR IGNORE INTO PACKAGE_VERSION_IMAGE_FILEPATH(package, version, image, filepath) values (?,?,?,?)'
    cur.executemany(sql1, data1)
    cur.executemany(sql2, data)
    con.commit()
    con.close()

if __name__ == '__main__':
    main()
