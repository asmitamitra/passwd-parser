import json
class UserData:
    def __init__(self, uname, uid):
        self.fullname = uname
        self.uid = uid
        self.groups = []

    def set_group(self, gname):
        self.groups.append(gname)


if __name__ == "__main__":
    list_of_users = {}
    isReadSuccessful = True
    try:
        with open("etc_passwd.txt") as fp:
            line = fp.readline()
            while line:
                entry = line.split(":")
                if entry.__len__() != 7:
                    print("Invalid entry format for /etc/passwd file")
                if entry[0] not in list_of_users:
                    list_of_users[entry[0]] = UserData(entry[4], entry[2])
                else:
                    continue
                line = fp.readline()
            fp.close()
        # print(list_of_users)
    except FileNotFoundError:
        print("Wrong file or file path")
        isReadSuccessful = False
    try:
        with open("etc_groups.txt") as fp:
            line = fp.readline()
            while line:
                entry = line.split(":")
                groupName = entry[0]
                groupList = entry[-1].rstrip()
                groupList = groupList.split(",")
                for uname in groupList:
                    if uname in list_of_users:
                        list_of_users[uname].set_group(groupName)
                    else:
                        continue
                line = fp.readline()
            fp.close()
        print(list_of_users)
    except FileNotFoundError:
        print("Wrong file or file path")
        isReadSuccessful = False
    if isReadSuccessful:
        with open("output.txt", "w") as fp:
            data = {}
            for user in list_of_users:
                data[user] = {"uid": "0", "full_name": "", "groups": []}
                data[user]["uid"] = list_of_users[user].uid
                data[user]["full_name"] = list_of_users[user].fullname
                data[user]["groups"] = list_of_users[user].groups
            json.dump(data, fp, indent=4)
            fp.close()
    else:
        with open("output.txt", "w") as fp:
            fp.write("Wrong file or wrong file path was entered. Reading /etc/passwd or /etc/groups was not successful.")
            fp.close()