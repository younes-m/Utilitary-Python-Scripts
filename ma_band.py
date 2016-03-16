from urllib.request import Request, urlopen
from urllib.error import HTTPError
from bs4 import BeautifulSoup

class Main:
    def __init__(self, input='behemoth'):
        self.choices = None      
        
        self.band = input.lower().replace(' ', '_')
        self.url = u'http://www.metal-archives.com/bands/{0}'.format(self.band)
        
        self.request = Request(self.url)
        
        try:
            self.source = urlopen(self.request)
        except HTTPError:
            print("band not found")
            return
       
        
        self.soup = BeautifulSoup(self.source, 'html.parser')

        
        try :
            self.find_id()

        except TypeError :
            print('More than 1 band, taking the first\n')
            self.url = self.find_url()
            self.request = Request(self.url)
            self.source = urlopen(self.request)
            self.soup = BeautifulSoup(self.source, 'html.parser')
            self.choices = 'ahquecoucou'

            
        
        self.lefttable = self.soup.find('dl', "float_left")
        self.righttable = self.soup.find('dl', "float_right")
        
        #print(self.righttable)
        
        self.table_array = []
        self.put_soup_in_array(self.lefttable, self.table_array)
        self.put_soup_in_array(self.righttable, self.table_array)
        
        self.bandinfo = {}
        self.bandinfo['ID'] = self.find_id()
        self.bandinfo['Band name'] = self.soup.find('h1').contents[0].contents[0]
        for i in range(1, len(self.table_array), 2):
            try :
                self.bandinfo[self.table_array[i - 1].replace(':', '')] = self.table_array[i].contents[0]
            except AttributeError:
                self.bandinfo[self.table_array[i - 1].replace(':', '')] = self.table_array[i] 

        
        print(""\
            "{Band name}\n"\
            "\n"\
            "{Country of origin} ({Location})\n"\
            "Formed in {Formed in}\n"\
            "{Genre}\n"\
            "Status : {Status}\n"\
            "Lyrical themes : {Lyrical themes}"\
            .format(**self.bandinfo).encode('CP850', 'replace').decode('CP850', 'ignore'))
        try :
            print("Last label : {Last label}\n".format(**self.bandinfo))
        except KeyError:
            print("Current label : {Current label}\n".format(**self.bandinfo))
            
        self.get_albums()
        self.maxsize_album()
        
        print('Full-Lengthes :')
        if len(self.albums) > 1 :
            for element in reversed(self.albums) :
                print('{0}: {1}.- {2}'.format(element[2], self.maxed(element[0], self.maxsize_album), element[3]).encode('CP850', 'replace').decode('CP850', 'ignore'))
        else :
            print('No album found')
        
        
        
        if self.choices == 'ahquecoucou' :
            self.choicesf(self.bandschoice)
        else :
            self.choices = None
       
        
        
    def find_id(self):
        self.completeurl = self.soup.find('h1').contents[0]['href']
        return self.completeurl.split('/')[-1]
    
    def find_url(self):
            self.bandschoice = self.soup
            for element in self.soup.find_all('a'):
                if '<a href="http://www.metal-archives.com/bands/{0}'.format(self.band) in str(element).lower() :
                    return element['href']
            print('Rien trouvé !')
            return
  
    def put_soup_in_array(self, source, array):
        for line in source:
            if line != '\n':
               array.append(line.contents[0])
        return (array)
    
    def get_albums(self):
        self.albums = []
    
        self.albumsurl = u'http://www.metal-archives.com/band/discography/id/{0}/tab/main'.format(self.bandinfo['ID'])
        self.albumssoup = BeautifulSoup(urlopen(self.albumsurl), 'html.parser')
        
        i = 0
        for element in self.albumssoup.find_all('td'):
            #title
            if i == 0:
                self.albums.append(element.contents[0].contents)
                i += 1
            #full lenght
            elif i == 1:
                self.albums[-1].append(element.contents[0])
                i += 1
            #release date
            elif i == 2:
                self.albums[-1].append(element.contents[0])
                i += 1
            #reviews number
            elif i == 3:
                try :
                    self.reviews = element.find('a').contents[0].split(' ')
                    self.albums[-1].append(self.reviews[-1].replace('(', '').replace(')', '') + ' ({0} reviews)'.format(self.reviews[-2]))
                except AttributeError :
                    self.albums[-1].append('No review yet')
                i = 0
        
        return self.albums

    def maxsize_album(self):
        self.maxsize_album = 0
        for element in self.albums :
            if self.maxsize_album < len(element[0]):
                self.maxsize_album = len(element[0])
     
    def maxed(self, element, maxsize):
        while len(element) < maxsize:
            element = element + '.'
        return element
        
    def choicesf(self, source):
        self.choices = {}
        i = 1
        for element in source.find_all('a') :
            if '<a href="http://www.metal-archives.com/bands/{0}'.format(self.band) in str(element).lower() :
                #{key i : band name, url}
                self.choices[i] = [element.contents[0], element['href']]
                i+=1
        
        i = 1
        #adding the genre
        for element in source.find_all('strong') :
            self.choices[i].append(element.contents[0])
            i += 1
        return self.choices
 
def second_run(input1):
    newchoice = 'a'
    while newchoice.lower() != 'q' :
        print('\n')
        if input1.choices != None:
            print('Wrong band ? Enter the index of another one. You can also make a new search or press q to quit\n')
            for element in input1.choices :
                print('{0} : {1} ({2})'.format(str(element), str(input1.choices[element][0]), str(input1.choices[element][2])))

            newchoice = input('\n> ')
        else :
            newchoice = input('Make a new search or press q to quit\n> ')
        
        try :
            if int(newchoice) in input1.choices :
                newband = input1.choices[int(newchoice)][1].split('/')
                newband = '/'.join([newband[-2], newband[-1]])
                input1 = Main(newband)
        except ValueError :
            if newchoice.lower() != 'q' :
                input1 = Main(newchoice)
 
if __name__ == '__main__':
    band = input('enter a band name\n> ')
    print('\n')
    input1 = Main(band)
    second_run(input1)
    