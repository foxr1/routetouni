# RoutetoUni

RoutetoUni is a web-based application that is designed to help first year
students studying at Newcastle University.

---
### Functionality
The application supports different pages that would to relate to questions a typical first year
student would ask. The pages include Societies, Accommodation, Pubs & Clubs, Revision, News, Health, 
Campus Map and Chat.
Along with individual pages showing information there is
a trained bot that will answer any questions a user would have. The Societies, Accommodation
, Pubs & Clubs, Revision and Health pages display information on flipcards. The Chat redirects to
 the chatrooms and the Campus redirects to a map of Newcastle with points of interest marked.
A user can create an account and join a chatroom in which they will be randomly assigned with
other first year students, a maximum of 10 people can join each chatroom. If a student is a peer
 mentor he/she is able to join different a chatroom. 

---
### Running RouteToUni locally
To run RouteToUni locally you will need to download the required plugins that are shown in
requirements.txt. The commands below are to be ran in your terminal whilst in the directory of
routetouni.

`pip install -r requirments.txt`

followed by 

`docker compose up`

finally run the main.py file and the website will be deployed on http://localhost:5000/.

---
### Viewing the website online
If you do not want to run RouteToUni locally you are able to view the website at 
[RouteToUni](https://routetouni.me)
online.