# biocontainers_image検索スクリプト

遺伝研スーパーコンピューターシステムには [BioContainers](https://biocontainers.pro/) の singularity image がインストールされています。本ツールは、このイメージ中にインストールされているコマンド名や R package 名を抽出してSQLite3 DBに格納し、コマンド名・R package名でインストールされている singularity image を検索するためのツールです。

本ツールは /lustre7/software/experimental/ に配置されています。

## コマンド検索スクリプト search_command_db.py の使用方法
search_command_db.py は SQLite3 DB (command.db) を簡易に検索するためのスクリプトです。

スクリプト中のDB_PATH変数のパスをcommand.dbの場所に合わせて変更すること。
### help
-h オプションでヘルプを表示します。
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
--command または -c オプションで指定した文字列と完全一致するコマンドがインストールされている BioContainers singularity image のパスを表示します。ヒットしたすべてのイメージのパスが返ってくるため、多数のイメージにインストールされているコマンドを検索する場合は注意すること。
```
$ ./search_command_db.py -c arriba
/usr/local/biotools/a/arriba:1.0.1--h10824c4_0
/usr/local/biotools/a/arriba:1.1.0--h10824c4_0
/usr/local/biotools/a/arriba:1.1.0--h10824c4_1
/usr/local/biotools/a/arriba:1.2.0--h248197f_1
/usr/local/biotools/a/arriba:1.2.0--hc088bd4_0
（中略）
/usr/local/biotools/a/arriba:2.3.0--ha04fe3b_1
/usr/local/biotools/a/arriba:2.3.0--haa8aa89_0
/usr/local/biotools/a/arriba:2.4.0--h0033a41_2
/usr/local/biotools/a/arriba:2.4.0--h6b7c446_1
/usr/local/biotools/a/arriba:2.4.0--ha04fe3b_0
```
#### 複数のコマンド名での検索の場合
--command または -c オプションで指定したすべてのコマンドがインストールされている BioContainers singularity image のパスを表示します。--command または -c オプションは何回でも指定できます。
```
$ ./search_command_db.py -c STAR -c rsem-prepare-reference
/usr/local/biotools/m/mulled-v2-cf0123ef83b3c38c13e3b0696a3f285d3f20f15b:606b713ec440e799d53a2b51a6e79dbfd28ecf3e-0
/usr/local/biotools/m/mulled-v2-cf0123ef83b3c38c13e3b0696a3f285d3f20f15b:64aad4a4e144878400649e71f42105311be7ed87-0
```
### イメージ名からインストールされているコマンドを検索
--image または -i オプションで指定した文字列と完全一致するファイル名の BioContainers singularity image の /usr/local/bin/ にインストールされているコマンドを表示します。
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
--filepath または -f オプションで指定した文字列と一致するファイルパスの BioContainers singularity image の /usr/local/bin/ にインストールされているコマンドを表示します。
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
## R package 検索スクリプト search_R_package_db.py の使用方法
search_R_packge_db.py は SQLite3 DB (R_package.db) 検索の簡略化のためのスクリプトです。

スクリプト中のDB_PATH変数のパスをR_package.dbの場所に合わせて変更すること。
### help
-h オプションでヘルプを表示します。
```
$ ./search_R_package_db.py -h
usage: search_R_package_db.py [-h] (-p PACKAGE | -i IMAGE | -f FILEPATH)
                              [-v VERSION]
 
search database of biocontainer singularity image.
 
optional arguments:
  -h, --help            show this help message and exit
  -p PACKAGE, --package PACKAGE
                        outputs the file path of the singularity image
                        containing the specified R package.
  -i IMAGE, --image IMAGE
                        outputs a list of package and version contained in the
                        specified singularity image.
  -f FILEPATH, --filepath FILEPATH
                        outputs a list of package and version contained in the
                        specified file path of singularity image.
  -v VERSION, --version VERSION
                        specify the version of R package.
```
### R package 名から singularity image を検索
#### バージョンを指定しない場合
--package または -p オプションで指定した文字列と完全一致する R package がインストールされている BioContainers singularity image のパスとインストールされている R package のバージョンを表示します。ヒットしたすべてのイメージのパスが返ってくるため、多数のイメージにインストールされている R package を検索する場合は注意すること。
```
$ ./search_R_package_db.py -p phangorn
2.10.0|/usr/local/biotools/f/forwardgenomics:1.0--hdfd78af_0
2.10.0|/usr/local/biotools/m/mulled-v2-e1cc45da8cd2f369a33510f9fe9edc22faa1d31b:f5d5f88daf810935d34451be63ccb080c594b940-0
2.10.0|/usr/local/biotools/r/r-enchantr:0.0.6--r42hdfd78af_0
2.10.0|/usr/local/biotools/r/rerconverge:0.3.0--r42hec16e2b_0
2.11.1|/usr/local/biotools/bioconductor/d/bioconductor-dialignr:2.6.0--r42hf17093f_1
（中略）
2.9.0|/usr/local/biotools/r/r-enchantr:0.0.5--r42hdfd78af_0
2.9.0|/usr/local/biotools/r/r-fastbaps:1.0.7--r41h5b5514e_0
2.9.0|/usr/local/biotools/r/r-fastbaps:1.0.8--r41h5b5514e_0
2.9.0|/usr/local/biotools/r/r-fastbaps:1.0.8--r42h5b5514e_1
2.9.0|/usr/local/biotools/r/r-metacoder:0.3.5--r42hecf12ef_2

```
#### バージョンを指定する場合
--package または -p オプションで R package 名を指定するとともに、--version または -v オプションで R package のバージョンを指定します。該当する R package のインストールされている BioContainers singularity image のパスが表示されます。
```
$ ./search_R_package_db.py -p phangorn -v 2.11.1
/usr/local/biotools/bioconductor/d/bioconductor-dialignr:2.6.0--r42hf17093f_1
/usr/local/biotools/bioconductor/d/bioconductor-dialignr:2.8.0--r43hf17093f_0
/usr/local/biotools/bioconductor/l/bioconductor-lymphoseq:1.28.0--r43hdfd78af_0
/usr/local/biotools/bioconductor/m/bioconductor-meskit:1.10.0--r43hdfd78af_0
/usr/local/biotools/bioconductor/m/bioconductor-metascope:1.0.0--r43hdfd78af_0
（中略）
/usr/local/biotools/r/r-mytai:0.9.3--r42hb0898b6_0
/usr/local/biotools/t/trinity:2.13.2--hff880f7_4
/usr/local/biotools/t/trinity:2.15.1--h6ab5fc9_2
/usr/local/biotools/t/trinity:2.15.1--pl5321h146fbdb_3
/usr/local/biotools/t/trycycler:0.5.4--pyhdfd78af_0

```
### イメージ名からインストールされている R package を検索
--image または -i オプションで指定した文字列と完全一致するファイル名の BioContainers singularity image にインストールされている R package とバージョンを表示します。
```
$ ./search_R_package_db.py -i bioconductor-dialignr:2.8.0--r43hf17093f_0
Biobase|2.60.0
BiocGenerics|0.46.0
DBI|1.1.3
DIAlignR|2.8.0
MASS|7.3-60
（中略）
utils|4.3.0
vctrs|0.6.3
viridisLite|0.4.2
withr|2.5.0
zoo|1.8-12

```
#### イメージのファイルパスからインストールされているコマンドを検索
--filepath または -f オプションで指定した文字列と一致するファイルパスの BioContainers singularity image にインストールされている R package 名とバージョンを表示します。
```
$ ./search_R_package_db.py -f /usr/local/biotools/bioconductor/d/bioconductor-dialignr:2.8.0--r43hf17093f_0
Biobase|2.60.0
BiocGenerics|0.46.0
DBI|1.1.3
DIAlignR|2.8.0
MASS|7.3-60
（中略）
utils|4.3.0
vctrs|0.6.3
viridisLite|0.4.2
withr|2.5.0
zoo|1.8-12

```

# 管理者によるDBメンテナンスについて
## /usr/local/biotools/ 以下の全イメージのコマンド・共有ライブラリリストの取得（初回）
/usr/local/biotools/ 以下に配置されているすべての singularity image から、インストールされているコマンド（/usr/local/bin/ 以下が対象）・共有ライブラリ（/usr/ 以下が対象）を取得します。実行日の日付（yyyymmdd）でディレクトリが生成され、ディレクトリ中に qsub で実行されるスクリプトとその実行結果が格納されます。処理の並列実行のためにUGEを使用しています。
```
$ mkdir biotools_image_list
$ touch biotools_image_list/dummy.txt
$ bash get_command_and_shared_library_list_qsub.sh /home/y-okuda/biocontainers/biotools_image_list/dummy.txt
```

## json ファイルの生成
get_command_and_shared_library_list_qsub.sh の実行結果から jsonファイルを生成します。生成されるjsonファイルはsolrへのデータ投入に使用する想定で作成しています。
```
$ cd <実行日の日付ディレクトリ>
$ for i in $(ls biotools_*.sh.o*);do perl ../create_json.pl $i > $i.json; done
```

## コマンド・共有ライブラリリスト取得済みイメージリストの生成
get_command_and_shared_library_list_qsub.sh の実行結果から、コマンド・共有ライブラリのリストを取得した singularity image のリストを生成します。このリストに記載されている singularity image はすでにデータ取得済みであるため、次回の実行時には処理が不要です。
```
$ grep "^IMAGE" <実行日の日付>/* | perl -e 'while(<>){chomp;s/^.*?biotools_(.*?)\.sh.o\d+:IMAGE:(.*)$/$1\t$2\n/;s/^([^\t]+)_/$1\//;print;}' \
> biotools_image_list/biotools_image_list_<実行日の日付>.txt
$ cp biotools_image_list/biotools_image_list_<実行日の日付>.txt biotools_image_list/biotools_image_list_merged_<実行日の日付>.txt
```

## 新規追加イメージのコマンド・共有ライブラリリストの取得（2回目以降）
新規に生成された BioContainers の singularity image は毎週 /usr/local/biotools/ 以下にインストールされます。新規追加された singularity image から、インストールされているコマンド・共有ライブラリを取得します。前回実行時までの singularity image リストファイルを参照して、リストに存在しないイメージからデータを取得します。
```
$ bash get_command_and_shared_library_list_qsub.sh /home/y-okuda/biocontainers/biotools_image_list/biotools_image_list_merged_<前回の実行日の日付>.txt
```
この後、実行結果に対し初回と同様に json ファイルの生成を行います。

## コマンド・共有ライブラリリスト取得済みイメージリストの更新
新規追加された singularity image のリストを生成し、データ取得済みの singularity image リストを更新します。
```
$ grep "^IMAGE" <今回実行時の日付>/* | perl -e 'while(<>){chomp;s/^.*?biotools_(.*?)\.sh.o\d+:IMAGE:(.*)$/$1\t$2\n/;s/^([^\t]+)_/$1\//;print;}' \
> biotools_image_list/biotools_image_list_<今回実行時の日付>.txt
$ cat biotools_image_list/biotools_image_list_merged_<前回実行時の日付>.txt biotools_image_list/biotools_image_list_<今回実行時の日付>.txt | sort \
> biotools_image_list/biotools_image_list_merged_<今回実行時の日付>.txt
```
biotools_image_list/biotools_image_list_merged_<今回実行時の日付>.txt がデータ取得済みの全イメージのリストになります。

## BioContainers にインストールされているコマンドの SQLite3 DB の作成
create_json.pl で生成した json ファイルからデータを取り出し、SQLite3 DB (command.db) を作成します。
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
## BioContainers singularity image にインストールされている R package の SQLite3 DB の作成
### R package 名とバージョンのファイル出力
create_json.pl で出力したファイルから R がインストールされている BioContainers singularity image を抽出し、それぞれのイメージで installed_packages.R を実行してインストールされている R package の名称とバージョンを出力します。

R を実行するには login.q のデフォルトのメモリ割り当て量である 4GB では足りないので、qlogin 時に 20GB 程度を割り当てること。

BASE変数のパスを実行環境に合わせて変更すること。
```
for i in <コマンドリスト取得実行日の日付ディレクトリ>/*.json; do python3 get_R_command_image_from_json.py $i; done
```
### SQLite3 DBの作成
get_R_command_image_from_json.py が出力したファイルを import_R_package_data.py に渡してデータを SQLite3 DB (R_package.db) に投入します。R_package_data ディレクトリ以下は実行日ごとに分割されていないため、 find コマンドを使って対象ファイルを抽出し、 xargs で import_R_package_data.py に渡します。
```
find R_package_data -mtime -1 -name '*.txt' | xargs -I {original} python3 import_R_package_data.py {original} R_package.db
```
#### 作成されるテーブル
```
sqlite> .tables
PACKAGE_VERSION                 PACKAGE_VERSION_IMAGE_FILEPATH
```
### スキーマ
```
sqlite> .schema
CREATE TABLE PACKAGE_VERSION(package text, version text, PRIMARY KEY(package, version));
CREATE TABLE PACKAGE_VERSION_IMAGE_FILEPATH(package text, version text, image text, filepath text, PRIMARY KEY(package, image));
CREATE INDEX PACKAGE_INDEX ON PACKAGE_VERSION_IMAGE_FILEPATH(package);
CREATE INDEX IMAGE_INDEX ON PACKAGE_VERSION_IMAGE_FILEPATH(image);
CREATE INDEX FILEPATH_INDEX ON PACKAGE_VERSION_IMAGE_FILEPATH(filepath);
```
