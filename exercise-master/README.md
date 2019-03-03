````Holvi transaction API exercise
==============================

Welcome to Holvi transactions API exercise!

In this exercise, you'll implement an API for recording transactions to
simple bank accounts. A skeleton Django project is provided, but the rest is
up to you.

To get the app running, you should install Python 3.6.x and Django 2.1.x
in your development system. On top of that you should use Django Rest
Framework (DRF) for the implementation of the API. You can use other
libraries if you so wish.

Your submission should be returned as a Git repository. We prefer publicly
accessible Github repositories, but other submission methods are OK too,
as long as we have access to your code and Git commits. When working with
Git we prefer small commits over larger ones. At least the commit history
should clearly separate the skeleton project from your work.

Minimum requirements
--------------------

Complete the following tasks based on existing database models and
Django Rest Framework:
  1. Implement an API for fetching balance of an account
     (API endpoint GET /account/uuid/balance/).
  2. Implement an API for fetching transactions on account.
     The main use case for the API is to build the typical transaction
     listing you can see in most mobile banks. Design the API as you
     see best for this use case.
  3. Implement an API to POST a new transaction to account.
     You should prevent withdrawal transactions if recording the
     transaction would return in negative account balance. Note that
     the operation should be recorded atomically. That is, the transaction
     listing and account balance shouldn't go out of sync.
  4. Implement a management command to load some users, accounts and
     transactions to the system.
  5. Implement tests for the APIs and business logic you have built.

We appreciate if you follow Python's and Django's typical coding conventions
for your source code, API design and testing setup.

Include a small document where you explain how to set up, run and test your
solution. There will be a review session afterwards where you can explain your
solution in detail.


Optional tasks
--------------

We have collected a large list of optional additional tasks. The main purpose
of the additional tasks is to allow you to show your skillset a bit more. If
you feel you know a bit more than the usual candidate about some of below
tasks, do let us know by completing the task!

Descriptions can be done either in written form or as part of the review
session for your submission.

Client & features: 
  1. Implement a web frontend for the APIs. Usage of some Javascript
     framework is a big bonus for this task.
  2. Implement console based client for the APIs.
  3. Implement operations personnel access to the system. The system should
     allow operation personnel to find and view details of users, accounts
     and transactions, and to do corrections to the data.
  4. Implement a change to the account balance API so that it's possible
     to query the balance of the account at end of given date.

Authentication and audit:
  1. Describe or implement authentication and authorisation solution for above
     APIs.
  2. Describe or implement an audit system for above APIs (a solution
     which allows one to see who did what in the system).

Concurrency, scalability, reliability:
  1. Describe possible pain points in scaling the system to tens of thousands
     of users. Some of the users could have very large number of transactions
     on single account.
     What if the system would need to scale to tens of millions of users,
     each with millions of transactions on an account?
  2. Describe or implement changes to make the system work correctly if
     there are concurrent POSTing of transactions to one account.
  3. Assume an external system posts transactions to the system. As part of
     the data posted there's a "source_transaction_id" field which is
     guaranteed to be unique in the external system. Describe or implement
     changes to the API and data model so that it works great for this use
     case (think of the case where the external system posts the same data
     twice).
  4. Assume you have a large amount of accounts in the system. Describe or implement
     changes to add a new field "currency" to the Account model. The field
     should default to 'EUR'. In which order database migrations, code
     releases and other possible operations should be applied if we want to
     keep the system running all the time without interruptions. For this task
     you should assume the database is PostgreSQL 10 or some other similarly
     advanced database.

Devops:
  1. Make the application run in a Docker container.
  2. Descrbe how you would implement CI for the application.
  3. Assume you would need to deploy the application in AWS. Which AWS features
     would you use to get the app running? How would you do the deployment?

Bookkeeping:
  1. Describe what it would mean to have a double entry bookkeeping system
     instead of the current single entry system. What would it imply on the
     data model side? Why would one want to use such a system for a bank
     account in general?

Keep in mind the real reason for this exercise. We want to be sure you know
how to write good clean Python code, which is easy to understand and maintain.

Above all, enjoy the exercise!
