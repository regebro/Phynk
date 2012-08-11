import sys
import os
import codecs
import shutil
import csv

DB_FILENAME = 'phynk.db'
IMAGE_EXTS = set(('jpg', 'png', 'gif',))

def gather(target_path, image_exts):
    for root, dirs, files in os.walk(unicode(target_path)):
        for filename in files:
            if os.path.splitext(filename)[1][1:].lower() in IMAGE_EXTS:
                stat = os.stat(os.path.join(root, filename))
                yield root, filename, stat

def gather_target(target_path, db_dir, image_exts=IMAGE_EXTS):
    db_path = os.path.join(db_dir, DB_FILENAME)
        
    with open(db_path, 'wb') as db:
        csvdb = csv.writer(db)
        csvdb.writerow(['Phynk v1', 'NAME'])

        for root, filename, stat in gather(target_path, image_exts):
            try:
                csvdb.writerow([filename.encode('UTF-8'), str(stat.st_size), str(stat.st_mtime)])
            except:
                import pdb;pdb.set_trace()
                csvdb.writerow([filename.encode('UTF-8'), str(stat.st_size), str(stat.st_mtime)])
                    

def collect_source(source_path, db_dir, image_exts=IMAGE_EXTS):
    db_path = os.path.join(db_dir, DB_FILENAME)
        
    with open(db_path, 'rb') as db:
        csvdb = csv.reader(db)
        header = csvdb.next()
        if header[0] != 'Phynk v1':
            raise ValueError('The file {} does not seem to be a Phynk database!'.format(db_path))

        allpics = {}
    
        for fileinfo in csvdb:
            
            filename, size, mtime = fileinfo
            filename = filename.decode('UTF-8')
            size = int(size)
            mtime = float(mtime)
            
            allpics[filename] = mtime
            
    with open(db_path, 'ab') as db:
        csvdb = csv.writer(db)
        new_files = 0
        for root, filename, stat in gather(source_path, image_exts):
            if filename in allpics:
                continue
            
            # TODO: Only print this if -v is passed in:
            print("New file %s found" % os.path.join(root, filename))
            try:
                shutil.copy2(os.path.join(root, filename), db_dir)
            except:
                # Remove partially copied file:
                target_file = os.path.join(db_dir, filename)
                if os.path.exists(target_file):
                    print("Removing partially copied file")
                    os.unlink(target_file)
                # Re-raise the original exception
                raise
            new_files += 1
            csvdb.writerow([filename.encode('UTF-8'), str(stat.st_size), str(stat.st_mtime)])
            
        #TODO: Print a summary
        print("{} new files found".format(new_files))
    
if __name__ == '__main__':
    # TODO: Proper argparse/optparse support
    if sys.argv[1] == 'init':
        gather_target(sys.argv[2], sys.argv[3])
    if sys.argv[1] == 'sync':
        collect_source(sys.argv[2], sys.argv[3])
