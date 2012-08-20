import sys
import os
import shutil
import csv
import argparse

IS_PY3 = sys.version_info >= (3,)
if IS_PY3:
    unicode = str
    csv_mode = 't'
    csv_kw = {'newline': '', 'encoding': 'UTF-8'}
    encode_filename = lambda x: x
else:
    csv_mode = 'b'
    csv_kw = {}
    encode_filename = lambda x: x.encode('UTF-8')
    

DB_FILENAME = 'phynk.db'
IMAGE_EXTS = set(('jpg', 'png', 'gif',))

def gather(source_dir, image_exts):
    for root, dirs, files in os.walk(unicode(source_dir)):
        for filename in files:
            if os.path.splitext(filename)[1][1:].lower() in IMAGE_EXTS:
                stat = os.stat(os.path.join(root, filename))
                yield root, filename, stat

def init_command(args):
    source_dir = args.source_dir
    data_dir = args.data_dir
    image_exts = IMAGE_EXTS # Make into an option
    db_path = os.path.join(data_dir, DB_FILENAME)
    
    with open(db_path, 'w'+csv_mode, **csv_kw) as db:
        csvdb = csv.writer(db)
        csvdb.writerow(['Phynk v1', 'NAME'])

        for root, filename, stat in gather(source_dir, image_exts):
            try:
                csvdb.writerow([encode_filename(filename), str(stat.st_size), str(stat.st_mtime)])
            except:
                csvdb.writerow([encode_filename(filename), str(stat.st_size), str(stat.st_mtime)])
                    

def sync_command(args):
    source_dir = args.source_dir
    data_dir = args.data_dir
    image_exts = IMAGE_EXTS # Make into an option
    
    db_path = os.path.join(data_dir, DB_FILENAME)
        
    with open(db_path, 'r'+csv_mode, **csv_kw) as db:
        csvdb = csv.reader(db)
        header = next(csvdb)
        filetype = header[0]
        if filetype.startswith('\xef\xbb\xbf'):
            # Somebody edited it with a brain dead editor, which inserted a
            # BOM, even though UTF8 has no BOM.
            filetype = filetype[3:]
        if filetype != 'Phynk v1':
            raise ValueError('The file {0} does not seem to be a Phynk database!'.format(db_path))

        allpics = {}
    
        for fileinfo in csvdb:
            
            filename, size, mtime = fileinfo
            if not IS_PY3:
                filename = filename.decode('UTF-8')
            size = int(size)
            mtime = float(mtime)
            
            allpics[filename] = mtime
            
    with open(db_path, 'a'+csv_mode, **csv_kw) as db:
        csvdb = csv.writer(db)
        new_files = 0
        for root, filename, stat in gather(source_dir, image_exts):
            if filename in allpics:
                continue
            
            # TODO: Only print this if -v is passed in:
            print("New file %s found" % os.path.join(root, filename))
            try:
                shutil.copy2(os.path.join(root, filename), data_dir)
            except:
                # Remove partially copied file:
                target_file = os.path.join(data_dir, filename)
                if os.path.exists(target_file):
                    print("Removing partially copied file")
                    os.unlink(target_file)
                # Re-raise the original exception
                raise
            new_files += 1
            csvdb.writerow([encode_filename(filename), str(stat.st_size), str(stat.st_mtime)])
            
        #TODO: Print a summary
        print("{0} new files found".format(new_files))

def phynk_entry_point():
    parser = argparse.ArgumentParser('phynk', description='Photo synchronization utility')
    subparsers = parser.add_subparsers(title='Commands')
    
    init_parser = subparsers.add_parser('init', help='Create the initial photo database from the primary collection of photos')
    init_parser.add_argument('source_dir', help='The directory that contains your main collection of photos. ex /home/username/Pictures')
    init_parser.add_argument('data_dir', help='The directory where the database should be created. This is typically a USB drive or similar. ex /media/MyUSB')
    init_parser.set_defaults(func=init_command)
    
    sync_parser = subparsers.add_parser('sync', help='Find missing photos in a secondary collection of photos')
    sync_parser.add_argument('source_dir', help='The directory that contains a secondary collection of photos. ex /home/username/Pictures')
    sync_parser.add_argument('data_dir', help='The directory where the database is located, and where the photos will be copied. This is typically a USB drive or similar. ex /media/MyUSB')
    sync_parser.set_defaults(func=sync_command)
    
    args = parser.parse_args()
    args.func(args)
    
    
if __name__ == '__main__':
    phynk_entry_point()