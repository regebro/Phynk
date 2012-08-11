Phynk
=====

Phynk is a "photo synchronizer" (hence the name Phynk). It's purpose is to
make sure that none of your vacation, baby, dog, concert, nature or
whatever-you-fancy photos are languishing unseen on one of your households
many computers.

It is written in Python to be easily portable to many different systems, so
it should support Windows, Mac OS X and Linux as a bare minimum.

Usage
-----

The main use case for Phynk is where you have one system that you are using
to show people all your pictures. This is often a computer of some sort, but
could just as well be a USB harddrive connected to your TV, decoder or set
top box.

But there may be several people with several cameras and several computers in
the household, and often pictures will end up being copied into the hard disk
on one computer, and then forgotten about.

You are also assumed to use some sort of photo manager software, such as
Shotwell, that will import photos and help you organize them.

What Phynk will help you with is that it will index the pictures on your main
system, and then you can ask it to look through the picture folders on your
other computers, and copy the ones that are missing from the main system to a
USB key or network folder etc, and then you can import the missing photos
with your photo manager software.

The typical process is this:

1. Take an empty USB key, and put it into the main computer that you are using.

2. From the command line, run "phynk init <picturefolder> <usbkey>" to index
   the photos you have on the main system. On Linux this would typically look
   something like this:
   
       $ phynk init /home/username/Photos /media/USB
       
   On Windows it would look something like this:
   
       C:\> "C:\Program Folder\Phynk\phynk" init "C:\User Data\User Name\Pictures"  D:\
       
   Phynk will now in the target folder create a file called phynk.db that contains the
   index of all files found in "C:\User Data\User Name\Pictures" and any folders below.
   
3. Take the USB key and go to the computers where you suspect you have pictures that
   has not been copied to the main system. There run phynk with the "sync" command.
      
       $ phynk sync /home/username/Photos /media/USB
   
   or 
   
       C:\> "C:\Program Folder\Phynk\phynk" init "C:\User Data\Other User\Pictures"  E:\
      
   or similar.
   
   Phynk will now look through the specified folder for pictures that where not on the
   target computer. It will copy them to the USB key, and add them to the database.
   
   
4. Take the USB key with missing pictures back to the main system and import them.

5. Delete the pictures from the USB key, but don't delete the phynk.db file. Then
   take the USB key to the next computer and repeate points 3 again, until you 
   have run out of places to look for missing files.
   
If you have many files, you may run out of space on the USB key. This should not
be a problem, just import the files that fit on the USB key, and then go back to
the computer and run the sync command again.
