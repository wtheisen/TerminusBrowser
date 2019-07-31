class Post():
    def __init__(self, userIden, content, timestamp, image=None, score='0', replies=None):
        self.userIden = userIden
        self.content = content
        self.timestamp = timestamp
        self.image = image
        self.score = score
        self.replies = [] if not replies else replies
