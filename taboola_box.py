class TaboolaBox(object):
    def __init__(self, title, sponsor, publisher):
        self.title = title
        self.sponsor = sponsor
        self.publisher = publisher
        self.image_url = image_url

    def write(self):
        data = (self.publisher, self.title)
        filename = '%s/%s.txt' % data
        with open(filename, 'w') as file:
            file.write('%s\n' % self.title)
            file.write('%s\n' % self.sponsor)
            file.write('%s\n' % self.publisher)

    def load(filename):
        title = ''
        sponsor = ''
        publisher = ''
        image_url = ''
        
        with open(filename, 'r') as file:
            file.readlines()
            title = file[0]
            sponsor = file[1]
            publisher = file[2]
            image_url = file[3]

        return TaboolaBox(title, sponsor, website, image_url)
