from crawler import Crawler

if __name__ == '__main__':

    consume_key = 'YOUR CONSUME KEY'
    consume_key_secret = 'YOUR CONSUME KEY SECRET'
    access_token = 'YOUR ACCESS TOKEN KEY'
    access_token_secret = 'YOUR ACCESS TOKEN KEY SECRET'

    crawler = Crawler(consumer_key=consume_key,
                      consumer_key_secret=consume_key_secret,
                      access_token_key=access_token,
                      access_token_key_secret=access_token_secret)

    list_friend_info = crawler.get_list_friends()

    friend_to_craw_name = ['yuukamiya68','inanakisiki','7subaru_anime','taka8rie']

    for name in friend_to_craw_name:
        for info in list_friend_info:
            if name == info['screen_name']:
                crawler.download_resources_from_friend(friend_id=info['friend_id'],max_status=30,name=name)
