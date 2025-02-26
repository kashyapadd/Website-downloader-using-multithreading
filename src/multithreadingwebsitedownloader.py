import random
from urllib import urlretrieve
import socket
import Queue
import time
import threading
from HTMLParser import *

#website = "www.ece.eng.wayne.edu"
q = Queue.Queue(100)
# threadLock = threading.Lock()
website = raw_input ("Enter the website process:")

class HTMLClassifier(HTMLParser):
    def handle_starttag(self, tag, attrs):
        if tag == "img":
            threads=threads+1
            for attr, url in attrs:
               if attr == "src":
                    if url[0] == '/':
                         url = website + url
                    full = url
                    # threadLock.acquire()
                    q.put(full)
                    # threadLock.release()

    def handle_endtag(self, tag):
        pass

    def handle_data(self, data):
        pass

def parseHTML(htmlData):
    parser = HTMLClassifier()
    parser.feed(htmlData)
    pass

def download_web_image(url):
     name = random.randrange(1,1000)
     fileName = str(name) + ".jpg"
     if ("http://" in url) or ("https://" in url): 
            fullUrl = url
     else: 
            fullUrl = "http://" + url
     urlretrieve(fullUrl, fileName)

class myThread(threading.Thread):
    def __init__(self, threadId, name):
        threading.Thread.__init__(self)
        self.threadId = threadId
        self.name = name

    def run(self):
        print "Starting " + self.name
        work(self.threadId)
        print "Stopping " + self.name + "\n"

def work(threadId):
    printQueue(threadId)
    # time.sleep(10)

def printQueue(threadId):
    while not q.empty():
        imageUrl = q.get()
        print str(threadId) + " Downloading " + imageUrl + "\n"
        download_web_image(imageUrl)

def main():
    #Defining port number for the website
    port = 80
    #Creating a socket or initializing
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("Student_1:Jahnavi Latha Laveti\nStudent_2:Sesha Sai Kashyap Addanki\nThe program is interpreted correctly and completely verified. Images are downloaded")
    #Getting the ip address of the host name of the website
    ipAddress = socket.gethostbyname(website)
    #printing the ip Address
    print ("IP Address:",ipAddress)
    #Connecting to the website using the ip address and the port number
    s.connect((ipAddress, port))
    #Sending the request to the server
    s.sendall("GET / HTTP/1.0\r\n\r\n")
    #Infinite loop and receive website content by a 1 Mega Byte
    htmlData = ""

    while True:
        response = s.recv(4096)
        if response == "":
            break
        #This is the response data
        htmlData += response
    parseHTML(htmlData)
    pos = htmlData.find("\r\n\r\n")
    htmlData = htmlData[pos:]
    fileName = open("downloaded.html","w")
    fileName.truncate()
    fileName.write(htmlData)

    threads = ["1", "2"]
    threadId = 1

    for i in threads:
        thread = myThread(threadId, i)
        thread.start()
        threadId += 1

    while not q.empty():
        pass

    print "Successful!"
    s.close()

if __name__ == '__main__':
    main()
