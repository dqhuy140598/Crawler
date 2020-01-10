import twitter
from friend import Friend
from status import Status
from requests import get
from tqdm import tqdm
import os


class Crawler:

    def __init__(self, consumer_key, consumer_key_secret, access_token_key, access_token_key_secret):
        self.consumer_key = consumer_key
        self.consumer_key_secret = consumer_key_secret
        self.access_token_key = access_token_key
        self.access_token_key_secret = access_token_key_secret
        self.api = twitter.Api(consumer_key=self.consumer_key,
                               consumer_secret=self.consumer_key_secret,
                               access_token_key=access_token_key,
                               access_token_secret=self.access_token_key_secret)
        self.friends = []

    def __str__(self):
        profile = self.api.VerifyCredentials().AsDict()
        return 'Name : {0}, ID_str: {1}, Screen_name: {2}, Friend_count:{3} '.format(profile['name'],
                                                                                     profile['id_str'],
                                                                                     profile['screen_name'],
                                                                                     profile['friends_count'])

    def get_list_friends(self):
        list_raw_data = self.api.GetFriends()
        for info in list_raw_data:
            info_dict = info.AsDict()
            friend = Friend(friend_id=info_dict['id_str'], name=info_dict['name'], screen_name=info_dict['screen_name'])
            self.friends.append(friend)

        list_info = [friend.get_friend_info() for friend in self.friends]
        # for info in list_info:
        #     print(info)
        return list_info

    def get_friend_time_line(self, friend_id, max_status=30):
        if len(self.friends) == 0:
            self.get_list_friends()
        friend = [x for x in self.friends if x.get_friend_info()['friend_id'] == friend_id][0]
        if friend is None:
            raise Exception('Your Friend ID not exists')

        list_status = self.api.GetUserTimeline(user_id=friend_id, count=max_status)
        for i, info in enumerate(list_status):

            info_dict = info.AsDict()

            if 'media' in list(info_dict.keys()):
                status = Status(status_id=info_dict['id_str'],
                                title=info_dict['text'],
                                created_at=info_dict['created_at'],
                                media=info_dict['media'])
            else:
                status = Status(status_id=info_dict['id_str'],
                                title=info_dict['text'],
                                created_at=info_dict['created_at'], )

            friend.add_status(status)

        return friend.get_all_status()

    def download_image_from_friend_status(self, status, image_out_path):
        image_url = status['media'][0]['media_url_https']
        req = get(image_url)
        with open(image_out_path, 'wb') as file:
            for i in tqdm(range(10000)):
                pass
            file.write(req.content)

    def download_resources_from_friend(self, friend_id, max_status, name=None):
        friend_statues = self.get_friend_time_line(friend_id, max_status=max_status)
        count = 0
        if name is not None:
            resource_directory = os.path.join('images', name)
        else:
            resource_directory = os.path.join('images', friend_id)
        if not os.path.exists(resource_directory):
            os.mkdir(resource_directory)
        for status in friend_statues:
            status_info = status.get_status_info()
            if status_info['media'] is not None:
                image_name = str(count + 1) + '.png'
                image_path = os.path.join(resource_directory, image_name)
                self.download_image_from_friend_status(status_info, image_out_path=image_path)
                count += 1
        print('Done !!')

    def post_status(self, title, media):
        self.api.PostUpdate(status=title, media=media)
        print('Done Post Status !')

    def post_newest_status_from_friend(self,friend_id):
        friend_statues = self.get_friend_time_line(friend_id)
        for status in friend_statues:
            status_info = status.get_status_info()
            if status_info['media'] is not None:
                title = status_info['title']
                media = status_info['media'][0]['media_url_https']
                self.post_status(title,media)
                break
