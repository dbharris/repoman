#!/usr/bin/env python
'''
Created on Sep 16, 2010

@author: fransham
'''
import repo_tools
from time import sleep
from daemon import Daemon 
import sys
import threading
import SocketServer

class ThreadedTCPRequestHandler(SocketServer.BaseRequestHandler):

    def handle(self):
        repo = repo_tools.ImageRepository()
        data = self.request.recv(1024)
        self.request.settimeout(10)
        command = data.rsplit()
        print command[0]
        
        if command[0].startswith("list"):
            response = repo.get_images(command[1])
            for message in  response:
                print message[0]+"  "+message[1]
                self.request.send(message[0]+"  "+message[1])
            self.request.send("") # send a null command to close the connection
            
        elif command[0].startswith("geturl"):
            response = repo.get_url(command[1], command[2])
            for message in  response:
                self.request.send(message[0])
            self.request.send("")
            
        elif command[0].startswith("save"):
            self.request.send("doit")
            while True:
                data = self.request.recv(1024)
                
                if not data:
                    print "Connection to VM lost"
                    repo.flag_as_bad(command[]1, command[2])    
                       
                #check of the rsync is still ongoing
                elif data.startswith("copying"):
                    self.request.send("okay")
                    sleep(5)
                            
                #check if the save is done
                elif data.startswith("complete"):
                    self.request.send("ktnxbye")
                    break
                
                else:
                    print "Connection to VM lost"
                    repo.flag_as_bad(command[]1, command[2])    
                    
               
            
                
                              
#            try:
#                print command[1]+" "+command[2]
#                mounted_at = repo.mount(command[1], command[2])
#            except repo_tools.MountError as e:
#                #crap, something failed.  Tell the client that there's a problem
#                self.request.send("ERROR: Mounting of image failed." + e.msg)
#            else:
#                # if the mount command succeeded, it will return the path 
#                # to the mounted image 
#                self.request.send(mounted_at)
#            
#                # now wait for the client to do an rsync.  This can take a while.  
#                # the client is responsible for keeping the socket open, otherwise 
#                # the image will be unmounted.
#                try:
#                    while True:
#                        data = self.request.recv(1024)
#                        
#                        #check of the rsync is still ongoing
#                        if data.startswith("copying"):
#                            self.request.send("okay")
#                            sleep(5)
#                            
#                        #check if the save is done
#                        elif data.startswith("complete"):
#                            self.request.send("ktnxbye")
#                            break
#                        
#                        #oops, something went wrong
#                        else:
#                            raise Exception("Connection to VM lost")
#                            print "Connection to VM lost"
#                        
#                except Exception as e:
#                    print e.msg
#                    #the copy didn't succeed.  Mark the image as bad.
#                    repo.flag_as_bad(command[1], command[2])
#                #sweet, everything is okay.  unmount the image and we're done!
#                try:
#                    repo.umount(command[1], command[2])
#                except repo_tools.MountError as e:
#                    #crap, something failed.  Tell the client that there's a problem
#                    print e.msg
#                    #self.request.send("ERROR: Unmounting of image failed." + e.msg)
#                    
                             
            

class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    pass


class RepoMgr(Daemon):    

    def run(self):
        HOST, PORT = "alto.cloud.nrc.ca", 21567

        server = ThreadedTCPServer((HOST, PORT), ThreadedTCPRequestHandler)
        ip, port = server.server_address

        # Start a thread with the server -- that thread will then start one
        # more thread for each request
        server_thread = threading.Thread(target=server.serve_forever)
        # Exit the server thread when the main thread terminates
        server_thread.setDaemon(True)
        server_thread.start()
        print "Server loop running in thread:", server_thread.getName()  
        server.serve_forever()              
                        
                        
                        
 
if __name__ == "__main__":
        daemon = RepoMgr('/tmp/daemon-example.pid')
        if len(sys.argv) == 2:
                if 'start' == sys.argv[1]:
                        daemon.start()
                elif 'stop' == sys.argv[1]:
                        daemon.stop()
                elif 'restart' == sys.argv[1]:
                        daemon.restart()
                else:
                        print "Unknown command"
                        sys.exit(2)
                sys.exit(0)
        else:
                print "usage: %s start|stop|restart" % sys.argv[0]
#
                sys.exit(2)
