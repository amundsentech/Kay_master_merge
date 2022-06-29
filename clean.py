import getopt,sys

import argparse
import pandas as pd
import cleaningtools as ct
import filter_config as config
import datetime

def main(argv):
    assay_file='Google Drive/Shared drives/AMC Projects/_AZ_Kay/_Master Databases/drill assays master.csv'
    spec_file='Google Drive/Shared drives/AMC Projects/_AZ_Kay/_Master Databases/spectral master.csv'
    try:
        opts, args = getopt.getopt(argv,"cs:a:",["spec_file=","assay_file="])
        for opt, arg in opts:
            if opt == '-c':
                print ('test.py -s <spec_file> -a <assay_file>')
                sys.exit()
            elif opt in ("-s", "--spec_file"):
                spec_file = arg
            elif opt in ("-a", "--assay_file"):
                assay_file = arg

        print ('Input file is "', spec_file)
        print ('Output file is "', spec_file)
    except getopt.GetoptError:
        print ('test.py -i <assayfile> -o <spectralfile>')
        print('using default paths')
    
    assays=pd.read_csv(assay_file)
    spectral=pd.read_csv(spec_file,low_memory=False)
    msg = "Begin Cleaning"
    print('msg')


    spectral=ct.pull_sample_ids(spectral)

    assays=ct.pull_sample_ids(assays)

    #### clean and fill spectral data
    spectral=ct.column_cleanup(spectral,mapping=config.depth_mapping)
    spectral=ct.column_cleanup(spectral,mapping=config.file_mapping)
    spectral=ct.column_cleanup(spectral,mapping=config.vnir_mapping)
    spectral=spectral.fillna('')
    spectral=spectral.replace('nan','')
    #### clean and fill Assay data
    assays=ct.carrot_cleanup(assays)
    assays=ct.column_cleanup(assays,mapping=config.depth_mapping)
    assays=ct.column_cleanup(assays,mapping=config.file_mapping)
    assays=assays.fillna('')
    assays=assays.replace('nan','')

    ## date var for final output file names
    
    date=datetime.datetime.today().strftime('%Y_%m_%d')
    #outputnames
    spectral_fname=f'Master_Spectral_Clean_{date}.csv'
    assay_fname=f'Master_assay_Clean_{date}.csv'
    final_fname=f'Master_Spectral_Assay_Merge_Clean_{date}.csv'

    final=pd.merge(assays,spectral,on='sample_id',how='inner',sort=True)
    
    ## out put final csvs
    path=config.output_path
    print(f'output {spectral_fname}')
    spectral.to_csv(path+spectral_fname)
    
    print(f'output {spectral_fname}')
    assays.to_csv(path+assay_fname)
    
    print(f'output {spectral_fname}')
    final.to_csv(path+final_fname)

if __name__ == "__main__":
    main(sys.argv[1:])