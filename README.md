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
/usr/local/biotools/ 以下に新規追加された singularity image から、インストールされているコマンド・共有ライブラリを取得する。
```
$ bash get_command_and_shared_library_list_qsub.sh /home/y-okuda/biocontainers/biotools_image_list/biotools_image_list_merged_<前回の実行日の日付>.txt
```
実行結果に対し、json ファイルの生成・コマンド・共有ライブラリリスト取得済みイメージリストの生成を実行する。

