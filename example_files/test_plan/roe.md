# Rules of Engagement

## Proposed Dates

 Milestone                  | Date
:---------------------------|:----------------
Test Start                  | %{planned_start}
Test End                    | %{planned_end}
Draft Report Delivery       | %{planned_draft}
Acceptance of Final Report  | %{planned_final}

## System Details

The following system details have been provided:

 System                     | IP/URL                    | Entry Point
:---------------------------|:--------------------------|:----------------------
Invoice Portal              | http://10.3.65.74:9999/   | http://10.3.65.74:9999/
Retest systems              | 10.3.11.11, 10.3.11.12, 10.3.11.13, 10.3.11.14, 10.3.11.16, 10.3.11.17, 10.3.11.18 | N/A


## Accounts

The following accounts will be supplied:

 Account Type           | Number        | System
:-----------------------|:--------------|:-----------------------
Portal User             | 3             | Invoice Portal
Domain Administrator    | 1             | b2b.local

## Contacts

 Name               | Role               | Number        | Email
:-------------------|:-------------------|:--------------|:-----------------------
George Stewart      | Penetration Tester | 0432 918 830  | george.stewart@colmancomm.com
Sachin Patel        | GM - Product & Technology | 0411 655 405 | sachin@btbaustralia.com.au
Graham Corrigan     | GM - Software and Architecture | 0409 368 903 | graham@btbaustralia.com.au
Clem Colman         | Security Consultant | 0417 744 511 | clem@colmancomm.com

## Permitted Activities

The following table shows activities that are permitted and those that are expressly forbidden.  Any activity not included in this list is forbidden by default.

%{company} will seek specific agreement should any actions potentially affect the integrity or availability of targeted systems.

### External testing

Activity                                    | Execution Permission
:-------------------------------------------|:----------------------
Network scanning and service identification | PERMITTED
Vulnerability scanning and identification   | PERMITTED
Vulnerability exploitation                  | PERMITTED
Modification of system configurations       | PERMITTED (CINDY ONLY)
Modification of application/business data   | PERMITTED (CINDY ONLY)
Brute force attempts                        | PERMITTED
Denial of Service (DoS) testing             | NOT PERMITTED
Social engineering                          | NOT PERMITTED


## Third Parties

The following third parties have been identified as managing systems under test, or as being likely to recieve security events while testing is underway. They should be notified that the %{assessment_type} is taking place, and given a chance to warn users, security teams, system managers and upstream providers that there may be a potential interuption to services and/or a large number of security events generated.

* N/A

## Source IPs

The %{assessment_type} will be performed from the following IP addresses:

* N/A

Intrusion Detection Systems and other automatic countermeasures operated by %{client} or other third parties should be configured to ignore traffic from these addresses for the test.
