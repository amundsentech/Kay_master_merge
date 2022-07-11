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
import filter_config as config
import datetime

def main(argv):
    lith_file=config.lith_file
    lith=pd.read_csv(lith_file,low_memory=False)
    output_file=lith_file
    try:
        opts, args = getopt.getopt(argv,"ri:o:",["input_file=","output_file="])
        for opt, arg in opts:
            if opt == '-r':
                print ('lithology_curate.py -i <input_file> -a <output_file>')
                print('using defaults if no file specified')
                
            elif opt in ("-i", "--input_file"):
                lith_file = arg
                print ('Input file is ',)
                lith=pd.read_csv(lith_file)
                output_file=lith_file
            elif opt in ("-o", "--output_file"):
                output_file = arg
                print ('Output file is ', output_file)
    except getopt.GetoptError:
        print ('file error read grom google drive')
    print ('Input file is ', config.lith_file)
    print ('Output file is ', output_file)
    #pull sample ids
    lith=ct.pull_sample_ids(lith)
    #### clean and fill lith data
    lith=ct.lith_cleanup(lith)

    
    print(f'output {output_file}')
    lith.to_csv(config.lith_file)
    return lith

if __name__ == "__main__":
    main(sys.argv[1:])