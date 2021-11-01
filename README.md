# Data Set Documentation
## comments\_0101\_0831.csv
This file contains relevant information on all the comments from Jan 1 to Aug 31 on PTT Gossiping Board
- post\_id: the ID of the post that the comment is under
- content: the comment
- datetime: the date and time at which the comment was posted
- user: the ID of the user who posted the comment
## comments\_0501\_0831.csv
This file contains relevant information on the comments that are under events from May 1 to Aug 31 on PTT Gossiping Board
- post\_id: the ID of the post that the comment is under
- event\_id: the ID of the event that the comment is under
- content: the comment
- datetime: the date and time at which the comment was posted
- user: the ID of the user who posted the comment
- sentiment\_score: the score that measures a reader's perception on how positive or negative the comment may appear. 0 indicates a negative perception; 0.5 indicates a neutral perception and 1 indicates a positive perception
- incite\_score: the score that indicates how likely the comment is to provoke an emotional response from a reader. The higher the score, the more likely the comment will provoke an emotional response from a reader
## event\_info\_0501\_0831.csv
This file contains relevant information on all the events from May 1 to Aug 31 on PTT Gossiping Board
- event\_id: the ID of the event
- event\_title: the name of the event
- islander\_url: the url of the event on [Islander]
- num\_ptt\_article: the number of PTT posts under the event
- num\_ptt\_comments: the number of PTT comments under the event
- label: the category the event falls under
## final\_user\_groups\_0501\_0831.csv
This file contains relevant information on the user groups using data collected from May 1 to Aug 31 on PTT Gossiping Board
- user\_group: the ID of the user group
- user: the ID of user associated with the group
## posts\_0501\_0831.csv
This file contains relevant information on the posts that are under events from May 1 to Aug 31 on PTT Gossiping Board
- post\_id: the ID of the post
- post\_date: the date and time at which the post was posted
- content: detailed information on the post
- author: the ID of the user who posted the post
- event\_id: the ID of the event that the post is under
- ip: the IP address of the user that posted the post
- board: the board at which the post was posted
## share\_ip\_users\_under\_1\_hr\_with\_min\_diff\_0501\_0831.csv
This file contains relevant information on the users that shared IP addresses within 1 hour from May 1 to Aug 31 on PTT Gossiping Board
- user\_1: the ID of the user who shared IP address with user\_2
- user\_2: the ID of the user who shared IP address with user\_1
- min\_diff: the minute difference between the comments posted by the two users that shared IP address
## users\_events\_relationship\_0501\_0831.csv
This file contains information on user patterns under events from May 1 to August 31 on PTT Gossiping Board
- user: the ID of the user who participated in the event
- event\_id: the ID of the event
- event\_participation\_rate\_by\_comments: the number of comments the user posted under the event divided by the total number of comments under the event
- event\_participation\_rate\_by\_post: the number of posts the user posted under the event divided by the total number of posts under the event
- top\_10\_commenter\_rate: the number of comments that are among the first 10 under each post in the event posted by the user divided by the total number of posts * 10 under the event
- comment\_repeatedly\_under\_same\_posts\_rate: the number of times the user commented more than once under each post in the event divided by the total number of posts under the event
- commented\_with\_slogan\_rate: the number of times the user comments contained slogan under each post in the event divided by the total number of posts under the event
## users\_grouped\_by\_high\_phi\_coef\_0501\_0831.csv
This file contains relevant information on the user groups considering only phi coefficient from May 1 to Aug 31 on PTT Gossiping Board
- user\_group: the ID of the user group
- user: the ID of the user associated with the group
## users\_with\_at\_least\_10\_comments\_0501\_0831.csv
This file contains user IDs who posted at least 10 comments from May 1 to Aug 31
- user: the user ID
## vpn\_users\_0501\_0831.csv
This file contains relevant information on the users that used VPN from May 1 to Aug 31
- user: the ID of the user who used VPN
- vpn: the VPN the user used

## Reference

[Islander]: <https://islander.cc/>