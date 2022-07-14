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
sys.path.append("../")
import file_config as fconfig
import spectral_config as config
import datetime

def main(argv):
    spec_file=fconfig.spec_file

    spectral=pd.read_csv(spec_file,low_memory=False)
    output_file=spec_file
    try:
        opts, args = getopt.getopt(argv,"ri:o:",["input_file=","output_file="])
        for opt, arg in opts:
            if opt == '-r':
                print ('spectral_curate.py -i <input_file> -a <output_file>')
                print('using defaults if no file specified')
                
            elif opt in ("-i", "--input_file"):
                spec_file = arg
                print ('Input file is ',)
                spectral=pd.read_csv(spec_file)
                output_file=spec_file
            elif opt in ("-o", "--output_file"):
                output_file = arg
                print ('Output file is ', output_file)
    except getopt.GetoptError:
        print ('file error read grom google drive')
    print ('Input file is ', fconfig.spec_file)
    print ('Output file is ', output_file)
    #pull sample ids
    spectral=ct.pull_sample_ids(spectral)
    #### clean and fill spectral data
    spectral=ct.carrot_cleanup(spectral)
    for map in config.mappings:
        spectral=ct.column_cleanup(spectral,mapping=map)

    spec_fname= fconfig.spec_fname
        ## out put final csvs
    path=output_file

    
    print(f'output {output_file}')
    spectral.to_csv(fconfig.spec_file)
    return spectral

if __name__ == "__main__":
    main(sys.argv[1:])