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
import sample_config as config
import datetime

def main(argv):
    sample_file=fconfig.sample_file
    sample=pd.read_csv(sample_file,low_memory=False)
    output_file=sample_file
    try:
        opts, args = getopt.getopt(argv,"ri:o:",["input_file=","output_file="])
        for opt, arg in opts:
            if opt == '-r':
                print ('sample_curate.py -i <input_file> -a <output_file>')
                print('using defaults if no file specified')
                
            elif opt in ("-i", "--input_file"):
                sample_file = arg
                print ('Input file is ',)
                sample=pd.read_csv(sample_file)
                output_file=sample_file
            elif opt in ("-o", "--output_file"):
                output_file = arg
                print ('Output file is ', output_file)
    except getopt.GetoptError:
        print ('file error read grom google drive')
    print ('Input file is ', fconfig.sample_file)
    print ('Output file is ', output_file)
    #### clean and fill sample data
    sample=ct.depth_cleanup(sample)

    for map in config.mappings:
        sample=ct.column_cleanup(sample,mapping=map)
    print(f'output {output_file}')
    sample.to_csv(fconfig.sample_file,index=False)
    return sample

if __name__ == "__main__":
    main(sys.argv[1:])