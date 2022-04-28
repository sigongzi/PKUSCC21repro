### Compiler, Software Dependencies 

- **gcc 9.3.0** (use Redhat devtoolset 9)
- **Boost 1.70.0** (compile from source)
- **MVAPICH2 2.3.3** (compile from source)
- **scons 4.2.0** (install by pip)
- **pandas 1.1.5 **(install by pip)
- **numpy 1.19.5** (install by pip)

- **matplotlib 3.3.4** (install by pip)

### The thing to do with sudo

we use red hat toolset-9 to get gcc compiler 9 version. so before the following steps. You should ensure all the nodes have installed the devtoolset-9. Input the command with a user that can use sudo on all the nodes.

```shell
sudo yum install devtoolset-9 -y
```

### The thing to do with specific user

#### use pip in user mode to install python modules

```shell
pip3 install scons --user
pip3 install pandas --user
pip3 install numpy --user
pip3 install matplotlib --user
```

we use **numpy** and **pandas** to run the **ramble_experiments.py** and **ramble_weak_experiments.py**

and **matplotlib** to run figure script

####  use install_ramble.sh to compile source

At the first you should add this command to the end of ~/.bash_profile and source it



```shell
scl enable devtoolset-9 bash
```
This help keep same dynamic libraries when running multimachine tasks.

Then use the script install_ramble.sh

```shell
./install_ramble.sh
```

### Environment information gather script

we git **Author-Kit** and use the script in **compile/Author-Kit/collect_environment.sh**

the output can be found in **environment.log**



### Some .py scripts for running experiments
we do some modification in author's scripts

to avoid covering because of reinstallation, we save the these py scripts in compile