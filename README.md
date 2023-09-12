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
### コマンド名から singularity image を検索
#### 単一のコマンド名での検索の場合
--command または -c オプションで指定した文字列と完全一致するコマンドがインストールされている BioContainers singularity image のパスを表示する。ヒットしたすべてのイメージのパスが返ってくるため、多数のイメージにインストールされているコマンドを検索する場合は注意すること。
```
$ ./search_command_db.py -c arriba
/usr/local/biotools/a/arriba:1.0.1--h10824c4_0
/usr/local/biotools/a/arriba:1.1.0--h10824c4_0
/usr/local/biotools/a/arriba:1.1.0--h10824c4_1
/usr/local/biotools/a/arriba:1.2.0--h248197f_1
/usr/local/biotools/a/arriba:1.2.0--hc088bd4_0
/usr/local/biotools/a/arriba:1.2.0--hd2e4403_2
/usr/local/biotools/a/arriba:2.0.0--hd2e4403_0
/usr/local/biotools/a/arriba:2.0.0--hd2e4403_1
/usr/local/biotools/a/arriba:2.1.0--h3198e80_1
/usr/local/biotools/a/arriba:2.1.0--ha025227_2
/usr/local/biotools/a/arriba:2.1.0--hd2e4403_0
/usr/local/biotools/a/arriba:2.2.0--h3198e80_0
/usr/local/biotools/a/arriba:2.2.1--h3198e80_0
/usr/local/biotools/a/arriba:2.2.1--ha025227_1
/usr/local/biotools/a/arriba:2.2.1--hecb563c_2
/usr/local/biotools/a/arriba:2.3.0--ha04fe3b_1
/usr/local/biotools/a/arriba:2.3.0--haa8aa89_0
/usr/local/biotools/a/arriba:2.4.0--h0033a41_2
/usr/local/biotools/a/arriba:2.4.0--h6b7c446_1
/usr/local/biotools/a/arriba:2.4.0--ha04fe3b_0
```
#### 複数のコマンド名での検索の場合
--command または -c オプションで指定したすべてのコマンドがインストールされている BioContainers singularity image のパスを表示する。--command または -c オプションは何回でも指定できる。
```
$ ./search_command_db.py -c STAR -c rsem-prepare-reference
/usr/local/biotools/m/mulled-v2-cf0123ef83b3c38c13e3b0696a3f285d3f20f15b:606b713ec440e799d53a2b51a6e79dbfd28ecf3e-0
/usr/local/biotools/m/mulled-v2-cf0123ef83b3c38c13e3b0696a3f285d3f20f15b:64aad4a4e144878400649e71f42105311be7ed87-0
```
### イメージ名からインストールされているコマンドを検索
--image または -i オプションで指定した文字列と完全一致するファイル名の BioContainers singularity image の /usr/local/bin/ にインストールされているコマンドを表示する。
```
$ ./search_command_db.py -i arriba:2.4.0--ha04fe3b_0
2to3
2to3-3.11
R
Rscript
STAR
（中略）
zstd
zstdcat
zstdgrep
zstdless
zstdmt
```
### イメージのファイルパスからインストールされているコマンドを検索
--filepath または -f オプションで指定した文字列と一致するファイルパスの BioContainers singularity image の /usr/local/bin/ にインストールされているコマンドを表示する。
```
$ ./search_command_db.py -f /usr/local/biotools/a/arriba:2.4.0--ha04fe3b_0
2to3
2to3-3.11
R
Rscript
STAR
（中略）
zstd
zstdcat
zstdgrep
zstdless
zstdmt
```
## BioContainers にインストールされている R package の SQLite3 DB の作成
### R package 名とバージョンのファイル出力
create_json.pl で出力したファイルから R がインストールされている BioContainers singularity image を抽出し、それぞれのイメージで installed_packages.R を実行してインストールされている R package の名称とバージョンを出力する。

R を実行するには login.q のデフォルトのメモリ割り当て量である 4GB では足りないので、qlogin 時に 20GB 程度を割り当てること。
```
for i in <コマンドリスト取得実行日の日付ディレクトリ>/*.json; do python3 get_R_command_image_from_json.py $i; done
```
