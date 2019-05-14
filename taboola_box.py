class TaboolaBox(object):
    def __init__(self, title, sponsor, link, source_webpage): #webpage, image_url):
        self.title = title
        self.sponsor = sponsor
        self.link = link
        self.source_webpage = source_webpage

    def write(self, publisher):
        data = (publisher, hash(self.title))
        filename = 'data/%s/%d.txt' % data
        with open(filename, 'w+') as file:
            file.write('%s\n' % self.title)
            file.write('%s\n' % self.sponsor)
            file.write('%s\n' % self.link)
            file.write('%s\n' % self.source_webpage)

    @staticmethod
    def load(filename):
        with open(filename, 'r') as file:
            lines = file.readlines()
            title = lines[0].strip()
            sponsor = lines[1].strip()
            link = lines[2].strip()
            source_webpage = lines[3].strip()

            return TaboolaBox(title, sponsor, link, source_webpage)
