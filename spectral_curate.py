import getopt,sys
import os
import subprocess
import cleaningtools as ct 
import pandas as pd
import file_config as fconfig
import spectral_config as config
import datetime

def main(argv):
    spec_file=[]
    try:
        opts, args = getopt.getopt(argv,"ri:o:",["input_file=","output_file="])
        for opt, arg in opts:
            if opt == '-r':
                print ('spectral_curate.py -i <input_file> -a <output_file>')
                print('using defaults if no file specified')
                
            elif opt in ("-i", "--input_file"):
                spec_file = arg
                print (f'Input file is {arg} ',)
                spectral=pd.read_csv(spec_file)
                output_file=spec_file
            elif opt in ("-o", "--output_file"):
                output_file = arg
                print ('Output file is ', output_file)
    except getopt.GetoptError as e:
        print (e)
        print ('FILE READ ERROR read from CONFIG')
    if len(spec_file)==0:
        spec_file=fconfig.spec_file
        spectral=pd.read_csv(spec_file,low_memory=False)
        output_file=spec_file    
    print ('Input file is ', spec_file)
    print ('Output file is ', output_file)
    msg = "Begin Cleaning"
    base_path=ct.get_base_path(spec_file,start_point='_AZ_Kay')

    sample_path=base_path+'/_Drilling/_Logs'


    print(msg)
    #pull sample ids
    spectral=ct.pull_sample_ids(spectral,config.sample_id_formats)
    #### clean and fill spectral data
    spectral=ct.carrot_cleanup(spectral)
    for map in config.mappings:
        spectral=ct.column_cleanup(spectral,mapping=map)

    data_list=[]
    i=0
    print('#### start pulling hyper spectral sample ids######')
    for folder in os.listdir(sample_path):
        folder=sample_path+'/'+folder
        if os.path.isdir(folder):
            for file in os.listdir(folder):
                    if 'hyp-pkg samples' in file.lower():
                        print(i,file)
                        name=file
                        file=folder+'/'+file
                        try:
                            data=pd.read_excel(file, header=None,na_filter=True)
                            data=data.dropna(how='all')
                            headers = data.iloc[0].str.lower()
                            data  = pd.DataFrame(data.values[1:], columns=headers).reset_index(drop=True)
                            if data.T. index.duplicated().any():
                                print(i,'duplcate columns')
                                continue
                            data['FileName']=name
                            data_list.append(data)
                            i+=1
                        except Exception as e:
                            print(e)
        else: 
            print(f"{folder} is not a folder")

    spec_samples=pd.concat(data_list,axis=0,ignore_index=True)
    spec_samples=ct.generate_from_to(data,sort_by=['hole_id','depth_ft'])

    spec_samples=ct.remove_depth_errors(spec_samples)
    spec_final=spectral.merge(spec_samples,how='outer',left_on='sample_id',right_on='sample_id')
    print('#### Final Cleanup #####')
    starting_cols=['sample_id','from_ft','to_ft','from_m','to_m','hole_id','geo']
    ending_cols=[col for col in spec_final.columns if col not in starting_cols]
    spec_final=pd.concat([spec_final[starting_cols],spec_final[ending_cols]],axis=1)
    spec_fname= fconfig.spec_fname

    spec_final=spec_final.sort_values(['hole_id','from_ft','sample_id'])
    print(f'output {output_file}')
    spec_final.to_csv(output_file,index=False)
    return spectral

if __name__ == "__main__":
    main(sys.argv[1:])