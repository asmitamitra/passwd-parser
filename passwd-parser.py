import json
class UserData:
    def __init__(self, uname, uid):
        self.fullname = uname
        self.uid = uid
        self.groups = []

    def set_group(self, groupname):
        self.groups.append(groupname)


def parser(passwdfile, groupsfile):
    list_of_users = {}
    is_read_successful = True

    try:
        # reading passwdFile
        with open(passwdfile) as fp:
            line = fp.readline()
            while line:
                entry = line.split(":")
                if entry.__len__() != 7:
                    print("Invalid entry format for /etc/passwd file")
                if entry[0] not in list_of_users:
                    # list_of_users: dict { "username": Class of UserData<full_name, groupsList>}
                    list_of_users[entry[0]] = UserData(entry[4], entry[2])
                else:
                    continue
                line = fp.readline()
            fp.close()
        # print(list_of_users)
    except FileNotFoundError:
        print("Wrong file or file path for etc/passwd")
        is_read_successful = False

    try:
        # reading groupsFile
        with open(groupsfile) as fp:
            line = fp.readline()
            while line:
                entry = line.split(":")
                groupName = entry[0]
                groupList = entry[-1].rstrip()
                groupList = groupList.split(",")
                # for each username in groupList, append corresponding group name to the user
                for uname in groupList:
                    if uname in list_of_users:
                        list_of_users[uname].set_group(groupName)
                    else:
                        continue
                line = fp.readline()
            fp.close()
        # print(list_of_users)
    except FileNotFoundError:
        print("Wrong file or file path for etc/groups")
        is_read_successful = False

    # if read both file successfully then make into JSON format
    if is_read_successful:
        # print data in JSON format
        data = {}
        for user in list_of_users:
            data[user] = {"uid": "0", "full_name": "", "groups": []}
            data[user]["uid"] = list_of_users[user].uid
            data[user]["full_name"] = list_of_users[user].fullname
            data[user]["groups"] = list_of_users[user].groups
        print(json.dumps(data, indent=4))

    else:
        print("Reading /etc/passwd or /etc/groups was not successful.")


if __name__ == "__main__":

    # For this sample case, pass the default filenames:
    passwdFileName = "./etc_passwd.txt"
    groupsFileName = "./etc_groups.txt"

    # can also take input from user for the path to /etc/passwd & /etc/groups file
    # passwdFileName = input("Enter path/filename for /etc/passwd")
    # groupsFileName = input("Enter path/filename for /etc/groups")

    # while running a cron job, the parser function should be called periodically and #
    # each time pass the path/filename for /etc/passwd and /etc/groups #
    parser(passwdFileName, groupsFileName)