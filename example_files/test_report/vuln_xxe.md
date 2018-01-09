---
v_xxe:
    name: XML External Entity Injection
    rating: Medium
    num_treatments: '1'
    status: Fixed
...

## %{v_xxe.name}{.finding}

| Rating                     | Status          |
|:---------------------------|:----------------|
| [%{v_xxe.rating}]{.rating} | %{v_xxe.status} |

### Description

One potential instance of XML external entity injection was discovered in the getBPayments method of EziDebtPaymentImpl.class. The DOM Parser was not configured to disable external entity processing after creation, and the remote DTD is supplied to the parser.

```java
  public List<String> getBPayments(SystemParamService systemParamService)
  {
    DOMParser parser = new DOMParser();
    List<String> ret = new ArrayList();
    try
    {
      PaymentExchangeLocator pel = new PaymentExchangeLocator();
      pel.setPaymentExchangeSoapEndpointAddress(systemParamService.getSystemParamString(SystemParamKey.EZIDEBIT_SERVER_URL));
      PaymentExchangeSoap pes = pel.getPaymentExchangeSoap();
      Calendar cal = Calendar.getInstance();
      cal.add(5, -7);
      String result = pes.getPaymentsExXmlString(systemParamService.getSystemParamString(SystemParamKey.EZIDEBIT_KEY), "ALL", "ALL", "ALL", "", DateUtil.safeFormatDate(cal.getTime(), DateFormatKey.DATE_FORMAT_YYYY_MM_DD), DateUtil.safeFormatDate(new Date(), DateFormatKey.DATE_FORMAT_YYYY_MM_DD), "SETTLEMENT", "", "");
      
      // Remote DTD in supplied to parser.
      ByteArrayInputStream bis = new ByteArrayInputStream(("<?xml version=\"1.0\" encoding=\"ISO-8859-1\"?>\n" + result).getBytes());
      InputSource is = new InputSource(bis);
      parser.parse(is);
```

Due to time restrictions exploitation was not attempted, but in theory could result in disclosure of system files, server side request forgery (including port scanning) or denial of service.

### Treatments
<div class="treatment">
#. Configure the XML parser not to parse XML External Entities as per https://www.owasp.org/index.php/XML_External_Entity_(XXE)_Prevention_Cheat_Sheet
</div>

BTB state they have deprecated this function.

### References

* [XML Entity Injection](#### XML Entity Injection)
