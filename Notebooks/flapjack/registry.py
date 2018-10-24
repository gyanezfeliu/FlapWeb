import pandas as pd
import pandas.io.sql as psql
from sqlalchemy import create_engine
from sqlalchemy.orm import mapper, sessionmaker, aliased
import numpy as np
import flapjack
from flapjack import tables, upload
import os


class Registry:
    '''
    The registry class connects to the database and provides functions to extract data
    by querying, joining and filtering.

    Data is returned as Pandas dataframes for analysis and visualisation.
    '''
    def __init__(self, database_name, username, password):
        '''
        database_name : str, the database name data will be collected from
        password: str, the password for such database
        '''

        self.engine = create_engine("postgresql://{}:{}@localhost/{}".format(username, password, database_name))
        '''
        engnine that connects the database
        '''
        
        self.Session = sessionmaker(bind=self.engine)
        '''
        session entablished with the engine
        '''

    def session(self):
        '''
        Generate and return a database session
        '''
        return self.Session()

    def load_from_file(self, path='.', fileformat='synergy'):
        session = self.session()
        cwd = os.getcwd()
        file_list = os.listdir(path) #os.path.join(cwd,path))

        # THIS IS VERY IMPORTANT!!! THIS ARE THE MEASUREMENTS THAT ARE BEING LOOKED FOR
        medidas = ['OD600:600', 'RFP-YFP:585/10,620/15', 'RFP-YFP:500/27,540/25', 'CFP:420/50,485/20'] 

        #loads all the files specified
        print('Reading files from %s/'%path)
        for filename in file_list:
                if '.xlsx' in filename:
                    upload.load(os.path.join(path,filename), fileformat, session, self.engine, medidas)
        session.commit()
        print('Finished loading data.')

    def join_all(self):
        session = self.Session()
        qjoin = session.query(tables.measurements,\
                                tables.samples,\
                                tables.plasmids,\
                                tables.cells,\
                                tables.experiments)\
                                .outerjoin(tables.samples)\
                                .outerjoin(tables.vectors)\
                                .outerjoin(tables.plasmids)\
                                .outerjoin(tables.cells)\
                                .outerjoin(tables.experiments)

        return qjoin

    def possible_values(self, dataframe, column_name):
        return dataframe[column_name].dropna().unique()

    def get_table(self, table_name):
        return psql.read_sql_table(table_name, self.engine)

    def get_data(self, session, query):
        '''
        Return Pandas dataframe for query joined to supplements/inducers tables
        This forms the complete data frame with multiple supplements per sample
        Replaces the concentration column name with the inducer name, e.g. column aTc 
        is the concentration of supplement with inducer name aTc
        '''
        qsupplements = session.query(tables.supplement, tables.inducers)
        qsupplements = qsupplements.filter(tables.supplements.inducer_id==tables.inducers.id)
        session.commit()
        dfsupplements = pd.read_sql_query(qsupplements.selectable, self.engine)
        supplements_grps = dfsupplements.groupby('inducers_name')

        df = pd.read_sql_query(query.selectable, self.engine)
        #print('---')
        #print(len(df))
        for id,sup in supplements_grps:
            sup = sup.rename(index=str, columns={'supplements_concentration':id})
            df = pd.merge(df, sup, left_on='samples_id', right_on='supplements_sample_id', how='left', suffixes=['1','2'])
            fillvals = {id:-1}
            df = df.fillna(value=fillvals)
        #print('---')
        df.sort_values('samples_id')
        df.sort_values('measurements_time')
        #print(df.columns)
        #print(len(df[df.inducers_name_x.isnull()]))

        fillvals = {'supplements_concentration_x': -1, \
            'supplements_concentration_y': -1, \
            'inducers_name_x': 'None', \
            'inducers_name_y': 'None'}
        #df = df.fillna(value=fillvals)
        return df

    def query(self, session):
        '''
        Returns a query object that selects all measurment data,
        to be filtered and passed to get_data() to extract all supplement data

        e.g. dataframe = registry.get_data(registry.query().filter(tables.plasmids.id=='myplasmid'))
        '''
        # Join all main tables (implicit join)
        q = session.query(  tables.measurement,\
                            tables.sample,\
                            tables.dna,\
                            tables.vector,\
                            tables.experiment)
        # Where clause to match up ids
        q = q.filter(tables.measurement.sample_id==tables.sample.id)\
                            .filter(tables.vector.dna_id==tables.dna.id)\
                            .filter(tables.vector.sample_id==tables.sample.id)\
                            .filter(tables.sample.experiment_id==tables.experiment.id)
        # Return the resulting query                 
        return q



