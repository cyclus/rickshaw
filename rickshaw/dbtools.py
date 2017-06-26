"""Tools for merging and splitting Cyclus databases."""
import os
import shutil
from argparse import ArgumentParser
from contextlib import contextmanager

from cyclus import lib

@contextmanager
def db_open(file_name):
    rec = lib.Recorder(inject_sim_id=False)
    prefix, ext = os.path.splitext(file_name)
    if ext == '.h5':
        db = lib.Hdf5Back(file_name)
    elif ext == '.sqlite':
        db = lib.SqliteBack(file_name)
    else:
        raise ValueError('Unsupported file type')
    rec.register_backend(db)
    yield (rec, db)
    rec.flush()
    db.close()
    rec.close()
    
def merge(first, second, outfile=None):
    if outfile is not None:
        shutil.copyfile(second, outfile)
        second = outfile
    with db_open(first) as (frec, fdb), db_open(second) as (srec, sdb):
        for table in fdb.tables:
            print(table)
            data = fdb.query(table)
            schema = fdb.schema(table)
            datad = data.to_dict(orient='list')
            for i in range(len(data)):
                d = srec.new_datum(table)
                for colinfo in schema:
                    colname = colinfo.col
                    d.add_val(colname, datad[colname][i], type=colinfo.dbtype, shape=colinfo.shape)
                d.record()
                srec.flush()

def merge_action(ns):
    merge(ns.first, ns.second, outfile=ns.outfile)

def build_parser():
    p = ArgumentParser('dbtools')
    subp = p.add_subparsers(title='command', dest='command')
    mergep = subp.add_parser('merge', help='Merges databases.')
    mergep.add_argument('first', help='First file to merge.')
    mergep.add_argument('second', help='Second file to merge.')
    mergep.add_argument('-o', '--outfile', dest='outfile', default=None, help='Optional file to store merge result.')
    return p

MAIN_ACTIONS = {'merge': merge_action}

def main(args=None):
    p = build_parser()
    ns = p.parse_args(args=args)
    MAIN_ACTIONS[ns.command](ns)

if __name__ == '__main__':
    main()                    
                    
                    
