class Post():
    def __init__(self, userIden, content, timestamp, image=None):
        self.userIden = userIden
        self.content = content
        self.timestamp = timestamp
        self.image = image
        self.replies = []