import datetime

class Weibo:
    def __init__(self):
        self.id = 'default'
        self.content = ''
        self.time = datetime.datetime.now()
        self.isreposst = False
        self.repostreason = ''