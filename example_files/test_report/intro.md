# Introduction 

The objective of the %{assessment_type} was to assess the effectiveness of %{client}'s preventative controls against attack by an adversary with credentials to CINDY, but not any other infrastructure.

## Timeframe

%{days_allocated} days of testing were allocated for this engagement. The testing was performed between %{test_start} and %{test_end}.

## Scope

The test scope was:

* A penetration test of CINDY.
* A penetration test of Internet facing infrastructure.
* A penetration test of the internal networks.

Further information can be found in the test plan btb_2017_test_plan_v1.1.pdf.

## Personnel

The following individuals were involved in the testing process:

Name            | Role               | Phone           | Email
:---------------|:-------------------|:----------------|:-----------------------------------------
%{author}       | Security Tester    | 0432 918 830  | george.stewart@colmancomm.com
Sachin Patel    | GM - Product & Technology | 0411 655 405 | sachin@btbaustralia.com.au
Graham Corrigan | GM - Software and Architecture | 0409 368 903 | graham@btbaustralia.com.au
Clem Colman     | Security Consultant | 0417 744 511 | clem@colmancomm.com

## Setup

Testing of CINDY was performed in a environment dedicated to the %{assessment_type}. All other testing was performed in production. 

The testing was conducted with limited knowledge of the target. The following was supplied:

* Test accounts for CINDY.
* Libraries in use by CINDY.
* Network diagrams for the organisation.
* An error checking feature that would disable the application for an IP after a certain threshold of errors was hit was disabled.
* Once code execution in CINDY was proven, VPN access to the internal network was provided so that testing could continue without affecting production.
