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


def main(argv):
    assay_file=config.assay_file
    spec_file=config.spec_file

    try:
        opts, args = getopt.getopt(argv,"cs:a:o:",["spectral_file=","assay_file=",'output_path:'])
        for opt, arg in opts:
            if opt == '-s':
                print ('kay_curate_merge.py -s < spectral_file> -a <assay_file> -o <output_path>')
                sys.exit()
            elif opt in ("-s", "--spectral_file"):
                assay_file = arg
                print ('assay file is "', assay_file)

            elif opt in ("-a", "--assay_file"):
                spec_file = arg
                print ('Input file is "', assay_file)
                       
            elif opt in ("-o", "--output_path"):
                output_file = arg

                print ('Output file is "', output_file)
    except getopt.GetoptError:
        print ('Spectral paths "', config.assay_file)
        print ('Assay paths "', config.assay_file)
        print ('Output pth "', config.output_path)
    
    
    assays=pd.read_csv(assay_file)
    spectral=pd.read_csv(spec_file,low_memory=False)
    msg = "Begin Cleaning"
    print(msg)


    spectral=ct.pull_sample_ids(spectral)

    assays=ct.pull_sample_ids(assays)

    #### clean and fill spectral datav
    spectral=ct.carrot_cleanup(spectral)
    spectral=ct.column_cleanup(spectral,mapping=config.depth_mapping)
    spectral=ct.column_cleanup(spectral,mapping=config.file_mapping)
    spectral=ct.column_cleanup(spectral,mapping=config.vnir_mapping)
    
    #### clean and fill Assay data
    assays=ct.carrot_cleanup(assays)
    assays=ct.column_cleanup(assays,mapping=config.depth_mapping)
    assays=ct.column_cleanup(assays,mapping=config.file_mapping)


    ## date var for final output file names
    #outputnames
    spectral_fname= config.spec_fname
    assay_fname= config.assay_fname
    final_fname= config.final_fname

    final=pd.merge(assays,spectral,on='sample_id',how='inner',sort=True)
    
    ## out put final csvs
    path=config.output_path
    print(f'output {spectral_fname}')
    spectral.to_csv(path+spectral_fname)
    
    print(f'output {assay_fname}')
    assays.to_csv(path+assay_fname)
    
    print(f'output {final_fname}')
    final.to_csv(path+final_fname)

if __name__ == "__main__":
    main(sys.argv[1:])