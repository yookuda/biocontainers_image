#!/bin/bash
# 引数でイメージのリストを指定し、リスト中に存在しないbiotoolsイメージからイメージ内の/usr以下の共有ライブラリ・/usr/local/binのコマンドを取得する。

function output_and_exec_script () {
    echo '#!/bin/bash' > $1
    echo '#$ -S /bin/bash' >> $1
    echo '#$ -V' >> $1
    echo '#$ -cwd' >> $1
    echo "DIR=\"${2}\"" >> $1
    echo 'echo "DIR:${DIR}"' >> $1
    echo "BASE_LIST=\"${3}\"" >> $1
    echo 'for IMAGE in $(ls ${DIR}); do' >> $1
    echo 'if grep -q ${IMAGE} ${BASE_LIST} ; then' >> $1
    echo ':' >> $1
    echo 'else' >> $1
    echo 'echo "IMAGE:${IMAGE}"' >> $1
    echo 'singularity exec ${DIR}/${IMAGE} find /usr -name "*.so" -or -name "*.so.*" | xargs -I {} echo "LIBRARY:"{}' >> $1
    echo 'singularity exec ${DIR}/${IMAGE} ls /usr/local/bin |  xargs -I {} echo "COMMAND:"{}' >> $1
    echo 'fi' >> $1
    echo 'done' >> $1
    qsub $1
}

if [ $# != 1 ]; then
    echo "usage:bash $0 <image list file>"
    exit 1
fi

BASE_LIST=$1

if [ ! -e $BASE_LIST ]; then
    echo "${BASE_LIST} is not exists."
    exit
fi

DATE=`date '+%Y%m%d'`
mkdir $DATE
cd $DATE

for D in $(ls /usr/local/biotools); do
    if [ ${D} = 'bioconductor' ]; then
        for D2 in $(ls /usr/local/biotools/bioconductor); do
            SCRIPT="biotools_${D}_${D2}.sh"
            DIR="/usr/local/biotools/${D}/${D2}"
            output_and_exec_script ${SCRIPT} ${DIR} ${BASE_LIST}
        done
    else
        SCRIPT="biotools_${D}.sh"
        DIR="/usr/local/biotools/${D}"
        output_and_exec_script ${SCRIPT} ${DIR} ${BASE_LIST}
    fi
done

