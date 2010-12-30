import abc
from requests import AuthRequest,ArtistRequest,UserRequest,Request
import authinfo
import errors

class IWSData(object):

    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def URL(self):
        pass

    @abc.abstractmethod
    def authInfo(self):
        pass

    @abc.abstractmethod
    def mobileSession(self):
        pass

class LastFMClient(IWSData):
    def __init__(self, URL, authInfo):
        super(LastFMClient, self).__init__()
        self._URL = URL
        self._authInfo =  authInfo
        self._sk=None #mobileSession result

    @property
    def URL(self):
        return self._URL

    @property
    def authInfo(self):
        return self._authInfo

    @property
    def mobileSession(self):
        if self._sk is None:
            self._sk=AuthRequest(self,Request.GET_TYPE).getMobileSession()
        return self._sk

    @property
    def token(self):
        return AuthRequest(self,Request.GET_TYPE).getToken()

    def shout(self,user,message):
        return UserRequest(self,Request.POST_TYPE).shout(user,message)

    def addTags(self,artist,tags):
        return ArtistRequest(self,Request.POST_TYPE).addTags(artist,tags)

    def removeTag(self,artist,tag):
        return ArtistRequest(self,Request.POST_TYPE).removeTag(artist,tag)

    def getCorrection(self,artist):
        return ArtistRequest(self,Request.GET_TYPE).getCorrection(artist)

    def getArtistShouts(self,artist,limit=50,autocorrect=0,page=None):
        return ArtistRequest(self,Request.GET_TYPE).getShouts(artist,limit,autocorrect,page)

    def getArtistSimilar(self,artist,autocorrect=0):
        return ArtistRequest(self,Request.GET_TYPE).getSimilar(artist,autocorrect)

    def getArtistTags(self,artist,autocorrect=0):
        return ArtistRequest(self,Request.POST_TYPE).getTags(artist,autocorrect)

if __name__=="__main__":

    URL="ws.audioscrobbler.com"

    api_key=raw_input("Please enter your api_key: ")
    secret=raw_input("Please enter your secret: ")
    username=raw_input("Please enter your username: ")
    userpass=raw_input("Please enter your userpass: ")

    try:
        client = LastFMClient(URL,authinfo.AuthInfoType(api_key, secret, username, userpass))

        print "invocation client.token: ", client.token
        print "invocation client.mobileSession: ", client.mobileSession
        print "invocation client.shout: ", client.shout("varnie","this is a test")

        tags = ['m','e','t','a','l','l']
        print "client.addTags invocation", client.addTags("Behemoth",tags)
     
        print "client.getArtistTags invocation", client.getArtistTags("Behemoth")
        print "client.removeTag invocation"
        for tag in tags:
            print client.removeTag("Behemoth",tag)

        print "client.getCorrection invocation", client.getCorrection("Guns N")
        print "client.getArtistShouts invocation", client.getArtistShouts("Behemoth")
        print "client.getArtistSimilar invocation", client.getArtistSimilar("Behemoth")
    
    except errors.Error, e:
        print e


