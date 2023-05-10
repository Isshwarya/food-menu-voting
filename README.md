# food-menu-voting

An application that provides APIs for the employers of a company to vote for their favorite menu from different food chains.

## Assignment details

### About

Company needs internal service for its’ employees which helps them to make a decision
on lunch place.

Each restaurant will be uploading menus using the system every day over API
Employees will vote for menu before leaving for lunch on mobile app for whom backend has to be implemented
There are users which did not update app to the latest version and backend has to support both versions.
Mobile app always sends build version in headers.

### Needed API’s:

o Authentication
o Creating restaurant
o Uploading menu for restaurant (There should be a menu for each day)
o Creating employee
o Getting current day menu
o Voting for restaurant menu (Old version api accepted one menu, New one accepts top three menus with respective points (1 to 3)
o Getting results for current day

### Requirements:

Solution should be built using Python and preferably Django Rest Framework, but any other framework works
App should be containerised
Project and API Documentation
• Tests

### Extra points

HA Cloud Architecture Schema/Diagram (Preferably Azure)
Usage of Linting and Static typing tools

## Solution details

### Assumptions and TODOs

- For authentication, JWT system is used for its token expiry features and its popularity in mobile environments. The token expiry time can be adjusted in settings.py based on product requirements.

- For selecting top 3 menu's, it's not stated how to perform the selection approach. So the assumed approach is: top three menus are selected based on the menus getting highest no.of votes across any preference_score. This leaves us with the case where a menu getting high no.of votes for preference_score:3 could emerge as the top most finalist. Instead, we could do a weighted score and select top 3 menus based on total score (preference score=1 could be given 5 points, preference score=2 could be given 3 points, preference score=3 could be given 2 points) instead of merely going by counts of votes. This can be improved later based on product requirments.

- Add the ability for the user to change his/her menu preference later. Let's say if the user has voted for Restaurant "Rest1"'s menu as the top most preference and later the user wants to change it to "Rest2". Currently, once voted, we don't allow overrides. This can be decided based on product requirements.
