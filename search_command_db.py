#!/usr/bin/python3
import argparse
import subprocess

DB_PATH = '/lustre7/software/experimental/biocontainers_image/command.db'

def main():
    args = parse_args()

    if args.command:
        search_by_command(args.command)
    elif args.image:
        search_by_image(args.image)
    elif args.filepath:
        search_by_filepath(args.filepath)

def parse_args():
    parser = argparse.ArgumentParser(description='search database of biocontainer singularity image.')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-c', '--command', action='append', help='outputs the file path of the singularity image containing the specified commands.')
    group.add_argument('-i', '--image', help='outputs a list of package and version contained in the specified singularity image.')
    group.add_argument('-f', '--filepath', help='outputs a list of package and version contained in the specified file path of singularity image.')

    args = parser.parse_args()

    #print(args)
    return(args)

def search_by_command(commands):
    sql_part = []
    for command in commands:
        sql_part.append('SELECT filepath FROM COMMAND_IMAGE_FILEPATH WHERE command=\'' + command + '\'')
    sql = '"' + ' INTERSECT '.join(sql_part)  + ' ORDER BY filepath;"'
    #print(sql)
    command = 'sqlite3' + ' ' + DB_PATH + ' ' + sql
    #print(command)
    exec_subprocess(command)

def search_by_image(image):
    sql = '"' + 'SELECT command FROM COMMAND_IMAGE_FILEPATH WHERE image=\'' + image + '\' ORDER BY command;' + '"'
#    print(SQL)
    command = 'sqlite3' + ' ' + DB_PATH + ' ' + sql
#    print(COMMAND)
    exec_subprocess(command)

def search_by_filepath(filepath):
    sql = '"' + 'SELECT command FROM COMMAND_IMAGE_FILEPATH WHERE filepath=\'' + filepath + '\' ORDER BY command;' + '"'
#    print(SQL)
    command = 'sqlite3' + ' ' + DB_PATH + ' ' + sql
#    print(COMMAND)
    exec_subprocess(command)

def exec_subprocess(command):
    proc = subprocess.run(command, stdout = subprocess.PIPE, stderr = subprocess.PIPE, shell = True)
    print(proc.stdout.decode("utf8"))
    if proc.stderr:
        print(proc.stderr.decode("utf8"))

if __name__ == '__main__':
    main()

