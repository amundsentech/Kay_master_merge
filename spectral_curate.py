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
    spec_file=config.spec_file
    spec_file='https://drive.google.com/uc?id=' + spec_file.split('/')[-2]
    output_file=config.output_path+config.spec_fname
    spectral=pd.read_csv(spec_file,low_memory=False)
    try:
        opts, args = getopt.getopt(argv,"ci:o:",["input_file=","output_file="])
        for opt, arg in opts:
            if opt == '-c':
                print ('spectral_curate.py -i <input_file> -a <output_file>')
                sys.exit()
            elif opt in ("-i", "--input_file"):
                spec_file = arg
                print ('Input file is ',)
                spectral=pd.read_csv(spec_file)
                output_file=config.output_path+spec_file
            elif opt in ("-o", "--output_file"):
                output_file = arg
                print ('Output file is ', output_file)
    except getopt.GetoptError:
        print ('file error read grom google drive')
    print ('Input file is ', config.spec_file)
    print ('Output file is ', output_file)
    #pull sample ids
    spectral=ct.pull_sample_ids(spectral)
    #### clean and fill spectral data
    spectral=ct.carrot_cleanup(spectral)
    spectral=ct.column_cleanup(spectral,mapping=config.depth_mapping)
    spectral=ct.column_cleanup(spectral,mapping=config.file_mapping)
    spectral=ct.column_cleanup(spectral,mapping=config.vnir_mapping)

    spec_fname= config.spec_fname
        ## out put final csvs
    path=output_file

    
    print(f'output {output_file}')
    spectral.to_csv(output_file)
    return spectral

if __name__ == "__main__":
    main(sys.argv[1:])