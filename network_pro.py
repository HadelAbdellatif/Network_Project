from socket import *

dataList = []

def readfile():
    """Read the data of smartphones from the txtfile.txt and fill them in dataList"""
    file = open("txtfile.txt", "r")  # create file that read from input
    infoLine = file.readlines()  # read line by line from file and put the data in info
    for line in infoLine:  # split the data from file and append it in another list
        eachLine = line.split(";")
        eachLine[1] = str(eachLine[1]).replace("\n", "")  # Remove the newline signal
        eachLine[1] = int(eachLine[1])
        dataList.append(eachLine)


readfile()
serverPort = 7000 #The port that enables us to enter the page
# defining the socket, and binding it to the port
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(("127.0.0.1", serverPort))
# socket listening for response
serverSocket.listen(1)
print("The server is ready to receive")

while True:
    connectionSocket, add = serverSocket.accept() #creates a new socket to communicate with the client
    sentence=connectionSocket.recv(1024).decode()
    print("IP: " + add[0] + ", Port: " + str(add[1]))
    print(sentence)
    try:

        IP = add[0]
        Port = add[1]
        List = sentence.split(' ')  # Split request from spaces
        method = List[0]
        request_File = List[1]
        connectionSocket.send(f"HTTP/1.1 200 OK\r\n".encode())
        myNewfile = request_File.split('?')[0]  # After the "?" symbol not relevent here
        myNewfile = myNewfile.lstrip('/')

        if myNewfile == '':
            myNewfile = 'index.html'  # Default File

        elif myNewfile.lower() == 'sortbyname' or myNewfile.lower() == 'sortbyprice':
            # if the user requests to sort the smartphones, it will enter this IF condition
            if myNewfile.lower() == 'sortbyname':
                # Sort the data according to the names of the phone ascending
                dataList.sort()
                outstring = '<html><head><style>#phones {font-family: Arial, Helvetica, sans-serif;text-align:center;border-collapse: collapse;width: 50%;}  #phones td, #phones th {border: 1px solid #ddd;padding: 8px;}  #phones tr:nth-child(even){background-color: #f2f2f2;}  #phones tr:hover {background-color: #ddd;}  #phones th {padding-top: 12px;padding-bottom: 12px;text-align: left;text-align:center;color: white;}</style></head><body><center><h1>Sort By Name</h1><table id="phones"><tr style="background-color: #4CAF50;"><th>Logo</th><th>Name</th><th>Price</th></tr>'
            else:
                # Sort the data according to the prices of the phone ascending
                dataList.sort(key=lambda data: data[1])
                outstring = '<html><head><style>#phones {font-family: Arial, Helvetica, sans-serif;text-align:center;border-collapse: collapse;width: 50%;}  #phones td, #phones th {border: 1px solid #ddd;padding: 8px;}  #phones tr:nth-child(even){background-color: #f2f2f2;}  #phones tr:hover {background-color: #ddd;}  #phones th {padding-top: 12px;padding-bottom: 12px;text-align: left;text-align:center;color: white;}</style></head><body><center><h1>Sort By Price</h1><table id="phones"><tr style="background-color: #4CAF50;"><th>Logo</th><th>Name</th><th>Price</th></tr>'

            # We will use sorted.html to show our sorted data
            myNewfile = 'sorted.html' # change name of index.html to sorted.html
            for chocklet in dataList: # for each phone in dataList
                # FOR loop used to check every phone in data list

                # and IF condition used to put a company logo for each phone in html file
                if str(chocklet[0]).startswith("Galaxy"):
                    outstring += '<tr><th style="width: 10%"><img src="images\Galaxy.jpg" style="width: 50px"></th>'
                elif str(chocklet[0]).startswith("Hershey"):
                    outstring += '<tr><th style="width: 10%"><img src="images\Hershey.jpg" style="width: 50px"></th>'
                elif str(chocklet[0]).startswith("Jewels"):
                    outstring += '<tr><th style="width: 10%"><img src="images\Jewels.jpg" style="width: 50px"></th>'
                elif str(chocklet[0]).startswith("Lotus"):
                    outstring += '<tr><th style="width: 10%"><img src="images\Lotus.png" style="width: 50px"></th>'
                elif str(chocklet[0]).startswith("M&Ms"):
                    outstring += '<tr><th style="width: 10%"><img src="images\M&Ms.jpg" style="width: 50px"></th>'
                elif str(chocklet[0]).startswith("Mackintosh"):
                    outstring += '<tr><th style="width: 10%"><img src="images\Mackintosh.jpg" style="width: 50px"></th>'
                elif str(chocklet[0]).startswith("Mars & Snickers"):
                    outstring += '<tr><th style="width: 10%"><img src="images\Mars&Snickers.jpg" style="width: 50px"></th>'
                elif str(chocklet[0]).startswith("Merci"):
                    outstring += '<tr><th style="width: 10%"><img src="images\Merci.jpg" style="width: 50px"></th>'
                elif str(chocklet[0]).startswith("Oreo"):
                    outstring += '<tr><th style="width: 10%"><img src="images\Oreo.jpg" style="width: 50px"></th>'
                elif str(chocklet[0]).startswith("Raffaello"):
                    outstring += '<tr><th style="width: 10%"><img src="images\Raffaello.jpg" style="width: 50px"></th>'
                else:
                    outstring += '<tr><th style="width: 10%"><img src="images\Dairy Milk.jpg" style="width: 50px"></th>'
                outstring += '<td>' + chocklet[0] + '</td><td>$' + str(chocklet[1]) + '</td></tr>'
            outstring += "</table></center></body></html>"

            # sorted.html will be opened and overwritten by the string 'outstring'
            f = open("sorted.html", "w")
            f.write(outstring)
            f.close()

        # to open and read the requested file in byte format
        request_File = open(myNewfile, 'rb') # rb : read in byte
        response = request_File.read()
        request_File.close()

        # The following IF condition is to specify the type of the requested file

        #if the request is a .jpg then the server should send the jpg image with Content-Type:
        if myNewfile.endswith(".jpg"):
            connectionSocket.send(f"Content-Type: image/jpg \r\n".encode())

        # - if the request is a .png then the server should send the png image with Content-Type:
        elif myNewfile.endswith(".png"):
            connectionSocket.send(f"Content-Type: image/png \r\n".encode())

        #- if the request is a css then the server should send html file with Content-Type: text/css.
        elif myNewfile.endswith(".css"):
            connectionSocket.send(f"Content-Type: text/css \r\n".encode())

        #if the request is an .html then the server should send html file with Content-Type:
        else:
            connectionSocket.send(f"Content-Type: text/html \r\n".encode())

    #If the request is wrong or the file doesn’t exist the server should return a simple HTML webpage that contains (Content-Type: text/html)
    except Exception as e:
        # When an exception handled, it will return a simple HTML with our IDs
        header = 'HTTP/1.1 404 Not Found\n\n'
        response = (
                '<html><title>Error</title><body><center><h1 style="color: red;>Error 404: Not found</h1><hr><p style="color: red;>Error</p><p style= "font-weight: bold;">Hadeel Abdellatif - 1190451</p><p style= "font-weight: bold;">Hiba Khaled - 1191621</p><p style= "font-weight: bold;">Dana Hammad - 1191568</p><hr><h2>IP: ' + str(
            IP) + ', Port: ' + str(Port) + '</h2></center></body></html>').encode('utf-8')
    connectionSocket.send(f"\r\n".encode())
    connectionSocket.send(response)
    connectionSocket.close()
