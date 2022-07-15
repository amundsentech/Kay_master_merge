import getopt,sys
import subprocess
try:
    print('check for pandas')
    import pandas as pd
    
except:
    try:
        print('install pandas')
        subprocess.check_call([sys.executable,'-m','pip','install','pandas'])
    except:
        print('upgrade pip then try again')
        subprocess.check_call([sys.executable,'-m','pip','install','--upgrade','pip'])
        subprocess.check_call([sys.executable,'-m','pip','install','pandas'])
        import pandas as pd

import cleaningtools as ct 
import file_config as fconfig
import structure_config as config
import datetime

def main(argv):
    structure_file=fconfig.structure_file
    structure=pd.read_csv(structure_file,low_memory=False)
    output_file=structure_file
    try:
        opts, args = getopt.getopt(argv,"ri:o:",["input_file=","output_file="])
        for opt, arg in opts:
            if opt == '-r':
                print ('structure_curate.py -i <input_file> -a <output_file>')
                print('using defaults if no file specified')
                
            elif opt in ("-i", "--input_file"):
                structure_file = arg
                print (f'Input file is {arg} ',)
                structure=pd.read_csv(structure_file)
                output_file=structure_file
            elif opt in ("-o", "--output_file"):
                output_file = arg
                print ('Output file is ', output_file)
    except getopt.GetoptError:
        print ('file error read grom google drive')
    print ('Input file is ', fconfig.structure_file)
    print ('Output file is ', output_file)
    #### clean and fill structure data
    structure=ct.depth_cleanup(structure)
    for map in config.mappings:
        structure=ct.column_cleanup(structure,mapping=map)
    
    print(f'output {output_file}')
    structure.to_csv(output_file,index=False)

    return structure

if __name__ == "__main__":
    main(sys.argv[1:])