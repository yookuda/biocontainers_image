# biocontainers_image

[BioContainers](https://biocontainers.pro/) の singularity image にインストールされているコマンド名や R package 名を抽出してSQLite3 DBに格納し、コマンド名・R package名でインストールされている singularity image を検索するためのツールです。

## /usr/local/biotools/ 以下の全イメージのコマンド・共有ライブラリリストの取得
/usr/local/biotools/ 以下に配置されているすべての singularity image から、インストールされているコマンド（/usr/local/bin/ 以下が対象）・共有ライブラリ（/usr/ 以下が対象）を取得します。実行日の日付（yyyymmdd）でディレクトリが生成され、ディレクトリ中に qsub で実行されるスクリプトとその実行結果が格納されます。
```
$ mkdir biotools_image_list
$ touch biotools_image_list/dummy.txt
$ bash get_command_and_shared_library_list_qsub.sh /home/y-okuda/biocontainers/biotools_image_list/dummy.txt
```

## json ファイルの生成
get_command_and_shared_library_list_qsub.sh の実行結果から jsonファイルを生成します。生成されるjsonファイルはsolrへのデータ投入に使用する想定で作成したものです。
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

## 新規追加イメージのコマンド・共有ライブラリリストの取得
/usr/local/biotools/ 以下に新規追加された singularity image から、インストールされているコマンド・共有ライブラリを取得します。前回実行時までの singularity image リストファイルを参照して、リストに存在しないイメージからデータを取得します。
```
$ bash get_command_and_shared_library_list_qsub.sh /home/y-okuda/biocontainers/biotools_image_list/biotools_image_list_merged_<前回の実行日の日付>.txt
```
この後、実行結果に対し初回と同様に json ファイルの生成・コマンド・共有ライブラリリスト取得済みイメージリストの生成を実行します。

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
## コマンド検索スクリプトの使用方法
search_command_db.py は SQLite3 DB (command.db) 検索の簡略化のためのスクリプトです。
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
## BioContainers にインストールされている R package の SQLite3 DB の作成
### R package 名とバージョンのファイル出力
create_json.pl で出力したファイルから R がインストールされている BioContainers singularity image を抽出し、それぞれのイメージで installed_packages.R を実行してインストールされている R package の名称とバージョンを出力します。

R を実行するには login.q のデフォルトのメモリ割り当て量である 4GB では足りないので、qlogin 時に 20GB 程度を割り当てること。
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
## R package 検索スクリプトの使用方法
search_R_packge_db.py は SQLite3 DB (R_package.db) 検索の簡略化のためのスクリプトです。
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
2.11.1|/usr/local/biotools/bioconductor/d/bioconductor-dialignr:2.8.0--r43hf17093f_0
2.11.1|/usr/local/biotools/bioconductor/l/bioconductor-lymphoseq:1.28.0--r43hdfd78af_0
2.11.1|/usr/local/biotools/bioconductor/m/bioconductor-meskit:1.10.0--r43hdfd78af_0
2.11.1|/usr/local/biotools/bioconductor/m/bioconductor-metascope:1.0.0--r43hdfd78af_0
2.11.1|/usr/local/biotools/bioconductor/p/bioconductor-philr:1.26.0--r43hdfd78af_0
2.11.1|/usr/local/biotools/bioconductor/s/bioconductor-sangeranalyser:1.10.0--r43hdfd78af_0
2.11.1|/usr/local/biotools/bioconductor/t/bioconductor-tanggle:1.6.0--r43hdfd78af_0
2.11.1|/usr/local/biotools/m/mulled-v2-a4567890af2fd72603a7a44467e8278013842caa:934d292424738a426a835e7f69ec5a4eeab9a22f-0
2.11.1|/usr/local/biotools/r/r-dowser:1.2.0--r42h3121a25_0
2.11.1|/usr/local/biotools/r/r-enchantr:0.1.0--r42hdfd78af_0
2.11.1|/usr/local/biotools/r/r-enchantr:0.1.0--r42hdfd78af_1
2.11.1|/usr/local/biotools/r/r-enchantr:0.1.0--r42hdfd78af_2
2.11.1|/usr/local/biotools/r/r-enchantr:0.1.1--r42hdfd78af_0
2.11.1|/usr/local/biotools/r/r-enchantr:0.1.2--r42hdfd78af_0
2.11.1|/usr/local/biotools/r/r-enchantr:0.1.3--r42hdfd78af_0
2.11.1|/usr/local/biotools/r/r-fastbaps:1.0.8--r42h43eeafb_2
2.11.1|/usr/local/biotools/r/r-fastbaps:1.0.8--r43h43eeafb_3
2.11.1|/usr/local/biotools/r/r-metacoder:0.3.6--r42h21a89ab_2
2.11.1|/usr/local/biotools/r/r-metacoder:0.3.6--r42hecf12ef_0
2.11.1|/usr/local/biotools/r/r-metacoder:0.3.6--r42hecf12ef_1
2.11.1|/usr/local/biotools/r/r-metacoder:0.3.6--r43h21a89ab_3
2.11.1|/usr/local/biotools/r/r-mytai:0.9.3--r42hb0898b6_0
2.11.1|/usr/local/biotools/t/trinity:2.13.2--hff880f7_4
2.11.1|/usr/local/biotools/t/trinity:2.15.1--h6ab5fc9_2
2.11.1|/usr/local/biotools/t/trinity:2.15.1--pl5321h146fbdb_3
2.11.1|/usr/local/biotools/t/trycycler:0.5.4--pyhdfd78af_0
2.2.0|/usr/local/biotools/bioconductor/p/bioconductor-philr:1.4.0--r3.4.1_0
2.2.0|/usr/local/biotools/f/frogs:2.0.1--py27_0
2.2.0|/usr/local/biotools/r/r-phangorn:2.2.0--r3.4.1_0
2.3.1|/usr/local/biotools/bioconductor/p/bioconductor-philr:1.6.0--r341_0
2.3.1|/usr/local/biotools/r/r-phytools:0.6_44--r3.4.1_0
2.3.1|/usr/local/biotools/r/r-phytools:0.6_44--r341_1
2.3.1|/usr/local/biotools/r/r-phytools:0.6_60--r341h6115d3f_0
2.3.1|/usr/local/biotools/r/r-poppr:2.8.1--r341h470a237_0
2.4.0|/usr/local/biotools/bioconductor/l/bioconductor-lymphoseq:1.10.0--r351_0
2.4.0|/usr/local/biotools/bioconductor/p/bioconductor-philr:1.6.0--r351_0
2.4.0|/usr/local/biotools/bioconductor/p/bioconductor-philr:1.8.1--r351_0
2.4.0|/usr/local/biotools/f/frogs:3.1.0--py27_0
2.4.0|/usr/local/biotools/r/r-phangorn:2.4.0--r341h9d2a408_0
2.4.0|/usr/local/biotools/r/r-phangorn:2.4.0--r351h9d2a408_0
2.4.0|/usr/local/biotools/r/r-phytools:0.6_60--r351h6115d3f_0
2.4.0|/usr/local/biotools/r/r-poppr:2.8.1--r351h14c3975_1
2.4.0|/usr/local/biotools/r/r-poppr:2.8.1--r351h470a237_0
2.5.3|/usr/local/biotools/bioconductor/p/bioconductor-philr:1.10.0--r351_0
2.5.3|/usr/local/biotools/r/r-phytools:0.6_60--r351h6115d3f_2
2.5.3|/usr/local/biotools/r/r-poppr:2.8.2--r351h14c3975_0
2.5.5|/usr/local/biotools/bioconductor/l/bioconductor-lymphoseq:1.12.0--r36_1
2.5.5|/usr/local/biotools/bioconductor/l/bioconductor-lymphoseq:1.14.0--r36_0
2.5.5|/usr/local/biotools/bioconductor/l/bioconductor-lymphoseq:1.16.0--r40_0
2.5.5|/usr/local/biotools/bioconductor/l/bioconductor-lymphoseq:1.18.0--r40_0
2.5.5|/usr/local/biotools/bioconductor/m/bioconductor-meskit:0.99.16--r40_0
2.5.5|/usr/local/biotools/bioconductor/m/bioconductor-meskit:1.0.0--r40_0
2.5.5|/usr/local/biotools/bioconductor/m/bioconductor-microbiotaprocess:1.0.3--r40_0
2.5.5|/usr/local/biotools/bioconductor/m/bioconductor-microbiotaprocess:1.2.0--r40_0
2.5.5|/usr/local/biotools/bioconductor/p/bioconductor-philr:1.10.0--r36_1
2.5.5|/usr/local/biotools/bioconductor/p/bioconductor-philr:1.12.0--r36_0
2.5.5|/usr/local/biotools/bioconductor/p/bioconductor-philr:1.14.0--r40_0
2.5.5|/usr/local/biotools/bioconductor/p/bioconductor-philr:1.16.0--r40_0
2.5.5|/usr/local/biotools/bioconductor/s/bioconductor-sangeranalyser:1.0.0--r40_0
2.5.5|/usr/local/biotools/c/coinfinder:1.0.0--py36h78a066a_0
2.5.5|/usr/local/biotools/c/coinfinder:1.0.0--py36h78a066a_1
2.5.5|/usr/local/biotools/c/coinfinder:1.0.0--py36h78a066a_2
2.5.5|/usr/local/biotools/c/coinfinder:1.0.0--py36h78a066a_3
2.5.5|/usr/local/biotools/c/coinfinder:1.0.0--py37h78a066a_0
2.5.5|/usr/local/biotools/c/coinfinder:1.0.0--py37h78a066a_1
2.5.5|/usr/local/biotools/c/coinfinder:1.0.0--py37h78a066a_2
2.5.5|/usr/local/biotools/c/coinfinder:1.0.0--py37h78a066a_3
2.5.5|/usr/local/biotools/c/coinfinder:1.0.1--py36h78a066a_0
2.5.5|/usr/local/biotools/c/coinfinder:1.0.1--py37h78a066a_0
2.5.5|/usr/local/biotools/c/coinfinder:1.0.2--py36h78a066a_0
2.5.5|/usr/local/biotools/c/coinfinder:1.0.2--py36h78a066a_1
2.5.5|/usr/local/biotools/c/coinfinder:1.0.2--py37h78a066a_0
2.5.5|/usr/local/biotools/c/coinfinder:1.0.2--py37h78a066a_1
2.5.5|/usr/local/biotools/c/coinfinder:1.0.3--py36h78a066a_0
2.5.5|/usr/local/biotools/c/coinfinder:1.0.3--py37h78a066a_0
2.5.5|/usr/local/biotools/c/coinfinder:1.0.4--py36h78a066a_0
2.5.5|/usr/local/biotools/c/coinfinder:1.0.4--py36h78a066a_1
2.5.5|/usr/local/biotools/c/coinfinder:1.0.4--py36hc27cf86_2
2.5.5|/usr/local/biotools/c/coinfinder:1.0.4--py37h6b63d35_2
2.5.5|/usr/local/biotools/c/coinfinder:1.0.4--py37h78a066a_0
2.5.5|/usr/local/biotools/c/coinfinder:1.0.4--py37h78a066a_1
2.5.5|/usr/local/biotools/c/coinfinder:1.0.5--py36hc27cf86_0
2.5.5|/usr/local/biotools/c/coinfinder:1.0.5--py36hc27cf86_1
2.5.5|/usr/local/biotools/c/coinfinder:1.0.5--py37h6b63d35_0
2.5.5|/usr/local/biotools/c/coinfinder:1.0.5--py37h6b63d35_1
2.5.5|/usr/local/biotools/c/coinfinder:1.0.5--py38h69d548c_0
2.5.5|/usr/local/biotools/c/coinfinder:1.0.5--py38h69d548c_1
2.5.5|/usr/local/biotools/c/coinfinder:1.0.6--py36hc27cf86_0
2.5.5|/usr/local/biotools/c/coinfinder:1.0.6--py37h6b63d35_0
2.5.5|/usr/local/biotools/c/coinfinder:1.0.6--py38h69d548c_0
2.5.5|/usr/local/biotools/c/coinfinder:1.0.7--py36hc27cf86_0
2.5.5|/usr/local/biotools/c/coinfinder:1.0.7--py37h6b63d35_0
2.5.5|/usr/local/biotools/c/coinfinder:1.0.7--py38h69d548c_0
2.5.5|/usr/local/biotools/d/dadaist2-full:0.7--0
2.5.5|/usr/local/biotools/f/frogs:3.1.0--1
2.5.5|/usr/local/biotools/m/mulled-v2-9a28a1e6bc757d0de672d2b8e05c2cd30003da0f:c8dc3c82333b304d76c2a6bb733aa8c06b449fab-0
2.5.5|/usr/local/biotools/p/pirate:1.0.2--0
2.5.5|/usr/local/biotools/p/pirate:1.0.2--1
2.5.5|/usr/local/biotools/p/pirate:1.0.3--0
2.5.5|/usr/local/biotools/r/r-fastbaps:1.0.1--r36_0
2.5.5|/usr/local/biotools/r/r-fastbaps:1.0.2--r36_0
2.5.5|/usr/local/biotools/r/r-fastbaps:1.0.3--r36_0
2.5.5|/usr/local/biotools/r/r-fastbaps:1.0.3--r40_1
2.5.5|/usr/local/biotools/r/r-fastbaps:1.0.4--r40_0
2.5.5|/usr/local/biotools/r/r-metacoder:0.3.3--r36h0357c0b_0
2.5.5|/usr/local/biotools/r/r-metacoder:0.3.4--r36h0357c0b_0
2.5.5|/usr/local/biotools/r/r-metacoder:0.3.4--r40h0357c0b_1
2.5.5|/usr/local/biotools/r/r-phytools:0.6_99--r36h6115d3f_0
2.5.5|/usr/local/biotools/r/r-phytools:0.6_99--r40h6115d3f_1
2.5.5|/usr/local/biotools/r/r-poppr:2.8.3--r36h516909a_0
2.5.5|/usr/local/biotools/r/r-poppr:2.8.4--r36h516909a_0
2.5.5|/usr/local/biotools/r/r-poppr:2.8.5--r36h516909a_0
2.5.5|/usr/local/biotools/r/r-poppr:2.8.5--r40h516909a_1
2.5.5|/usr/local/biotools/t/trinity:2.11.0--h5ef6573_1
2.5.5|/usr/local/biotools/t/trinity:2.12.0--h5ef6573_0
2.5.5|/usr/local/biotools/t/trycycler:0.3.1--py_0
2.5.5|/usr/local/biotools/t/trycycler:0.4.1--py_0
2.5.5|/usr/local/biotools/t/trycycler:0.4.2--py_0
2.6.2|/usr/local/biotools/bioconductor/l/bioconductor-lymphoseq:1.18.0--r40hdfd78af_1
2.6.2|/usr/local/biotools/bioconductor/m/bioconductor-meskit:1.0.1--r40hdfd78af_0
2.6.2|/usr/local/biotools/bioconductor/p/bioconductor-philr:1.16.0--r40hdfd78af_1
2.6.2|/usr/local/biotools/bioconductor/s/bioconductor-sangeranalyser:1.0.0--r40hdfd78af_1
2.6.2|/usr/local/biotools/d/dadaist2-full:0.7--hdfd78af_1
2.6.2|/usr/local/biotools/r/r-metacoder:0.3.4--r40h52a8340_2
2.6.3|/usr/local/biotools/d/dadaist2-full:1.0--hdfd78af_0
2.6.3|/usr/local/biotools/t/trinity:2.12.0--ha140323_1
2.7.0|/usr/local/biotools/bioconductor/l/bioconductor-lymphoseq:1.20.0--r41hdfd78af_0
2.7.0|/usr/local/biotools/bioconductor/m/bioconductor-meskit:1.2.0--r41hdfd78af_0
2.7.0|/usr/local/biotools/bioconductor/p/bioconductor-philr:1.18.0--r41hdfd78af_0
2.7.0|/usr/local/biotools/bioconductor/s/bioconductor-sangeranalyser:1.2.0--r41hdfd78af_0
2.7.0|/usr/local/biotools/c/coinfinder:1.1.0--py36h558eaa1_1
2.7.0|/usr/local/biotools/c/coinfinder:1.1.0--py36hb6edc42_0
2.7.0|/usr/local/biotools/c/coinfinder:1.1.0--py37ha26c1f0_0
2.7.0|/usr/local/biotools/c/coinfinder:1.1.0--py37haba7c85_1
2.7.0|/usr/local/biotools/c/coinfinder:1.1.0--py38h5d91f80_1
2.7.0|/usr/local/biotools/c/coinfinder:1.1.0--py38h8283bdf_0
2.7.0|/usr/local/biotools/c/coinfinder:1.1.0--py39h2ce926b_1
2.7.0|/usr/local/biotools/c/coinfinder:1.1.0--py39hefd1346_0
2.7.0|/usr/local/biotools/c/coinfinder:1.2.0--py36h558eaa1_0
2.7.0|/usr/local/biotools/c/coinfinder:1.2.0--py37haba7c85_0
2.7.0|/usr/local/biotools/c/coinfinder:1.2.0--py38h5d91f80_0
2.7.0|/usr/local/biotools/c/coinfinder:1.2.0--py39h2ce926b_0
2.7.0|/usr/local/biotools/c/coinfinder:1.2.1--py310h457ec61_1
2.7.0|/usr/local/biotools/c/coinfinder:1.2.1--py310hd530c1b_0
2.7.0|/usr/local/biotools/c/coinfinder:1.2.1--py36h558eaa1_0
2.7.0|/usr/local/biotools/c/coinfinder:1.2.1--py37haba7c85_0
2.7.0|/usr/local/biotools/c/coinfinder:1.2.1--py38h4338f67_1
2.7.0|/usr/local/biotools/c/coinfinder:1.2.1--py38h5d91f80_0
2.7.0|/usr/local/biotools/c/coinfinder:1.2.1--py39h2ce926b_0
2.7.0|/usr/local/biotools/c/coinfinder:1.2.1--py39h462859d_1
2.7.0|/usr/local/biotools/r/r-metacoder:0.3.4--r41h52a8340_3
2.7.0|/usr/local/biotools/r/r-metacoder:0.3.5--r41h52a8340_0
2.7.1|/usr/local/biotools/bioconductor/d/bioconductor-dialignr:2.2.0--r41h399db7b_0
2.7.1|/usr/local/biotools/bioconductor/l/bioconductor-lymphoseq:1.22.0--r41hdfd78af_0
2.7.1|/usr/local/biotools/bioconductor/m/bioconductor-meskit:1.4.0--r41hdfd78af_0
2.7.1|/usr/local/biotools/bioconductor/p/bioconductor-philr:1.20.0--r41hdfd78af_0
2.7.1|/usr/local/biotools/bioconductor/s/bioconductor-sangeranalyser:1.4.0--r41hdfd78af_0
2.7.1|/usr/local/biotools/bioconductor/t/bioconductor-tanggle:1.0.0--r41hdfd78af_0
2.7.1|/usr/local/biotools/d/dadaist2-full:1.1--hdfd78af_0
2.7.1|/usr/local/biotools/d/dadaist2-full:2.0--hdfd78af_0
2.7.1|/usr/local/biotools/t/trinity:2.12.0--ha140323_2
2.7.1|/usr/local/biotools/t/trinity:2.12.0--ha140323_3
2.7.1|/usr/local/biotools/t/trycycler:0.5.0--pyhdfd78af_0
2.7.1|/usr/local/biotools/t/trycycler:0.5.1--pyhdfd78af_0
2.8.0|/usr/local/biotools/t/trinity:2.13.2--ha140323_0
2.8.0|/usr/local/biotools/t/trycycler:0.5.3--pyhdfd78af_0
2.8.1|/usr/local/biotools/bioconductor/d/bioconductor-dialignr:2.2.0--r41h619a076_1
2.8.1|/usr/local/biotools/r/r-dowser:0.1.0--r41h3121a25_0
2.8.1|/usr/local/biotools/r/r-dowser:1.0.0--r41h3121a25_0
2.8.1|/usr/local/biotools/r/r-fastbaps:1.0.6--r41h2e03b76_0
2.8.1|/usr/local/biotools/r/r-fastbaps:1.0.6--r41h5b5514e_1
2.8.1|/usr/local/biotools/r/r-metacoder:0.3.5--r41hecf12ef_1
2.8.1|/usr/local/biotools/t/trinity:2.13.2--h00214ad_1
2.8.1|/usr/local/biotools/t/trinity:2.13.2--h15cb65e_2
2.9.0|/usr/local/biotools/bioconductor/d/bioconductor-dialignr:2.2.0--r41hc247a5b_2
2.9.0|/usr/local/biotools/bioconductor/d/bioconductor-dialignr:2.6.0--r42hc247a5b_0
2.9.0|/usr/local/biotools/bioconductor/m/bioconductor-meskit:1.8.0--r42hdfd78af_0
2.9.0|/usr/local/biotools/bioconductor/p/bioconductor-philr:1.24.0--r42hdfd78af_0
2.9.0|/usr/local/biotools/bioconductor/t/bioconductor-tanggle:1.4.0--r42hdfd78af_0
2.9.0|/usr/local/biotools/r/r-dowser:1.1.0--r41h3121a25_0
2.9.0|/usr/local/biotools/r/r-dowser:1.1.0--r42h3121a25_1
2.9.0|/usr/local/biotools/r/r-enchantr:0.0.1--r41hdfd78af_0
2.9.0|/usr/local/biotools/r/r-enchantr:0.0.3--r41hdfd78af_0
2.9.0|/usr/local/biotools/r/r-enchantr:0.0.3--r42hdfd78af_1
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
/usr/local/biotools/bioconductor/p/bioconductor-philr:1.26.0--r43hdfd78af_0
/usr/local/biotools/bioconductor/s/bioconductor-sangeranalyser:1.10.0--r43hdfd78af_0
/usr/local/biotools/bioconductor/t/bioconductor-tanggle:1.6.0--r43hdfd78af_0
/usr/local/biotools/m/mulled-v2-a4567890af2fd72603a7a44467e8278013842caa:934d292424738a426a835e7f69ec5a4eeab9a22f-0
/usr/local/biotools/r/r-dowser:1.2.0--r42h3121a25_0
/usr/local/biotools/r/r-enchantr:0.1.0--r42hdfd78af_0
/usr/local/biotools/r/r-enchantr:0.1.0--r42hdfd78af_1
/usr/local/biotools/r/r-enchantr:0.1.0--r42hdfd78af_2
/usr/local/biotools/r/r-enchantr:0.1.1--r42hdfd78af_0
/usr/local/biotools/r/r-enchantr:0.1.2--r42hdfd78af_0
/usr/local/biotools/r/r-enchantr:0.1.3--r42hdfd78af_0
/usr/local/biotools/r/r-fastbaps:1.0.8--r42h43eeafb_2
/usr/local/biotools/r/r-fastbaps:1.0.8--r43h43eeafb_3
/usr/local/biotools/r/r-metacoder:0.3.6--r42h21a89ab_2
/usr/local/biotools/r/r-metacoder:0.3.6--r42hecf12ef_0
/usr/local/biotools/r/r-metacoder:0.3.6--r42hecf12ef_1
/usr/local/biotools/r/r-metacoder:0.3.6--r43h21a89ab_3
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
Matrix|1.6-0
ProtGenerics|1.32.0
R6|2.5.1
RColorBrewer|1.1-3
RMSNumpress|1.0.1
RSQLite|2.3.1
Rcpp|1.0.10
RcppEigen|0.3.3.9.3
RcppTOML|0.2.2
Rhdf5lib|1.22.0
ape|5.7-1
base|4.3.0
bit|4.0.5
bit64|4.0.5
blob|1.2.4
cachem|1.0.8
cli|3.6.1
colorspace|2.1-0
compiler|4.3.0
cpp11|0.4.4
crayon|1.5.2
data.table|1.14.8
datasets|4.3.0
digest|0.6.33
dplyr|1.1.2
ellipsis|0.3.2
fansi|1.0.4
farver|2.1.1
fastmap|1.1.1
fastmatch|1.1-3
generics|0.1.3
ggplot2|3.4.2
glue|1.6.2
grDevices|4.3.0
graphics|4.3.0
grid|4.3.0
gtable|0.3.3
here|1.0.1
igraph|1.4.3
isoband|0.2.7
jsonlite|1.8.7
labeling|0.4.2
lattice|0.21-8
lifecycle|1.0.3
magrittr|2.0.3
memoise|2.0.1
methods|4.3.0
mgcv|1.8-42
munsell|0.5.0
mzR|2.34.1
ncdf4|1.21
nlme|3.1-162
parallel|4.3.0
phangorn|2.11.1
pillar|1.9.0
pkgconfig|2.0.3
plogr|0.2.0
png|0.1-8
pracma|2.4.2
purrr|1.0.1
quadprog|1.5-8
rappdirs|0.3.3
reticulate|1.30
rlang|1.1.1
rprojroot|2.0.3
scales|1.2.1
signal|0.7-7
splines|4.3.0
stats|4.3.0
stats4|4.3.0
stringi|1.7.12
stringr|1.5.0
tcltk|4.3.0
tibble|3.2.1
tidyr|1.3.0
tidyselect|1.2.0
tools|4.3.0
utf8|1.2.3
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
Matrix|1.6-0
ProtGenerics|1.32.0
R6|2.5.1
RColorBrewer|1.1-3
RMSNumpress|1.0.1
RSQLite|2.3.1
Rcpp|1.0.10
RcppEigen|0.3.3.9.3
RcppTOML|0.2.2
Rhdf5lib|1.22.0
ape|5.7-1
base|4.3.0
bit|4.0.5
bit64|4.0.5
blob|1.2.4
cachem|1.0.8
cli|3.6.1
colorspace|2.1-0
compiler|4.3.0
cpp11|0.4.4
crayon|1.5.2
data.table|1.14.8
datasets|4.3.0
digest|0.6.33
dplyr|1.1.2
ellipsis|0.3.2
fansi|1.0.4
farver|2.1.1
fastmap|1.1.1
fastmatch|1.1-3
generics|0.1.3
ggplot2|3.4.2
glue|1.6.2
grDevices|4.3.0
graphics|4.3.0
grid|4.3.0
gtable|0.3.3
here|1.0.1
igraph|1.4.3
isoband|0.2.7
jsonlite|1.8.7
labeling|0.4.2
lattice|0.21-8
lifecycle|1.0.3
magrittr|2.0.3
memoise|2.0.1
methods|4.3.0
mgcv|1.8-42
munsell|0.5.0
mzR|2.34.1
ncdf4|1.21
nlme|3.1-162
parallel|4.3.0
phangorn|2.11.1
pillar|1.9.0
pkgconfig|2.0.3
plogr|0.2.0
png|0.1-8
pracma|2.4.2
purrr|1.0.1
quadprog|1.5-8
rappdirs|0.3.3
reticulate|1.30
rlang|1.1.1
rprojroot|2.0.3
scales|1.2.1
signal|0.7-7
splines|4.3.0
stats|4.3.0
stats4|4.3.0
stringi|1.7.12
stringr|1.5.0
tcltk|4.3.0
tibble|3.2.1
tidyr|1.3.0
tidyselect|1.2.0
tools|4.3.0
utf8|1.2.3
utils|4.3.0
vctrs|0.6.3
viridisLite|0.4.2
withr|2.5.0
zoo|1.8-12

```
