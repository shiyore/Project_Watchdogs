# Project_Watchdogs

## **Warnings**

This is the intellectual property of Aiden Yoshioka without any copyrights or trademarks. I'm fine with the free use of my project, but I would apprectiate any recognition I can get.
 
In addition to that, I am not responsible for the actions of any individual that uses the code from my project. This project is meant to be a proof of concept of a mobile hacking platform built on a raspberry pi, and is strictly meant for educational purposes.


---


## **Introduction**


My project was both inspired heavily by media and was built to solve an issue I, and a company I used to work for, encountered.  

First, the problem.  When working at Resurgence IT, it became apparent that lower level IT technicians don't have a large amount of experience working with offensive security skills. This requires them to have to hire a new specialized employee in order to test their clients, or outsource their penetration testing. Both of which cost a whole lot of money. My project, as of now, aims to make a cheap and easy to use tool that would allow users to perform some basic (hopefully advanced down the line) tests/hacks on a client's network. I planned to do this by using a raspberry pi 3 and a wireless card with monitor mode (which don't cost more than $30-$40 together), and would house a very easy to use UI that would allow users to scan and disrupt a networks (to start with) with just a couple buttons.

As for my inspiration. I was heavily inspired by one of my favorit game franchises, [watchdogs](https://www.ubisoft.com/en-us/game/watch-dogs/watch-dogs-2).  In these games, hackers are able to control cars, overload batteries, disrupt networks, cause blackouts, and a ton of other hacks using nothing more than their phone. In the real world, this isn't really possible without having a suspicious antenna hanging off your phone, but it's not impossible to access something on your phone. Watchdogs inspired the ease of use for my project. The ultimate goal will be to minimize the amount of input the user needs in order to make hacking a network be nothing more than pressing a button. I tried my best to make my UI minimalistic, but I would like to reduce my UI in another version or by creating a settings page in the near future.

---


## **Features and Requirements**

A more in-depth detail of all my functional features and requirements can be found in my [user stories document](https://docs.google.com/spreadsheets/d/19BBOpORVL5XS-3QDqhetDGyS-B04Luq9_laX4_Vq1-s/edit?usp=sharing)

My non-functional requirement was responsiveness. I wanted my project to be quick and snappy when being used, so speed and optimization were at the top of my mind when coding my features.  I accomplished this by switching to a lighter weight database, using my own scripts instead of open source tools, and utilizing asyncronized methods when I could. Overall, I think I did a good job making sure my site had a quick response time (except the scan at times).

As for functional requirements, I only had a couple major things I wanted to accomplish:
  - Have a home page that outlines my project
  - Make sure each page has a more detailed description at the top
  - Have a page to view all previously scanned devices
  - Have a page to jam and deauth a network with just a single button
  - Have a page to scan for nearby networks with just a single button
  - Store all data on a persistent database
  - Have the project aimed to run on a headless raspberry pi (everything starts on boot)

---

## **Technology Choices & Practices**

My choices were mainly based on what I would need the least amount of installation on a raspberry pi, so most of my choices had to be light weight. I also wanted to get more  experience using python because a large portion of hacking tools are built in python. I tried my best to follow pep8's python best practices, and the MVC design pattern in flask.  Below is a table of my techonologies:

|   Technology    |    Purpose   |   Reasoning    |
|   :---          |    :---:     |   :--         |
|   Python    |    Main Coding Language   |   I wanted more practice with a scripting language.    |
|   Flask    |    Web Dev Framework   |   Flask is a web development framework built on pythong, so it would be perfect when working with my scripts.    |
|   SQLite    |    Database   |   Light Weight and small for the purpose of my project. It also doesn't require any setup beyond a file in the same directory as the flask directory. And I've never used it before.    |
|   Flask server   |    Web Server   |   I would normally use an apache server, but I decided to challenge myself by trying something different that may be more of a challenge to setup to run on a headless pi.     |
|   Scapy    |    Packet interception and crafting   |   Scapy is used by programmers to manage wireless capabilities like sniffing and crafting packets.    |
|   Raspberry Pi    |    Project Housing   |   My project can't be run on a phone, so having a raspberry pi hosting a site would be the easiest way to access the tools on a phone.    |
|   Kali Linux    |    Operating System   |   Kali linux has a lot of built in tools that I can implement later down the line, and comes with some default packages that I use.    |
|   SQLAlchemy   |    Database Management   |   The only module I could find that was built to manage databases with flask.     |
>### Devops principles
>As my project isn't on the cloud, I did my best to try and implement CD\CI although it's not really possible. If the user wants to make any changes to the project, they can edit the site within the flask directory, and all changes will take place upon restart. As for any changes I make, they can also be updated fairly easily. All the user needs to do is navigate to the project directory and use "git pull" and all changes will take place upon restart.
>
>I would have liked to implement some sort of logging framework, but I encountered too many issues within the limited amount of time I had.  Sometime soon, I will implement a logging system
>

---

## **Technical Approach/Choices**

My technical approach was all centered around running everything on a fresh kali raspberry pi. I needed to make a raspberry pi that hosted a mobile centric site that I could access easily.  Most of my scripting would be done in python. Therefore, using flask would make it easy to utilize those same scripts. Below are some of my key technical diagrams.

Let's start with my **sitemap**. I had to create 2 other difficult scripts and learn a bunch of new technologies, so my site was farely simple.
![sitemap](https://a2-images.myspacecdn.com/images04/7/49ade93a9e9a49ed897403d822e5461e/full.jpg)

Here are my **wireframes**. Their designs represent what my actual site looks like. However, my tables are missing 1 column each due to an error with flask not letting me use the buttons if I have too many columns.
![Wireframes](https://a4-images.myspacecdn.com/images04/4/870628497a0249a288ecee3da9d8a064/full.jpg)

Because python/flask isn't object oriented in the conventional means, I didn't really have any classes.  Because of that, and my choice to use SQLite, my **UML** and **ER Diagram** are essentially the same thing because they exist to interact with my database using SQLAlchemy. 
![UML/ER Diagram](https://a4-images.myspacecdn.com/images04/11/31e3ec484a7041939df993a43d12cff3/full.jpg)

Last of my important diagrams is my **physical architecture** diagram. This lays out the physical technology I used and how they interact with my software.  As you can see, my project is relatively simple and is mainly just a web server on a raspberry pi.
![Physical Architecture](https://a4-images.myspacecdn.com/images04/3/7464d10a8bf741f7a6b4d4842960d343/full.jpg)

More of my diagrams can be found in my [lucidchart for my project](https://lucid.app/lucidchart/invitations/accept/cf606fbc-7325-4228-8e61-d5cca7a2093f).

---

## **Risks & Challenges**

My biggest risks ranked:
  1.Learning at least 4 new technologies at the same time
  2.Using a raspbery pi for the first time
  3.Centering my entire project around an idea that I liked, but didn't really have experience working with. I've programmed small scripts, but nothing as indepth as what I had to do for this
  4.Deciding to make an install script when I have no idea what the best practices for that are

My biggest challenges were mainly concerned with the above. I overcame them all by trying to work on small scale projects for each risk one by one. I made small scale projects to re-learn python, create a site in flask, script something that interacts with bash, creating a script to install dependencies, and manage a database with SQLAlchemy.  Other than that, I tried to learn the skills I needed based on the goal of my sprints (scripting, install/setup, and web dev).  This did come back to bite me a couple times, because I had to develope and learn at the same time on a crunched timeline.

---

## **Outstanding Issues**

I only have to issues, scapy doesn't install correctly and may sometimes need manual install and the scan page sometimes doesn't reload after finishing (sometimes takes longer than the allotted time in the loading bar).

---

## **Video Demonstration, Project Planning Documents, and Screenshots**
Here is my **[Video Demonstration](https://youtu.be/QNEV_MoPcNQ)** that goes over my final submission's functionality, code, and most difficult issue I encountered.
[![IMAGE ALT TEXT HERE](https://i9.ytimg.com/vi/QNEV_MoPcNQ/mq2.jpg?sqp=CPC1q4MG&rs=AOn4CLBVq0j8hpi_lmtYZ59TXJN5FnMwFw)](https://youtu.be/QNEV_MoPcNQ)


Below will be links to my project planning documents:
 - [Project Proposal](https://docs.google.com/document/d/1pg_mEUOqFhxTsGsA435HpgMtg91far8Agp0mrHdH91k/edit?usp=sharing)
 - [Requirements Document](https://docs.google.com/document/d/1fgxIiI9hz0epV6K2WQsTxS0JCYTevAMDJNG45P_vgrI/edit?usp=sharing)
 - [Project Design Report](https://docs.google.com/document/d/1v1dn24ysHzHMVFWKqLSSSDKWW661LsDWZa1xOgVKl-w/edit?usp=sharing)
 - [Test Cases](https://docs.google.com/spreadsheets/d/1qxEOJRloOvlLFDv1exGzjEEpxZnYfWXp7LVJLyXyLVE/edit?usp=sharing)
 - [User Stories](https://docs.google.com/spreadsheets/d/19BBOpORVL5XS-3QDqhetDGyS-B04Luq9_laX4_Vq1-s/edit?usp=sharing)
 
![Home Page](https://a3-images.myspacecdn.com/images04/5/89e1f2bc187946aabbf6f826f21141b6/full.jpg)
![History Page](https://a2-images.myspacecdn.com/images04/4/d84d72e7712a4c06912de1c8ce688c28/full.jpg)
![Scan Page](https://a1-images.myspacecdn.com/images04/11/1ece233f52ed4c75a5e7611418cbdc93/full.jpg)
![Deauth Page](https://a2-images.myspacecdn.com/images04/5/a025a98adef34b998a03d8cd6133a535/full.jpg)

