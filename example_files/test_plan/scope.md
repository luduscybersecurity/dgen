# Scope

## Background

%{client_long} (%{client}) is a company specialising in whitelabling broadband telecommunications services to businesses with existing customer bases. %{client} provide the complete range of services required to operate an internet service provider, allowing their customers to focus on the sales and marketing.

%{client} has entered into an agreement with a large energy provider to whitelabel their services, who has specified that their systems be subject to network and web application penetration testing prior to launch. One round of testing has been completed, with a second required.

Part of %{client}'s offering is an Invoice Portal, which requires security testing. In addition, further retesting is required from the previous round of penetration testing.

## Threat Model

Several threats have been identified as being of interest:

* Attacks from application users
* Attacks from the broader Internet

Of particular concern to BTB are attacks that could result in:

* Remote compromise of BTB systems
* Unauthorised disclosure of commercial and/or personally identifiable information
* Fraud or other loss of money

%{client} have stated that all users should have access to all functions.

## Activities

The following activities are in-scope for this assessment:

* A penetration test of the Invoice Portal
* Delivery of a single report covering all activities above
* Retesting of fixes implemented for vulnerabilities identified during the assessment and confirmation they are effective
* A review of remediation performed as a result of previous testing:
    * Missing/Default passwords
    * Domain privileges

## Exclusions

The following activities are out of scope:

* %{company} will not implement fixes for vulnerabilities identified the assessment
* Denial of service is out of scope
* Social engineering is out of scope
* Any activities not explicitly defined as in-scope is out of scope
