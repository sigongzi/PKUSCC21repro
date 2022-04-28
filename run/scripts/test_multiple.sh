dir=`pwd`
compiledir="${dir}/../../compile"
LD_LIBRARY_PATH="${compiledir}/boost-1.70.0/lib:${compiledir}/mvapich2/lib:${LD_LIBRARY_PATH}"
PATH="${compiledir}/mvapich2/bin:${compiledir}/ramBLe:${compiledir}/ramBLe/common/scripts:${PATH}"
datadir="${dir}/data"
scratchdir="${dir}/../output/scratch"
outputdir="${dir}/../output/strong"
echo "${compiledir}"
export MV2_IBA_HCA=mlx5_2
export MV2_USE_RoCE=1
export LD_LIBRARY_PATH
export PATH
export MV2_ENABLE_AFFINITY=1
ulimit -l unlimited

cpu_number=$1
core_number=$2
dataset=$3
algorithm=$4
st=$5
hostfile=$6
p_number=$((${cpu_number}*${core_number}))
dataset_file="${datadir}/${dataset}_discretized.tsv"
prefix="${dataset}_${algorithm}_p${p_number}_strong"
output_file="${outputdir}/${prefix}.csv"
if [ -f ${dataset_file} ];then
    s=$st
    i=1

    while(( $i<$core_number))
    do
        s="${s}:`expr $st + $i`"
        i=`expr $i + 1`
    done
    echo $s
    ramble_experiments.py --basedir ${compiledir}/ramBLe --scratch ${scratchdir}/${prefix}.dot --mpi-arguments "-env MV2_CPU_MAPPING ${s}" --hostfile ./${hostfile} -p ${p_number} -r 1 -a ${algorithm} -d ${dataset_file} -s $'\t' -c -v -i  --results ${output_file} > ${outputdir}/${prefix}.save 
else
    echo "${dataset_file} not found!"
fi
