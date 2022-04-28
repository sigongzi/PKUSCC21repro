### Options and environment variables

**some pre-work**

stop hyper threading

experiments need MV2_ENABLE_AFFINITY on, so use sudo user to stop hyper threading

```shell
echo off| sudo tee /sys/devices/system/cpu/smt/control
```



**append scl devtoolset-9 in ~/.bash_profile**

```shell
scl enable devtoolset-9 bash
```



### Environment at run time

we add all running environment variable in .sh files

we list vital variables below

```shel
MV2_IBA_HCA=mlx5_2
MV2_USE_RoCE=1
MV2_ENABLE_AFFINITY=1
```

pre-append  to some environment variables

```
LD_LIBRARY_PATH="${compiledir}/boost-1.70.0/lib:${compiledir}/mvapich2/lib:${LD_LIBRARY_PATH}"
PATH="${compiledir}/mvapich2/bin:${compiledir}/ramBLe:${compiledir}/ramBLe/common/scripts:${PATH}"
```



and we add 

```shell
ulimit -l unlimited
```

to avoid runtime error



### How to run each experiment

during the competition, scheduling task is all do by manual work

you can use our scripts to test do experiment with fixed processor number, dataset, algorithm





#### do experiments within 32 cores 

these experiments can do on single machine

to do strong scale experiments, use

```shell
./test_single.sh {processor_number} {dataset} {algorithm} {start_cpu_id}
```

we use **start_cpu_id** to assign a series of continuous cpu cores to run and bind to them



for example, running C3 dataset using algorithm GS with 16 cores



input 

```shell
./test_single.sh 16 C3 gs 0
```



for weak scale, you can use

```shell
./test_weak_single.sh {processor_number} {dataset} {algorithm} {start_cpu_id} {variables}
```



for example, running 10000 variables in C2 dataset using algorithm GS with 16 cores 

input 

```shell
./test_weak_single.sh 16 C2 gs 0 10000
```



#### do experiments above 64 cores (included) 

these experiments need hostfile

to do strong scale experiments, use

```shell
./test_multiple.sh {machine_number} {processor_per_machine} {dataset} {algorithm} {start_cpu_id} {hostfile}
```

for example, running C3 dataset using algorithm GS with 64 cores

input 

```shell
./test_multiple.sh 2 32 C3 gs 0 ./hostfile2
```

for weak scale, use

```shell
./test_weak_multiple.sh {machine_number} {processor_per_machine} {dataset} {algorithm} {start_cpu_id} {variables} {hostfile}
```

for example, running 20000 variables in C2 dataset using algorithm GS with 64 cores 

input

```shell
./test_weak_multiple.sh 2 32 C2 gs 0 20000 ./hostfile2
```



### What is different

if you just use **.csv** files to record results. Nothing is different from **ramble_experiments.py**

but we distinguish all the resulted graphs instead of using temporary names 



###  How timings were measured

in compille **install_ramble.sh**， we compile ramble with choice **TIMER=1**, so we get time message in terminal.

we save the result **.save** files under **run/output/{strong|weak}**  

and **ramble_experiments.py** and **ramble_weak_experiments.py** help us translate raw message to **.csv** files