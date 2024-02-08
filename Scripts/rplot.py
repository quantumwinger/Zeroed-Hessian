 import numpy as np
 import os
 comment='''
 $comment
 Jobs for R-plot
 $end
 '''
 mol_label='''
 $molecule
 0  1
 '''
 rems='''
 $rem
    BASIS  =  6-31G(d,p)
    DFT_D  =  D3_BJ
    JOB_TYPE  =  OPT
    METHOD  =  B3LYP
    GEOM_OPT_MAX_CYCLES = 1500
    SYM_IGNORE = true
    NO_REORIENT = true
    MEM_TOTAL = 80000
    !MEM_STATIC = 4000
    SCF_MAX_CYCLES  =  500
 $end
 $opt
 CONSTRAINT
 '''
 curr_der = os.getcwd()
 def inputer(inp):
         crds=np.loadtxt(inp,skiprows=2,dtype=str)
         for i in range(-180,190,10):
             os.mkdir("rplot"+str(i))
             os.chdir("rplot"+str(i))
             for j in range(-180,190,10):
                 print(str(i),str(j))
                 f = open(inp[:-4]+"_f"+str(i)+"_s"+str(j)+".inp", "w")
                 f.write(comment)
                 f.write(mol_label)
                 for line in crds:
                     f.write(" ".join(line)+"\n")
                 f.write("$end \n")
                 f.write(rems)
                 f.write("tors 9 10 11 30 "+str(i)+"\n")
                 f.write("tors 11 30 31 32 "+str(j)+"\n")
                 f.write("ENDCONSTRAINT \n")
                 f.write("FIXED\n")
                 f.write("41 XYZ\n")
                 f.write("44 XYZ\n")
                 f.write("ENDFIXED\n")
                 f.write("$end \n")
             os.chdir(curr_der)
 inputer("pep.xyz")
5:00
#!/bin/bash
 for i in $(seq -180 10 180)
 do
    echo "Directory rplot${i}"
    cd rplot${i}
    for j in $(seq -180 10 180)
    do
         echo "pep_f${i}_s${j}.inp"
 cat << EOF > pep_f${i}_s${j}.job
 #!/bin/csh
 #SBATCH --job-name=pep_f${i}_s${j}
 #SBATCH --time=01:59:00
 #SBATCH --nodes=1 --ntasks-per-node=40
 #SBATCH --account=PAA0003
 #
 # Choose name for temporary scratch directory
 # and input/output files
 #
 module load intel/17.0.7
 module rm cxx17
 module load boost/1.67.0
 #module unload boost
 module load cmake/3.11.4
 setenv SCRDIR pep_f${i}_s${j}
 setenv FileName pep_f${i}_s${j}
 setenv QC /fs/scratch/PAS0291/osu9172/trunk-10-june
 source \$QC/bin/qchem.setup
 setenv QCAUX /users/PAS0291/osu9172/qcaux
 setenv QCSCRATCH /fs/scratch/PAS0291/osu9172/harm_conf/scr
 echo 'Using Q-Chem in ' \$QC
 echo 'scratch dir is ' \$QCSCRATCH
 cd \$SLURM_SUBMIT_DIR
 qchem -nt 40 -save \${FileName}.inp \${FileName}.out
 EOF
 #        sbatch pep_f${i}_s${j}.job
    done
 cd ..
 done
