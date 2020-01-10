

class Friend:

    def __init__(self,friend_id,name,screen_name):
        self.friend_id = friend_id
        self.name = name
        self.screen_name = screen_name
        self.list_status = []

    def __str__(self):
        return "id: {0}, screen_name: {1}".format(self.friend_id,self.screen_name)

    def add_status(self,status):
        self.list_status.append(status)

    def get_all_status(self):
        return self.list_status

    def get_friend_info(self):
        return self.__dict__