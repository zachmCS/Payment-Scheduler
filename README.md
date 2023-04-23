# Liquid Thunder Payment Scheduler

### Averi Bates, Marcos Bernier, Cameron Campbell, Toby Griffin, Zachary Muller

## Introduction

For the Spring 2023 semester, we were tasked by MSCI, Inc to build an application for our capstone design project - an important requirement for our graduation. We received a written explanation on what the firm desired from an application, and these requests are briefly summarized below.

MSCI is a global finance firm that provides indexes and financial instruments for the stock market, real estate, and other financial tools. Being a financial firm, MSCI has placed a lot of importance into the ability to calculate payable dates of financial instruments in a quick and efficient manner. Accordingly, MSCI has asked us to create a payment-scheduling application with some of the following as highly-desired features:

- Ability to pick a start and end date
- Selection of payable frequencies, such as monthly, weekly, etc.
- Acknowledgement of holidays and weekends as incompatible dates
- Ability to pick specific instructions (rules) that dictate what happens when a payable date falls on the same date as a holiday or weekend
- Exportability of date lists (optimally in a CSV format)
- Cloud-deployability considered in development, and tested

After meeting for the first time with project mentor and MSCI employee Gabriel Cardoso, we were able to further our understanding of the ideal final product. Additionally, the team decided to establish bi-weekly meetings with Gabriel in order to receive consistent feedback and ideas from him. Gabriel was an immense help whenever his input or ideas were needed!

## Team Roles

Although the development work on this project was mostly an all-hands collaborative effort, the team established de-facto “experts” on specific subject matters early on in the project development. These leaders served as managers of their respective subject matters, giving helpful context to other contributing group members whenever necessary.

### Front-End Development

*Zachary Muller and Marcos Bernier*

The front-end development team was responsible for everything readily evident to the user and relating to user input and system output. The front-end team created the user interface, and set it up so that users could interact with it and present data/options to it. This information was then packaged and sent to the back-end for respective operations. The output of the back-end was then received and presented by the front-end team.

### Back-End Development

*Averi Bates and Cameron Campbell*

The back-end development team was responsible for all inputs received from the front-end system. The team worked to create all applicable calculations and rule applications that MSCI requested. The team standardized the date calculation and collection process, allowing the program to receive an ordered pair of dates, a rule, a holiday jurisdiction, and frequency, ultimately having the back-end return a list of payable dates to the front-end.

### Cloud Deployment

*Toby Griffin*

The cloud deployment team was responsible for ensuring that the application was able to be run on the cloud by the end of the development cycle. This was done by countless test cycles done every time a major update was made to the application. Because of the cloud-friendly nature of the libraries used to develop this application, the application was thankfully nearly always cloud-ready.

## Underlying Technologies / Libraries

Before diving into the finished product, it is important to discuss the two major libraries that our payment scheduler takes advantage of in order to increase usability and efficiency of the program. There are two major (non-standard) libraries that are used to make the program work, *Holidays* and *Streamlit*.

### Holidays

Holidays is a Python package that provides an easy and efficient way to calculate holidays for different countries and regions. The team used this library to bypass many of the perceived difficulties related to the consideration of several different regions and their respective holiday calendars. With the Holidays library, we were able to simply instantiate a Holidays object and pass the desired region to it as an initializing argument. Then, when checking to see if specific dates were holidays or weekends, the library allowed for dates to be passed to the object as parameters of a function that returned *****true***** if the date was a holiday or weekend day, and ******false****** if it wasn’t.

### Streamlit

Streamlit is an open-source Python library that allows you to create interactive web applications in a few lines of code. We used this library in order to eliminate the stress and time involved with developing a user-interface from scratch. Using Streamlit, we were instead confronted with a very modular coding experience, where an input box could just be dropped into the environment in a perfectly-aligned format with just a line or two of code. When ran, a Python program containing a Streamlit user interface will automatically launch a web-application on an open port on the local machine. Because of this, it was incredibly easy for the team to develop this application for cloud deployment, as virtually no extra action was needed. 

## Application Appearance and Function

Once completed, the front-end team worked to make the user interface aesthetically pleasing and ensured that all was working. Thanks to Streamlit, this part of the development process was relatively easy. An image of a working state of the application is shown below:

![Untitled](Capstone%20Final%20Report%20218a5b719bc74326b945f17409acac7b/Untitled.png)

The application allows the user to select several options. First, the user can select a start date and an end date on the main section of the application. Then the user can access the sidebar to modify several values. The first value, being the payment schedule, tells the back-end how often the user desires a payable date to be calculated. The second value of holiday calendar allows the user to select a region and its corresponding financial holiday calendar. For the purpose of this application, we chose a financial calendar from every inhabited continent: NYSE, ECB, China, Brazil, Australia, and Nigeria. The last drop-down box allows the user to select a payment rule. The payment rule specifies what happens when a payable date falls on the same day as a weekend or holiday. The rules are laid out below:

- Following Business Day - If a date is a holiday or weekend, the payable date should be the closest following business day.
- Previous Business Day - If a date is a holiday or weekend, the payable date should be the closest previous business day.
- Modified Following Business Day - If a date is a holiday or weekend, the payable date should be the closest following business day, if and ONLY IF the date in question is in the same month as the original, non-valid date.
- Modified Previous Business Day - If a date is a holiday or weekend, the payable date should be the closest previous business day, if and ONLY IF the date in question is in the same month as the original, non-valid date.
- No Modification - Allow weekends and holidays to be valid payable dates. Implement no rules.

Additionally, the sidebar allows for the selection and implementation of the “End of Month” rule, which specifies that if a frequency calculation that uses months is selected, and the initial date is the end of its respective month, then all payable dates should default to the end of each month. For example, if February 28th 2023 was selected for a monthly payment cadence and “End of Month” was enabled, then the next payable date would be March 31st, 2023. The dates are exportable to the user’s device; they are downloaded into CSV format in the near-exact way they are displayed, except for the months column, which becomes a number rather than a name. The application, thanks to Streamlit, automatically scales to mobile devices and is perfectly compatible with responsive-touch (touchscreen) interfaces. 

## Cloud Deployment

A major ask of MSCI was that the application be cloud-ready, or easily deployable to the cloud with little modifications to the source code. With the libraries we were relying on for the presentation of the user interface, we found it nearly seamless to transition from hosting the application on a local machine for one user to hosting it on a public cloud service for multiple simultaneous users. We were able to create instances on Amazon Web Services, and with Internet traffic enabled on these instances, we were able to use the application and all of its features successfully from multiple devices at once. We intend to allow our peers to experience our application during the final presentation by accessing it at one of many provided IP addresses during the presentation.

## Future Features

Although our work has come to an end on this application, we believe it has potential for future continuous development and we hope that MSCI chooses to adopt it and assign resources to it. Before wrapping up development, the team had a discussion of possible future features or actions to take , and we present them below as suggestions to the MSCI team:

- Create a reserved domain for the web-application and host it internally on MSCI servers
    
    Because MSCI is a financial firm, the nature of their internal work is sometimes sensitive. Although we don’t believe this application can pose any risk by being publicly hosted using cloud services such as GCP or AWS, we still believe that it would be best for MSCI to host it internally, and only allow staff on the intranet to access it at a convenient domain name, such as *paymentscheduler.msci.com.*
    
- Make a local (machine) version of the application
    
    Although we believe that our choice to develop a web-app was the right choice, we think that MSCI should explore building a local application. Such a theoretical application could be written in C# and inherit the same design characteristics as our version of the application.
    
- Include export via email function
    
    While our final version of the web application does include the ability to export lists of dates via a convenient CSV file, we recognize that some users may be accessing the application from a device that they don’t necessarily need the information downloaded to, while still wanting to retain the information. We propose that MSCI implement a function that allows CSVs to either be locally downloaded, or sent to the corresponding employee’s email inbox.
