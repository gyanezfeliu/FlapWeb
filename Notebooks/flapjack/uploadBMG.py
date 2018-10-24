import sys, os, datetime, csv, sqlalchemy
import numpy as np
import tables as tbc


from sqlalchemy import Column, Float, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

usage = """usage:
ConvertPlateReader.py infile outfile row-name*

"""
def find_in_sublists(lst, value):
    for sub_i, sublist in enumerate(lst):
        try:
            return (sub_i, sublist.index(value))
        except ValueError:
            pass
    raise ValueError('%s is not in lists' % value)


def measurements_uBMG(session, filename, rownames, offset):
    nsets = len(rownames)
    rawdata = list(csv.reader(open(filename, 'rU')))

    # Work out location of header row, and column/row numbers
    try:
        (headerrow,ccol) = find_in_sublists(rawdata,'Well\nCol')
        (headerrow,crow) = find_in_sublists(rawdata,'Well\nRow')
    except ValueError:
        (headerrow,ccol) = find_in_sublists(rawdata,'Well Col')
        (headerrow,crow) = find_in_sublists(rawdata,'Well Row')

    # Time is on row below headers
    timerow = headerrow+1
    # Data is on rows below time
    datarow = timerow+1

    # Find where the data is in each row by looking for 1st 'Raw Data'
    headers = rawdata[headerrow]
#    print headers
    cdata = (i for i,v in enumerate(headers) if 'Raw Data' in v).next()
#    print cdata
    r = rawdata[datarow:]
    r1 = r[1]
#    print r1[cdata:]
#    for d in r1[cdata:]:
#        print map(float, d)

    # Pull out row,col and data for each row
    # Try combinations of alpha/numeric for row/col
    try:
        rows = [(ord(row[crow].upper())-64, int(row[ccol]), map(float, row[cdata:])) for row in rawdata[datarow:]]
    except ValueError:
        rows = [(int(row[ccol]), ord(row[crow].upper())-64, map(float, row[cdata:])) for row in rawdata[datarow:]]

    # Pull out time of each data point
    times = rawdata[timerow]
    times = times[cdata:]

    assert len(rows[0][2]) % nsets == 0
    nsteps = len(rows[0][2]) / nsets


    data = [['','row','col','t'] + rownames]
    

    n = 1
    for row, col, vals in rows:
        for i in range(nsteps):
            t = float(times[i])*60
            line = [n, row, col, t]
            for j in range(nsets):
                k = j*nsteps + i
                line.append(vals[k])
                m = tbc.measurements(name = rownames[j], value = vals[k], time = t, sample_id = offset + row*col)
                session.add(m)
            data.append(line)
            n = n+1

if __name__=='__main__':
    filename = sys.argv[1]
    database = sys.argv[2]
    rownames = sys.argv[3:]
    engine = sqlalchemy.create_engine("postgresql://postgres:996441@localhost/%s"%(database))
    Session = sessionmaker(bind=engine)
    session = Session()
    measurements_uBMG(sesssion, filename, rownames)
    session.commit()
    
