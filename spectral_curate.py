import getopt,sys


import pandas as pd
import cleaningtools as ct
import filter_config as config
import datetime

def main(argv):
    spec_file=config.spec_file

    try:
        opts, args = getopt.getopt(argv,"ci:o:",["input_file=","output_file="])
        for opt, arg in opts:
            if opt == '-c':
                print ('spectral_curate.py -i <input_file> -a <output_file>')
                sys.exit()
            elif opt in ("-i", "--input_file"):
                spec_file = arg
                print ('Input file is "', spec_file)
            elif opt in ("-o", "--output_file"):
                output_file = arg
                print ('Output file is "', output_file)
    except getopt.GetoptError:
        print ('Input file is "', config.spec_file)
        print ('Output file is "', config.output_path, config.spec_fname)

    spectral=pd.read_csv(spec_file,low_memory=False)
    #pull sample ids
    spectral=ct.pull_sample_ids(spectral)
    #### clean and fill spectral data
    spectral=ct.carrot_cleanup(spectral)
    spectral=ct.column_cleanup(spectral,mapping=config.depth_mapping)
    spectral=ct.column_cleanup(spectral,mapping=config.file_mapping)
    spectral=ct.column_cleanup(spectral,mapping=config.vnir_mapping)

    spec_fname= config.spec_fname
        ## out put final csvs
    path=config.output_path

    
    print(f'output {spec_fname}')
    spectral.to_csv(path+spec_fname)
    return spectral

if __name__ == "__main__":
    main(sys.argv[1:])