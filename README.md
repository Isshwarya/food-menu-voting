# food-menu-voting

An application that provides APIs for the employers of a company to vote for their favorite menu from different food chains.

About

Company needs internal service for its’ employees which helps them to make a decision
on lunch place.

Each restaurant will be uploading menus using the system every day over API
Employees will vote for menu before leaving for lunch on mobile app for whom backend has to be implemented
There are users which did not update app to the latest version and backend has to support both versions.
Mobile app always sends build version in headers.

Needed API’s:

o Authentication
o Creating restaurant
o Uploading menu for restaurant (There should be a menu for each day)
o Creating employee
o Getting current day menu
o Voting for restaurant menu (Old version api accepted one menu, New one accepts top three menus with respective points (1 to 3)
o Getting results for current day

Requirements:

Solution should be built using Python and preferably Django Rest Framework, but any other framework works
App should be containerised
Project and API Documentation
• Tests

Extra points
HA Cloud Architecture Schema/Diagram (Preferably Azure)
Usage of Linting and Static typing tools
