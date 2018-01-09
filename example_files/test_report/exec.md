# Executive Summary

%{client_long} (%{client}) commissioned %{company} to perform a %{assessment_type} against %{target}. The objective of the %{assessment_type} was to assess the effectiveness of %{client}'s preventative controls against attack by an adversary with credentials to CINDY, but not any other infrastructure.

Testing was conducted between %{test_start} and %{test_end}.

## Report findings and vulnerability summary

The key findings of the %{assessment_type} were:

#. An unauthenticated remote code execution vulnerability was discovered in the CINDY application.
#. The CINDY application was hosted jointly in a cloud instance and on the internal network. There were no controls enforcing network segregation between the internally hosted instance and the workstations on the internal network.
#. %{company} was able to establish domain dominance once a foothold on the internal network had been established.

Below is an overview of the vulnerabilities identified by %{company} during testing, grouped by priority:

<div class="rating center">
| [Urgent]{.urg}     | [High]{.high}        | [Medium]{.med}     | [Low]{.low}        | [Optional]{.opt}   |
|:------------------:|:--------------------:|:------------------:|:------------------:|:------------------:|
| [%{num_urg}]{.urg} | [%{num_high}]{.high} | [%{num_med}]{.med} | [%{num_low}]{.low} | [%{num_opt}]{.opt} |
</div>

A total of %{num_treatments} treatments have been recommended to address them.

## Systemic analysis and recommendations

<div class="rec">
A critical vulnerability was discovered allowing remote unauthenticated code execution. This was caused by the usage of the struts framework version 1, which has an unpatched vulnerability that will never be addressed as the framework has been marked "end of life". In addition to this, a list of other libraries and and their versions indicate that apache-common-collections version 3.1 is in use. This library suffers from a critical de-serialisation flaw that can result in remote code execution. However, checks of the application for evidence of serialised objects passed to the browser did not turn up any results.

#. Update application development practices to require the use of up-to-date components.
#. Integrate a tool to monitor libraries for vulnerabilities into the build and deploy process, so that vulnerable libraries can not be pushed into production. One such open source tool is [OWASP Dependency Check](https://www.owasp.org/index.php/OWASP_Dependency_Check).

Escalation to domain administrator privileges was made possible through the use of missing authentication, default credentials and password reuse. It is likely that had these issues not been discovered, %{company} would not have been able to achieve domain dominance within the test window. It was noted that %{client} seems to have a strong password policy, and it is unlikely that any passwords would have been cracked if attempted.

#. Ensure that deployment processes require all devices have default credentials changed prior to deployment.
#. Encourage the use of password managers to avoid password re-use.
#. Reset all credentials identified in this report including credentials for the btb.local domain and KRBTGT account (which must be reset twice in quick succession). The resource https://adsecurity.org/?p=483 provides background into the operation and the resource https://gallery.technet.microsoft.com/Reset-the-krbtgt-account-581a9e51 contains a script that can assist with the process.

%{company} did not observe an Active Directory design that aligns with best practice. Everyday use accounts of executives had been given domain administrator privileges, and groups to support role based access control were not observed.

#. Review the Active Directory architecture against Microsoft best-practice.
</div>