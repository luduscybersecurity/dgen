---
v_xmli:
    name: Xml Injection
    rating: High
    num_treatments: '2'
    status: Fixed
...

## %{v_xmli.name}{.finding}

| Rating                      | Status           |
|:----------------------------|:-----------------|
| [%{v_xmli.rating}]{.rating} | %{v_xmli.status} |

### Description

The application is vulnerable to XML injection, which could be exploited to perform fraudulent credit card transactions.

In NABPayment.class the makePayment function uses string concatenation to build the XML request for payment without any attempt to XML escape the input.

```java

public BillPaymentResult makePayment(Money amountPaid, String cardNumber, String cvv, String expiryMonth, String expiryYear, String name, String cidn, String billId, SystemParamService systemParamService)
  {
    String xmlString = "<?xml version=\"1.0\" encoding=\"UTF-8\"?><NABTransactMessage><MessageInfo><timeoutValue>60</timeoutValue><apiVersion>xml-4.2</apiVersion></MessageInfo><MerchantInfo>  <merchantID>" + 
    
      System.getProperty("nabMerchant") + 
      "</merchantID>  <password>" + 
      System.getProperty("nabPassword") + 
      "</password> </MerchantInfo>" + 
      "<RequestType>Payment</RequestType><Payment><TxnList count=\"1\"><Txn ID=\"1\"><txnType>0</txnType><txnSource>23</txnSource>" + 
      "<amount>" + 
      amountPaid.getCents() + 
      "</amount><currency>AUD</currency><CreditCardInfo><cardNumber>" + 
      cardNumber + 
      "</cardNumber><cvv>" + 
      cvv + 
      "</cvv>" + 
      "<expiryDate>" + (
      expiryMonth.length() < 2 ? "0" + expiryMonth : expiryMonth) + 
      "/" + (
      expiryYear.length() == 4 ? expiryYear.substring(2) : 
      expiryYear) + 
      "</expiryDate><cardHolderName>" + 
      name.replaceAll("&", "&amp;") + 
      "</cardHolderName><recurringflag>no</recurringflag> " + 
      "<purchaseOrderNo>" + 
      cidn + 
      ":" + 
      billId + 
      "</purchaseOrderNo>" + 
      "</CreditCardInfo></Txn></TxnList></Payment></NABTransactMessage>";
```

The same issue was discovered in NABPaymentIndividualDD.class.

As these functions are related to payments, these weaknesses may be exploited to modify payment information and commit fraud.

BTB have stated the functions are no longer in use.

### Treatments
<div class="treatment">
#. Ensure that variables are XML escaped before concatenation into the XML request by either:
    * making use of an XML library to generate the query, such as org.w3c.sax, org.w3c.dom or JDom; or
    * use StringEscapeUtils from the Apache Commons Lang to escape each string before it's concatenated into the query.
#. Render the function in-operable or delete it if it's no longer required.
</div>

BTB state that they have either escaped all variables to XML requests using the method StringUtil.escapeXMLReservedCharacters() or depricated the function. They have provided code snippets as evidence.

### References

 * [XML Injection](#### XML Injection)
