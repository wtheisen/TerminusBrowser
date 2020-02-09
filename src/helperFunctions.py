import os
import urllib.request

def downloadThreadImages(postList, uvm, folderPath='./Pictures'):
    def downloadImg(imgUrl, path):
        urllib.request.urlretrieve(imgUrl, os.path.join(path, imgUrl.split('/')[-1]))

    def checkCreatePath(path):
        if not os.path.exists(path):
            os.makedirs(path)

    checkCreatePath(folderPath)
    i = 0
    # imgList = [p for p in postList if p.image != '']
    for p in postList:
        uvm.currFocusView.frame.footerStringRight = f'{i} images downloaded...'
        if p.image != '': 
            downloadImg(p.image, folderPath)
            i += 1
            uvm.buildAddFooterView(uvm.currFocusView)
            uvm.renderScreen()
    
