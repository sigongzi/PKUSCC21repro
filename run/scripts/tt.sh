dir=`pwd`
compiledir="${dir}/../../compile"
LD_LIBRARY_PATH="${compiledir}/boost-1.70.0/lib:${compiledir}/mvapich2/lib:${LD_LIBRARY_PATH}"
PATH="${compiledir}/mvapich2/bin:${compiledir}/ramBLe:${compiledir}/ramBLe/common/scripts:${PATH}"
datadir="${dir}/data"
scratchdir="${dir}/../output/scratch"
outputdir="${dir}/../output"
echo "${compiledir}"
export MV2_IBA_HCA=mlx5_2
export MV2_USE_RoCE=1
export LD_LIBRARY_PATH
export PATH
export MV2_ENABLE_AFFINITY=1
ulimit -l unlimited

${compiledir}/Author-Kit/collect_environment.sh > ../../doc/scc21_team08_ExperimentalEnvironment.txt
