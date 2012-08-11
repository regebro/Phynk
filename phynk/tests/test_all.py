# -*- coding: utf-8 -*-

import unittest
import os
import tempfile
import phynk.main

class GatherTargetTest(unittest.TestCase):
    
    def test(self):
        target_dir = os.path.join(os.path.split(__file__)[0], 'target')
        db_dir = tempfile.gettempdir()
        
        phynk.main.gather_target(target_dir, db_dir)
        
        db_file = os.path.join(db_dir, 'phynk.db')
        with open(db_file, 'rt') as db:
            data = db.read()
            
        self.failUnless(data.startswith('Phynk v1,NAME\r\n'))
        self.failUnless('Petter Lundborg.JPG,2007609' in data)
        self.failUnless('Coffee diagram.png,129118' in data)
        self.failUnless('Högasvägen copy.jpg,1985600' in data)
        self.failUnless('lennartstudent2.jpg,1328952' in data)
        self.failUnless('lennart lifts the fa cup.jpg,30380' in data)
        self.failUnless('The King of Sweden.png,1011234' in data)
        self.failUnless('mac manc mcmanx.gif,11262' in data)
        
        self.failIf('somedbfile.db' in data)
        self.failIf('notanimage.txt' in data)
        
        # Cleanup:
        os.unlink(db_file)

class GatherSourceTest(unittest.TestCase):
    
    def test(self):

        target_dir = os.path.join(os.path.split(__file__)[0], 'target')
        source_dir = os.path.join(os.path.split(__file__)[0], 'source')
        db_dir = tempfile.gettempdir()
        
        phynk.main.gather_target(target_dir, db_dir)
        phynk.main.collect_source(source_dir, db_dir)
        
        db_file = os.path.join(db_dir, 'phynk.db')
        with open(db_file, 'rt') as db:
            data = db.read()

            self.failUnless(data.startswith('Phynk v1,NAME\r\n'))
            self.failUnless('Petter Lundborg.JPG,2007609' in data)
            self.failUnless('Coffee diagram.png,129118' in data)
            self.failUnless('Högasvägen copy.jpg,1985600' in data)
            self.failUnless('lennartstudent2.jpg,1328952' in data)
            self.failUnless('lennart lifts the fa cup.jpg,30380' in data)
            self.failUnless('The King of Sweden.png,1011234' in data)
            self.failUnless('mac manc mcmanx.gif,11262' in data)
            
            # New files:
            self.failUnless('2011-10-06 17.29.43.jpg,528192' in data)
            self.failUnless('paris.jpg,2468952' in data)
            self.failUnless('The King of Sweden 2.png,1247728' in data)
            
            tmpdirfiles = os.listdir(db_dir)
            self.failUnless('2011-10-06 17.29.43.jpg' in tmpdirfiles)
            self.failUnless('paris.jpg' in tmpdirfiles)
            self.failUnless('The King of Sweden 2.png' in tmpdirfiles)            
            
            self.failIf('somedbfile.db' in data)
            self.failIf('notanimage.txt' in data)

            # Cleanup:
            for filename in ('2011-10-06 17.29.43.jpg', 
                             'paris.jpg',
                             'The King of Sweden 2.png',
                             'phynk.db'):
                os.unlink(os.path.join(db_dir, filename))
        
        
if __name__ == '__main__':
    unittest.main()