import os
import urllib.request

def downloadThreadImages(postList, folderPath='./Pictures'):
    def downloadImg(imgUrl, path):
        urllib.request.urlretrieve(imgUrl, os.path.join(path, imgUrl.split('/')[-1]))

    def checkCreatePath(path):
        if not os.path.exists(path):
            os.makedirs(path)

    checkCreatePath(folderPath)
    for p in postList:
        if p.image != '': 
            downloadImg(p.image, folderPath)
    
