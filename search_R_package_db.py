#!/usr/bin/python3
import argparse
import subprocess

DB_PATH = '/lustre7/software/experimental/biocontainers_image/R_package.db'

def main():
    args = parse_args()

    if args.package:
        if args.version:
            search_by_package_with_version(args.package, args.version)
        else:
            search_by_package(args.package)
    elif args.image:
        search_by_image(args.image)
    elif args.filepath:
        search_by_filepath(args.filepath)

def parse_args():
    parser = argparse.ArgumentParser(description='search database of biocontainer singularity image.')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-p', '--package', help='outputs the file path of the singularity image containing the specified R package.')
    group.add_argument('-i', '--image', help='outputs a list of package and version contained in the specified singularity image.')
    group.add_argument('-f', '--filepath', help='outputs a list of package and version contained in the specified file path of singularity image.')
    parser.add_argument('-v', '--version', help='specify the version of R package.')

    args = parser.parse_args()
    if args.version and args.image or args.version and args.filepath:
        print("error on dependency. --version option can use only with --package option.")

    #print(args)
    return(args)

def search_by_package(package):
    sql = '"' + 'SELECT version, filepath FROM PACKAGE_VERSION_IMAGE_FILEPATH WHERE package=\'' + package + '\' ORDER BY version, filepath;' + '"'
    #print(sql)
    command = 'sqlite3' + ' ' + DB_PATH + ' ' + sql
    #print(command)
    exec_subprocess(command)

def search_by_package_with_version(package, version):
    sql = '"' + 'SELECT filepath FROM PACKAGE_VERSION_IMAGE_FILEPATH WHERE package=\'' + package + '\' AND version=\'' + version + '\' ORDER BY filepath;' + '"'
    #print(sql)
    command = 'sqlite3' + ' ' + DB_PATH + ' ' + sql
    #print(command)
    exec_subprocess(command)
    

def search_by_image(image):
    sql = '"' + 'SELECT package, version FROM PACKAGE_VERSION_IMAGE_FILEPATH WHERE image=\'' + image + '\' ORDER BY package, version;' + '"'
#    print(SQL)
    command = 'sqlite3' + ' ' + DB_PATH + ' ' + sql
#    print(COMMAND)
    exec_subprocess(command)

def search_by_filepath(filepath):
    sql = '"' + 'SELECT package, version FROM PACKAGE_VERSION_IMAGE_FILEPATH WHERE filepath=\'' + filepath + '\' ORDER BY package, version;' + '"'
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

