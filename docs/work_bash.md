# Notes from [Hima_Work](https://github.com/bahim22/work) Repository

## Encryption, Security, Linux

| SSH | GPG | Git | Commands | permissions |
|--- | ---| ---|--- | ---|
| | | | | |

- [Notes from Hima\_Work Repository](#notes-from-hima_work-repository)
	- [Encryption, Security, Linux](#encryption-security-linux)
	- [Git info](#git-info)
	- [SSH to GitHub](#ssh-to-github)
		- [initial ssh example](#initial-ssh-example)
		- [ssh-keygen cmds](#ssh-keygen-cmds)
		- [Example ssh connect](#example-ssh-connect)
		- [GPG key](#gpg-key)
	- [Git Commands \& examples](#git-commands--examples)
	- [Bash Script Info](#bash-script-info)
		- [Bash commands](#bash-commands)
		- [curl](#curl)
		- [Bash Scripting](#bash-scripting)
	- [Shell command info](#shell-command-info)
	- [Symbolic rep of data](#symbolic-rep-of-data)
	- [Linux permissions](#linux-permissions)
	- [PowerShell](#powershell)

## Git info

```sh
echo "# Scheduling App" >> README.md
git init
git add .
git commit -m $message
git branch -M dev
git remote add origin git@github.com:bahim22/engage_flower.git
ssh -T -v git@github.com
git push -u origin dev
git remote -v
git branch --v

# edit ssh config file
code ~/.ssh/config

# install node, nvm, npm
curl -o- --dns-servers 1.1.1.1 --compressed https://raw.githubusercontent.com/nvm-sh/nvm/master/install.sh | bash
nvm install --lts
nvm install node

# install file from github repo
curl -o work_bash.md --dns-servers 1.1.1.1 --compressed https://raw.githubusercontent.com/bahim22/work/ppu/Docs_Scripts/bash_cmds.md
```

___

## SSH to GitHub

> ssh connects and logs into the specified destination by setting the user, hostname and port
<!-- /* cspell: enableCompoundWords */ -->

```bash
#!/bin/bash
# formats for ssh
[user@]hostname | ssh://[user@]hostname[:port]
ssh://[user@]host.xz[:port]/~[user]/path/to/repo.git/
ssh://[user@]host.xz[:port]/path/to/repo.git/
ssh -i ~/.ssh/id_ed25519 # identity file (private key)
ssh -l login_name -p port
ssh-keygen -l -f /etc/ssh/ssh_host_rsa_key
# determine fingerprints
ssh-keygen -lv -f ~/.ssh/known_hosts
# ls fingerprints and random art for known hosts
ssh-keygen -r host.example.com.
# connect client to server
# Add SSHFP resource records to the zonefile for host 1st
dig -t SSHFP host.example.com
# check that zone is answering fingerprint queries.
ssh -o "VerifyHostKeyDNS ask" host.example.com
# client connects

ls -al ~/.ssh
```

### initial ssh example

```bash
# edit git config f
git config --global user.name <username>
git config --global user.email <email@mail.com>
ls -al ~/.ssh # list files in .ssh dir

ssh-keygen -m PEM -t rsa -b 4096
# generates 4096-bit SSH RSA public and private key files by default in the ~/.ssh directory.

ssh-keygen -t ed25519 -C "email@google.com"
# creates pub/priv key pair
# saves to .ssh/id_ed25519 & .ssh/id_ed25519.pub
  # generates key fingerprint & randomart image
eval "$(ssh-agent -s)" #check if agent is running
ssh-add ~/.ssh/id_ed25519 #add id to ~
cat ~/.ssh/id_ed25519.pub # display pub key then c/v to github acct
ssh -T git@github.com # test connection & clone repo
git clone git@github.com:<username>/<repo>.git
code .
git clone ssh://git@ssh.github.com:443/<username>/<repo>.git
```

```bash
ssh-keygen \
-f ~/.ssh/id_rsa.pub \
-e \
-m RFC4716 > ~/.ssh/id_ssh2.pem
# create RFC4716 formatted key from existing SSH pubkey (multiline format in a 'pem' container)

eval "$(ssh-agent -s)"
# cache private key file passphrase on local sys by verifying/using ssh-agent & ssh-add
ssh-add ~/.ssh/id_rsa
# add private key to ssh-agent

ssh-copy-id -i ~/.ssh/id_rsa.pub azureuser@myserver
#  copy existing public key to an existing remote machine
```

- ssh-keygen supports two types of certificates: user and host.
  - User certificates authenticate users to servers
    - placed in /path/to/user_key-cert.pub.
  - Host certificates authenticate server hosts to users
    - requires the -h option
    - host certificate will be output to /path/to/host_key-cert.pub.

```bash
#!/bin/bash

# generate a user certificate:
$ ssh-keygen -s /path/to/ca_key -I key_id /path/to/user_key.pub

# generate a host certificate:
ssh-keygen -s /path/to/ca_key -I key_id -h /path/to/host_key.pub

# copies the local-host’s pub key to the remote-host’s authorized_keys fi
ssh-copy-id
```

### ssh-keygen cmds

- run ssh-keygen to create key pair
  - `private` key stored in:
    - ~/.ssh/id_dsa (DSA), ~/.ssh/id_ecdsa (ECDSA)
    - ~/.ssh/id_ecdsa_sk (authenticator-hosted ECDSA)
    - ~/.ssh/id_ed25519 (Ed25519)
    - ~/.ssh/id_ed25519_sk (authenticator-hosted Ed25519)
    - ~/.ssh/id_rsa (RSA)
  - `public` key stored in user's home dir w/in subdir of:
    - ~/.ssh/id_dsa.pub (DSA), ~/.ssh/id_ecdsa.pub (ECDSA)
    - ~/.ssh/id_ecdsa_sk.pub (authenticator-hosted ECDSA)
    - ~/.ssh/id_ed25519.pub (Ed25519)
    - ~/.ssh/id_ed25519_sk.pub (authenticator-hosted Ed25519)
    - ~/.ssh/id_rsa.pub (RSA)
- Then copy public key to ~/.ssh/authorized_keys in home dir on the remote machine
- The authorized_keys file == ~/.rhosts file
- one key per line
- enables user to login w/o passwd

### Example ssh connect

>
- This example connects client network: 10.0.99.0/24
  - via a point-to-point connection
    - from 10.1.1.1 to 10.1.1.2
- SSH server running on the gateway to the remote network must allow connection 192.168.1.15

```bash
# On the client:
ssh -f -w 0:1 192.168.1.15 true
ifconfig tun0 10.1.1.1 10.1.1.2 netmask 255.255.255.252
route add 10.0.99.0/24 10.1.1.2

# On the server:
ifconfig tun1 10.1.1.2 10.1.1.1 netmask 255.255.255.252
route add 10.0.50.0/24 10.1.1.1
# Client access can be adjusted by editing:
    # /root/.ssh/authorized_keys fi
    # PermitRootLogin server option.

tunnel="1",command="sh /etc/netstart tun1" ssh-rsa ... jane
tunnel="2",command="sh /etc/netstart tun2" ssh-rsa ... john
# above cmds permits connections on:
# tun device 1 from user “jane”
# tun device 2 from user “john”
    # if PermitRootLogin == “forced-commands-only”
```

### GPG key

>>
  generate a gpg key and then c/v to GitHub
  This allows commits to be verified via signature
<!-- cspell: disable  -->
```sh
gpg --full-generate-key
# choose: key type, size, expire
#   user id[name, pass, comment], passphrase
gpg --list-keys --keyid-format LONG
# list long form pub/priv keys & copy sec/pub key after encryption standard
gpg --armor --export aaa123aaa123
# print gpg key id in ASCII armor format
```

___

## Git Commands & examples

```sh
# Clone the upstream and work on it. Feed changes to upstream.
# <!-- cspell: disable  -->

git clone git://git.kernel.org/pub/scm/.../torvalds/linux-2.6
my2.6
cd my2.6
git switch -c mine master (1)
edit/compile/test; git commit -a -s (2)
git format-patch master (3)
git send-email --to="person <email@example.com>" 00*.patch (4)
git switch master (5)
git pull (6)
git log -p ORIG_HEAD.. arch/i386 include/asm-i386 (7)
git ls-remote --heads http://git.kernel.org/.../jgarzik/libata
-dev.git (8)
git pull git://git.kernel.org/pub/.../jgarzik/libata-dev.git A
LL (9)
git reset --hard ORIG_HEAD (10)
git gc (11)
```
<!-- cspell: enable  -->

1. checkout a new branch mine from master.
2. repeat as needed.
3. extract patches from your branch, relative to master,
4. and email them.
5. return to master, ready to see what’s new
6. git pull fetches from origin by default and merges into the current branch.
7. immediately after pulling, look at the changes done upstream since last time we checked, only in the area we are interested in.
8. check the branch names in an external repository (if not known).
9. fetch from a specific branch ALL from a specific repo & merge
10. revert the pull.
11. garbage collect leftover objects from reverted pull.
<!-- cspell: disable  -->

```sh
# Push into another repository.
# from satellite machine
git clone mothership:frotz frotz (1)
cd frotz
git config --get-regexp '^(remote|branch)\.' (2)
remote.origin.url mothership:frotz
remote.origin.fetch refs/heads/*:refs/remotes/origin/*
branch.master.remote origin
branch.master.merge refs/heads/master
git config remote.origin.push \
  +refs/heads/*:refs/remotes/satellite/* (3)
edit/compile/test/commit
git push origin (4)

# from mothership machine
cd frotz
git switch master
git merge satellite/master (5)
```
<!-- cspell: enable  -->

1. mothership machine has a frotz repository under your home
directory; clone from it to start a repository on the satellite
machine.
1. clone sets these configuration variables by default. It
arranges git pull to fetch and store the branches of mothership
machine to local remotes/origin/* remote-tracking branches.
1. arrange git push to push all local branches to their
corresponding branch of the mothership machine.
1. push will stash all our work away on remotes/satellite/*
remote-tracking branches on the mothership machine. You could use
this as a back-up method. Likewise, you can pretend that
mothership "fetched" from you (useful when access is one sided).
1. on mothership machine, merge the work done on the satellite
machine into the master branch.

## Bash Script Info

```sh
url=$1 # or just use $1 in place where you'd insert the param.
branchname='name'
message=$2
git clone $url # git clone $1; then replace $1 w/ url when calling script
git status # what's changed since last commit
git checkout -b $branch_name
git add . # add all edited files to repo
git commit -m $message || $2
git push -u origin || git push ssh://git@ssh.github.com:443/($uname)/$repo.git
```

- You can do a compare & pull request to see changes that're done
- merge pull requests & del old branch

```sh
# conditionals
if [ "$fname" = "a.txt" ] || [ "$fname" = "c.txt" ]
if [[ "$fname" == "a.txt" || "$fname" == "c.txt" ]]; then
if test "$fname" = "a.txt" || test "$fname" = "c.txt"

#!/bin/bash

for fname in "a.txt" "b.txt" "c.txt"
do
  echo $fname
  if [ "$fname" = "a.txt" ] | [ "$fname" = "c.txt" ]; then
    echo "yes!"
  else
    echo "no!"
  fi
done

for i in {0..22..2}
do
    echo "Loop spin:" $i
done

for file in word_ls.sh num-rng.sh fi_name.sh # for file in *.sh
do
    ls -lh "$file"
done

chmod +x $fname # make fi exe
source || . $fname # exe a script file
```

___

### Bash commands

```sh
echo $BASH # => /usr/bin/bash
init $PATH
., .., ~, $HOME # current working dir, parent dir, home dir of user
ls -a -@ -l
ls -C -l

# remove dir & files
rm -r /folder/want-deleted # remove dir & content recursively
rm -rp # ignore permissions & errors
sudo rm -rf path/to/folder
su - user -c 'ls' # switch user and run cmd
diskutil list
df -h
find / -size +50000 -print
sudo lshw (dmidecode) # lists hardware specs
gcreate (lvcreate | lvextend lvm2 | fdisk)
# create/manage logical pars spanning >= 1 HDD with logical volume manager
whereis (exe | cmd)
whatis <cmdname>
uname -a # show system info
free -gh #show memory usage --lohi -l from /proc/meminfo
service ssh status # check service status
ssh -l username hostname
top -u ib-ub
ps -ef | more # view running processes
ps -ef grep code
kill -9 PID
# killall, pkill, xkill to terminate unix process

ifconfig <interface_name> # (eth0)
# -a (show all details)
ifconfig etho1 (up | down) (enable/disable), muto 1500
ifconfig eth0 192.168.2.2 netmask 255.255.255.0 \
    broadcast 192.168.2.255
# ex. assign IP, netmask and broadcast to interface eth0

netstat -a | more # list all ports
# -at all tcp ports, -au all udp ports
# -s stats, -l (show listening only)
netstat -ap | grep ssh
# info on which port a prog is running on
netstat -an | grep ':80'
# which process is using a specific port

grep -i "word" file.txt # find str in fi
find -iname "file.txt" # find fi
find /home/ib-ub -name *.md -type f

gzip file.md && gzip -d file.md # (zip | unzip) .gz fi
unzip fi.zip && unzip -l fi.zip
# (extract | view) w/o unzipping fi
shutdown -h now #shutdown now or -r to restart now
cat -n /home/ib-ub/flow/work/Docs2/requirements3.txt # print file to stdout
chmod ug+rwx file.txt # change permissions of fi/dir [-R u-rwx ex. will remove access recursively]
chown ib-ub:group_name file.txt # change owner
passwd username # change password; use sudo to reset w/o old pass

useradd -D && useradd login_name # show default options and add user
adduser user_name  # for interactive user creation
newusers file_name
# bulk creation using pre-config template fi
# example
cat homer-family.txt
# homer:HcZ600a9:1008:1000:Homer Simpson:/home/homer:/bin/bash
# marge:1enz733N:1009:1000:Marge Simpson:/home/marge:/bin/csh
man 3 free # bring up section 3 of free cmd
tail -n 10 file.txt # show last 10 lines of fi
less large_file.txt # efficient view of log fi (CTRL+F/B forward/backward 1 window)
diff -w file1.md file2.md # compare fi, ignore whitespace

rsync # sync fi & dir between source & destination dirs
rsnapshot # combo of rsync & hard links to maintain
#   full | incremental backups
dd # make boot images & copy/backup HDDs
    # Copy fi, converting & formatting depending on operands
makeswap && swapon # (add | manage) swap space
dpkg # install/remove deb packages
```

### curl

```sh
curl -o word-test.doc https://file-examples.com/wp-content/uploads/2017/02/file-sample_100kB.doc
curl -o test.png -u demo:password ftp://test.rebex.net/pub/example/KeyGenerator.png --compressed -# # or --progress-bar
redirect the response output to a file, using shell redirect (>), -o, --output
curl --dns-servers 1.1.1.1,1.0.0.1 --compressed -o $file -# $url
# use those dns servers, compress, output to file and use url variable
curl -u name:password --digest https://example.com
# prevents passwd from being sent as cleartext
curl --config file.txt https://example.com # -K file
--rate, -Y, --speed-limit and -y, --speed-time, -6 # use IPv6
# measured in bytes/second, unless suffix is appended, (k, M, G ex. 1k is 1024)

 curl -F '=(;type=multipart/alternative' \
      -F '=plain text message' \
      -F '= <body>HTML message</body>;type=text/html' \
      -F '=)' -F '=@textfile.txt' ...  smtp://example.com
 # --- Example file ---
 url = "example.com"
 output = "curlhere.html"
 user-agent = "superagent/1.0"
 url = "example.com/docs/manpage.html" # fetch another URL too
 -O
 referer = "http://nowhereatall.example.com/"
 # --- End of example file ---

# Data api ex.
 curl --location --request POST 'https://eastus2.azure.data.mongodb-api.com/app/data-pdctr/endpoint/data/v1/action/findOne' \
--header 'Content-Type: application/json' \
--header 'Access-Control-Request-Headers: *' \
--header 'api-key: abc123' \
--data-raw '{
    "collection":"listingsAndReviews",
    "database":"sample_airbnb",
    "dataSource":"Cluster0",
    "projection": {"_id": 1}
}'
```

```py
# MongoDB Data api ex.
import requests
import json
from os import environ
from dotenv import load_dotenv

load_dotenv('../server/.env')

url = "https://eastus2.azure.data.mongodb-api.com/app/data-pdctr/endpoint/data/v1/action/findOne"

payload = json.dumps({
    "collection": "listingsAndReviews",
    "database": "sample_airbnb",
    "dataSource": "Cluster0",
    "projection": {
        "_id": 1
    }
})
headers = {
  'Content-Type': 'application/json',
  'Access-Control-Request-Headers': '*',
  'api-key': os.environ.get('API_KEY'), # || os.getenv('API_KEY')
  'Accept': 'application/ejson'
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)
```

### Bash Scripting

```sh
folder_to_count=$1
# $1, $2...$9 are used as general vars that enable providing parameters when calling the rx

file_count=$(ls $folder_to_count | wc -l)
file_count=$(ls $1 | wc -l) # or use w/o dir var

echo $file_count files in $folder_to_count

chmod +x fi.sh
# must make script fi exe.

./fnct2.sh /dev # run script with a paramater

# env vars
$#: How many command line parameters were passed to the script.
$@: All the command line parameters passed to the script.
$?: The exit status of the last process to run.
$$: The Process ID (PID) of the current script.
$USER: The username of the user executing the script.
$HOSTNAME: The hostname of the computer running the script.
$SECONDS: The number of seconds the script has been running for.
$RANDOM: Returns a random number.
$LINENO: Returns the current line number of the script
```

## Shell command info

- ctrl + \ = Quit (SIGQUIT)
  - fquit a running instance
- open path/to/app.app
  - open an app from sh
- escape special chars:
  - prepending with \
  - wrapping it in single quotes

## Symbolic rep of data

| abbrev | value |
| --- | --- |
| no |  Global default |
|fi  |  Normal file |
|di  |  Directory|
|ln  |  Symbolic link |
|bd  |  Block device|
|cd  |  Character device|
|or  |  Symlink to non-existent fi |
|ex  |  Executable fi |
|*.extension | (ex: *.mp3)|

## Linux permissions

```py
# permission terms
r, w, x = read, write, execute | 4, 2, 1
u, g, o = user, group, others | first, sec., third (chars.)
```

```sh
chmod u+x file.txt
chmod u+r,g+x file.txt
chmod u-rx file.txt # remove permissions
chmod -R 775 dir_name/ # change perm of all fi in dir
chmode -R,a-x,u+X *
# recursively remove exec perm from all fi under
    # dir, then add exec for user
for f in 'ls -R'; do [! -d"$f"] && chmod a-x "$f"; done
# other solution
```

## PowerShell

```ps1
# purge accounts
Import-Csv '.\SP 23 Declines.csv' | foreach {
  $UPN = $_."PPU Email"
  $username = $UPN.Substring(0, $UPN.IndexOf('@'))
  get-aduser $Username | Remove-ADUser
}
```
