dir=`pwd`
compiledir="${dir}/../../compile"
LD_LIBRARY_PATH="${compiledir}/boost-1.70.0/lib:${compiledir}/mvapich2/lib:${LD_LIBRARY_PATH}"
PATH="${compiledir}/mvapich2/bin:${compiledir}/ramBLe:${compiledir}/ramBLe/common/scripts:${PATH}"
datadir="${dir}/data"
scratchdir="${dir}/../output/scratch"
outputdir="${dir}/../output/strong"
ramBLedir="${compiledir}/ramBLe"
echo "${compiledir}"
export MV2_IBA_HCA=mlx5_2
export MV2_USE_RoCE=1
export LD_LIBRARY_PATH
export PATH
export MV2_ENABLE_AFFINITY=1
ulimit -l unlimited

#ramble -f ${ramBLedir}/test/coronary.csv -n 6 -m 1841 -d -o ${ramBLedir}/test/coronary.dot

mpirun -np 8 ramble -f ${ramBLedir}/test/coronary.csv -n 6 -m 1841 -d -o ${ramBLedir}/test/coronary.dot
