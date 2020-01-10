class Status:

    def __init__(self, status_id, title, created_at, media=None):
        self.status_id = status_id
        self.title = title
        self.created_at = created_at
        self.media = media

    def __str__(self):
        return 'Status_id: {0}, Title: {1}, Created At: {2}, Media:{3}'.format(self.status_id, self.title,
                                                                                self.created_at, 1 if self.media else 0)

    def get_status_info(self):
        return self.__dict__