#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# %config IPCompleter.use_jedi = False


# # Import Required Libraries

# In[ ]:


import sys
import requests 
from bs4 import BeautifulSoup
import pandas as pd
import os, pathlib
import wget


# ## Input the URL and remove any trailing '/' 

# In[ ]:


# URL = 'https://boards.4channel.org/w/thread/2099866' # Example
URL = sys.argv[1]
while(URL[-1] == '/'):
    URL = URL[:-1]


# ## Retrieve the URL Page

# In[ ]:


r = requests.get(URL) 


# ## Parse to HTML

# In[ ]:


soup = BeautifulSoup(r.content, "html5lib")
# print(soup.prettify())


# ## Traverse HTML tree to get:
# * Thread Title (Dirty Solution)
# * Links to high-res posts

# In[ ]:


thread = soup.find('div', attrs={'class':"thread"})
# print(thread.prettify())


# In[ ]:


titleHTML = thread.find('blockquote')
title = str(titleHTML.contents[0]).replace(" ",'_')
print(title)


# In[ ]:


fileText = thread.findAll('div', attrs={'class':'fileText'})


# In[ ]:


imgList = ["https:"+each.a['href'] for each in fileText]


# In[ ]:


fileList = [each[each.rfind('/')+1:] for each in imgList]


# ## Combine Links and their respective FileNames into a DataFrame

# In[ ]:


df = pd.DataFrame(data=zip(imgList, fileList), columns=["URL","FileName"])
df.head()


# # Create Local Folder Structure

# ```
# ../current_directory  
#     /Scrapper.ipynb
#     /Posts
#         /board 
#             /thread  
#                 /post1.jpg  
#                 /post2.jpg  
#                 /post3.jpg  
#                 .  
#                 .  
#                 .  
# ```

# In[ ]:


def getBoard(url):
    temp = url[:url.rfind('/')]
    end = temp[:temp.rfind('/')]
    start = end[end.rfind('/')+1:]
    return start
def getThread(url):
    return url[url.rfind('/')+1:]


# In[ ]:


rootFolder = os.path.join(os.getcwd(), "Posts")


# ## Create Folders if they don't exist

# In[ ]:


boardFolder = os.path.join(rootFolder, getBoard(URL))
if not os.path.exists(boardFolder):
    os.mkdir(boardFolder)
print(getBoard(URL))


# In[ ]:


threadFolder = os.path.join(boardFolder, getThread(URL))
if not os.path.exists(threadFolder):
    os.mkdir(threadFolder)
print(getThread(URL))


# ## Create a file whose names if the first line of the first post of the thread.  
# ### Often the description.
# ### Name starts with '__' so it's the first file you see when you browse via an explorer.

# In[ ]:


pathlib.Path(os.path.join(threadFolder, ("__"+title))).touch()


# # Files are Downloaded

# In[ ]:


for index, row in df.iterrows():
    filePath = os.path.join(threadFolder, row['FileName'])
    url = row['URL']
    print("Downloading %s to %s"%(url, filePath), end='.')
    wget.download(url ,filePath)
    print(" Downloaded!")

