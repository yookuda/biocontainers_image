# biocontainers_image



## /usr/local/biotools/ 以下の全イメージのコマンド・共有ライブラリリストの取得
/usr/local/biotools/ 以下に配置されているすべての singularity image から、インストールされているコマンド・共有ライブラリを取得する。
```
$ mkdir biotools_image_list
$ touch biotools_image_list/dummy.txt
$ bash get_command_and_shared_library_list_qsub.sh /home/y-okuda/biocontainers/biotools_image_list/dummy.txt
```

## json ファイルの生成
get_command_and_shared_library_list_qsub.sh の実行結果から jsonファイルを生成する。
```
$ cd <実行日の日付ディレクトリ>
$ for i in $(ls biotools_*.sh.o*);do perl ../create_json.pl $i > $i.json; done
```

## コマンド・共有ライブラリリスト取得済みイメージリストの生成
get_command_and_shared_library_list_qsub.sh の実行結果から、コマンド・共有ライブラリのリストを取得した singularity image のリストを生成する。
```
$ grep "^IMAGE" <実行日の日付>/* | perl -e 'while(<>){chomp;s/^.*?biotools_(.*?)\.sh.o\d+:IMAGE:(.*)$/$1\t$2\n/;s/^([^\t]+)_/$1\//;print;}' \
> biotools_image_list/biotools_image_list_<実行日の日付>.txt
$ cp biotools_image_list/biotools_image_list_<実行日の日付>.txt biotools_image_list/biotools_image_list_merged_<実行日の日付>.txt
```

## 新規追加イメージのコマンド・共有ライブラリリストの取得
/usr/local/biotools/ 以下に新規追加された singularity image から、インストールされているコマンド・共有ライブラリを取得する。前回実行時までの singularity image リストファイルを参照して新規追加イメージを取得する。
```
$ bash get_command_and_shared_library_list_qsub.sh /home/y-okuda/biocontainers/biotools_image_list/biotools_image_list_merged_<前回の実行日の日付>.txt
```
実行結果に対し、初回と同様に json ファイルの生成・コマンド・共有ライブラリリスト取得済みイメージリストの生成を実行する。

## BioContainers にインストールされているコマンドの SQLite3 DB の作成
```
for i in <コマンドリスト取得実行日の日付ディレクトリ>/*.json; do python3 import_command.py $i command.db; done
```
### 作成されるテーブル
```
sqlite> .tables
COMMAND_IMAGE_FILEPATH
```
### スキーマ
```
sqlite> .schema
CREATE TABLE COMMAND_IMAGE_FILEPATH(command text, image text, filepath text);
CREATE INDEX COMMAND_INDEX ON COMMAND_IMAGE_FILEPATH(command);
CREATE INDEX IMAGE_INDEX ON COMMAND_IMAGE_FILEPATH(image);
CREATE INDEX FILEPATH_INDEX ON COMMAND_IMAGE_FILEPATH(filepath);
```
## コマンド検索スクリプトの使用方法
### help
```
$ ./search_command_db.py -h
usage: search_command_db.py [-h] (-c COMMAND | -i IMAGE | -f FILEPATH)
 
search database of biocontainer singularity image.
 
optional arguments:
  -h, --help            show this help message and exit
  -c COMMAND, --command COMMAND
                        outputs the file path of the singularity image
                        containing the specified command.
  -i IMAGE, --image IMAGE
                        outputs a list of commands contained in the specified
                        singularity image.
  -f FILEPATH, --filepath FILEPATH
                        outputs a list of commands contained in the specified
                        file path of singularity image.
```
