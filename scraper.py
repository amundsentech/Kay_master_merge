



import xlwings as xl
import pandas as pd



version1={}
# data with a single value after the header
version1['singular_indicators']=['Total Activity Hours']
# data with multiple columns and rows
version1['block_indicators']=   ['Drilling Information',
                                'Fluids',
                                'Billable Quantities',
                                'Activities']

# data containing only infor about the project 
version1['info_indicator']=['Report Information','Client Information']

version2={}
version2['singular_indicators']=['Total Activity Hours']
# data with multiple columns and rows
version2['block_indicators']=   ['Equip. Description',
                                'Description',
                                'Hourly Distribution',
                                'Footage Summary']

# data containing only infor about the project 
version2['info_indicator']=['Report Information','Client Information']

class scrape_excel():
    def __init__(self,data_path,version):
        # self.wb=xl.Book(data_path)
        version=version
        self.data_sheets=pd.ExcelFile(data_path)
        self.sheet_names=self.data_sheets.sheet_names
        self.data=pd.read_excel(data_path,sheet_name=self.sheet_names[0])
        self.data=self.integer_columns()

    def integer_columns(self):
        self.data.columns=range(len(self.data.columns))
        return self.data


def find_info_index(df,name='Total Activity Hours'):
    
    col=df[df==name].dropna(axis=1,how='all').dropna(how='all').columns.values[0]
    row=df[df==name].dropna(axis=1,how='all').dropna(how='all').index.values[0]
    return row,col

def find_info(df,name='shift'):
    col=df[df==name].dropna(axis=1,how='all').dropna(how='all')
    row=df[df==name].dropna(axis=1,how='all').dropna(how='all')
    return row,col

def pull_data(data,name,n_rows=1,n_cols=1,include_header=True):
    row,col=find_info_index(data,name=name)
    if not include_header:
        row =row+1
    slice=data.iloc[row:row+(n_rows+1),col:col+n_cols]
    return slice

def get_singles(data):
    row,col=find_info_index(data,name='Total Activity Hours')
    singular_data=[s for  s in data.iloc[row].dropna()]
    singles=[]
    for s in singular_data:
        slice=pull_data(data=data,name=s)
        singles.append(slice)
    singles=pd.concat(singles,axis=1)
    singles=singles.reset_index(drop=True)
    singles=singles.T.set_index(0,drop=True).T
    return singles

def get_blocks(df,name='Drilling Information',n_rows=9,n_cols=10,transpose=False):
    data=pull_data(df,name=name,n_rows=n_rows,n_cols=n_cols,include_header=False)
    singles=[]
    for col in data .columns:
        s=data[col].dropna(axis=0)
        if len (s)>0:
            singles.append(s)
    singles=pd.concat(singles,axis=1)
    singles=singles.reset_index(drop=True)
    singles=singles.T.set_index(0,drop=True).T
    if transpose:
        singles=singles.T.reset_index()
        singles=singles.T.set_index(0,drop=True).T
    return singles