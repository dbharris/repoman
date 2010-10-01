#!/bin/bash

# intro

BLANKSPACE='/mnt'
IMAGE=$BLANKSPACE/filesystemcopy.img
DESTDIR=$BLANKSPACE/fscopy

echo $$ > /var/lock/interactive.sh.lock


# create the image
SIZE=`df / | awk '{ if (NR == 2) {print $2} }'`
USED=`df / | awk '{ if (NR == 2) {print $3} }'`
BS_SIZE=`df /mnt | awk '{ if (NR == 2) {print $2} }'` 

if [ $BS_SIZE -lt $USED ]; then
    echo "insufficient blankspace"
    echo "BLANKSPACE: " $BS_SIZE
    echo "IMAGE SIZE: " $SIZE
    echo "SPACE USED: " $USED
    exit
fi

if [ $BS_SIZE -lt $SIZE ]; then
    $SIZE = $BS_SIZE
fi

dd if=/dev/zero of=$IMAGE count=0 bs=1k seek=$SIZE

mkfs -t ext3 $IMAGE


#image created, now mount it:
mkdir -p $DESTDIR
mount -o loop $IMAGE $DESTDIR
mkdir $DESTDIR/{dev,proc,sys,mnt,tmp}
chmod 777 $DESTDIR/tmp

#copy the filesystem:
nice -n 20 rsync -ax --exclude /dev --exclude /proc --exclude /sys --exclude /mnt --exclude /tmp / $DESTDIR/

rm /var/lock/interactive.sh.lock
