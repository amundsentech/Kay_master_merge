import getopt,sys

import argparse
import pandas as pd
import kaytools.cleaningtools as ct
import kaytools.filter_config as config
import datetime


msg = "Begin Cleaning"
# create a parser object
parser = argparse.ArgumentParser(description = msg)
parser.add_argument("spectral", nargs = '*', metavar = "spectral_path", type = str,
                     help = "add the path to the spectral_master data csv")
parser.add_argument("assays", nargs = '*', metavar = "spectral_path", type = str,
                     help = "add the path to the assay_master data csv")
args = parser.parse_args()

id_formats= config.sample_id_formats

assays=pd.read_csv('../_Master Databases/drill assays master.csv')
spectral=pd.read_csv('../_Master Databases/spectral master.csv',low_memory=False)

assays=pd.read_csv(args.spectral)
spectral=pd.read_csv(args.assays,low_memory=False)

date=datetime.date().strftime('%Y_%m_%d')

spectral=ct.pull_sample_ids(spectral)

assays=ct.pull_sample_ids(assays)


spectral=ct.column_cleanup(spectral,mapping=config.depth_mapping)
spectral=ct.column_cleanup(spectral,mapping=config.file_mapping)
spectral=ct.column_cleanup(spectral,mapping=config.vnir_mapping)
spectral=spectral.fillna('')
spectral=spectral.replace('nan','')

assays=ct.carrot_cleanup(assays)
assays=ct.column_cleanup(assays,mapping=config.depth_mapping)
assays=ct.column_cleanup(assays,mapping=config.file_mapping)
assays=assays.fillna('')

assays=assays.replace('nan','')



final=pd.merge(assays,spectral,on='sample_id',how='inner',sort=True)
final.to_csv(f'Master_Spectral_Assay_Merge_Clean_{date}')