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
import hypPackage_config as config
import datetime

def main(argv):
    try:
        opts, args = getopt.getopt(argv,"ri:o:",["input_file=","output_file="])
        for opt, arg in opts:
            if opt == '-r':
                print ('hypPackage_curate.py -i <input_file> -a <output_file>')
                print('using defaults if no file specified')
                
            elif opt in ("-i", "--input_file"):
                hyp_file = arg
                print (f'Input file is {arg} ',)
                hyp=pd.read_csv(hyp_file)
                output_file=hyp_file
            elif opt in ("-o", "--output_file"):
                output_file = arg
                print ('Output file is ', output_file)
    except getopt.GetoptError as e:
        print (e)
        print ('FILE READ ERROR read from CONFIG')
        hyp_file=fconfig.hyp_file
        hyp=pd.read_csv(hyp_file,low_memory=False)
        output_file=hyp_file
    print ('Input file is ', hyp_file)
    print ('Output file is ', output_file)
    #### clean and fill hyp data
    hyp=ct.depth_cleanup(hyp)

    for map in config.mappings:
        hyp=ct.column_cleanup(hyp,mapping=map)
    
    print(f'output {output_file}')
    hyp.to_csv(output_file,index=False)
    return hyp

if __name__ == "__main__":
    main(sys.argv[1:])