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
import datetime

def main(argv):
    alter_file=fconfig.alter_file
    alter=pd.read_csv(alter_file,low_memory=False)
    output_file=alter_file
    try:
        opts, args = getopt.getopt(argv,"ri:o:",["input_file=","output_file="])
        for opt, arg in opts:
            if opt == '-r':
                print ('alteration_curate.py -i <input_file> -a <output_file>')
                print('using defaults if no file specified')
                
            elif opt in ("-i", "--input_file"):
                alter_file = arg
                print ('Input file is ',)
                alter=pd.read_csv(alter_file)
                output_file=alter_file
            elif opt in ("-o", "--output_file"):
                output_file = arg
                print ('Output file is ', output_file)
    except getopt.GetoptError:
        print ('file error read grom google drive')
    print ('Input file is ', fconfig.alter_file)
    print ('Output file is ', output_file)
    #### clean and fill alter data
    alter=ct.depth_cleanup(alter)

    
    print(f'output {output_file}')
    alter.to_csv(fconfig.alter_file,index=False)
    return alter

if __name__ == "__main__":
    main(sys.argv[1:])