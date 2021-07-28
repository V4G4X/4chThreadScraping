# 4chan Post Scrapper
Run
```[python]
python Scraper.py <4chan thread link>
```
to download all posts in a thread at OG Format.

## Link Format expected:
```https://boards.4channel.org/<board_name>/thread/<thread_ID>```

## Output Folder Structure(Posts):
```
../current_directory  
    /Scrapper.ipynb
    /Posts
        /board(abbreviation) 
            /thread(ID)
                /__Thread_Description
                /post1
                /post2  
                /post3  
                .  
                .  
                .  
```

## Required python Libraries:
* sys
* requests
* bs4 
* pandas 
* os
* pathlib
* wget

### Run:
```pip install -r requirements.txt```
