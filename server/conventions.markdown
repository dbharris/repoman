# Conventions used in Repoman
All conventions listed in this file are(or will be) enforced by the repoman
server.

*minimum and maximum values are somewhat arbitrary at the moment*

## Group Names
* lowercase `a-z` characters allowed
* minimum length: 3
* maximum length: 100

* uppercase will be be accepted, but translated to lower case
* any invalid characters will result in an error

## User Names
* lowercase `a-z` characters allowed
* minimum length: 3
* maximum length: 100

* uppercase will be be accepted, but translated to lower case
* any invalid characters will result in an error

## Passwords
* In the event that passwords are needed for a web interface
* minimum length: 10
* maximum length: 100
 * mixed case
 * numbers and symbols allowed
  * `!@#$%^&*(){}[],.<>-_+=?'"`, `0-9`

## Image Names
* Upper and lowercase characters, underscores and dashes and periods allowed
  * `a-z`, `A-Z`, `._-`
* minimum length: 3
* maximum length: 256
* unallowed characters will result in an error

## UUIDs
* UUIDs will always be stored within repoman as lowercase
* formatting characters will be stripped out
* When specifying UUIDs, both upper and lowercase as well as mixed case will be accepted
  * they will always be translated to lowercase serverside when performing a lookup

