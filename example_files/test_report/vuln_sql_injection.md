---
v_sqli:
    name: Functions vulnerable to SQL injection
    rating: Medium
    num_treatments: '1'
    status: Fixed
...

## %{v_sqli.name}{.finding}

| Rating                      | Status           | 
|:----------------------------|:-----------------|
| [%{v_sqli.rating}]{.rating} | %{v_sqli.status} | 

### Description

Several instance of unsafe string concatenation were discovered that could lead to SQL injection.

* Method uploadAndProcess in ReferenceDataImporter.class: the contents of a file which includes wholesaler information is read, parsed, and a number of queries executed using the data without validation. The logic related to parsing the file was complex and it wasn't clear under what conditions injection could occur.

```java
        String firstToken = csvTokenizer.nextElement().toString();

        ... snip ...

        else if (currentTable.equals("ref_wholesaler"))
        {
          Statement stmt = (Statement)conn.createStatement();
          ResultSet rs = stmt.executeQuery("SELECT * FROM ref_wholesaler where code = '" + firstToken + "'");
          if (!rs.next())
          {
            LOG.debug("Adding to " + this.properties.getProperty("DATABASE") + " : class com.a3.domain.common.Wholesaler : " + firstToken);
            stmt.executeUpdate("INSERT INTO ref_wholesaler VALUES ('" + firstToken + "','" + csvTokenizer.nextElement().toString() + 
              "','" + csvTokenizer.nextElement().toString() + "','system','" + file_date + "')");
          }
        }
```

* Method doesServiceNumbersExist in ServiceNumberDirectDAO.class: the supplied list of service numbers may be user controlled. When entering service numbers, input validation checks allowed entry of "78654a') or ('1'='1".

```java
  public boolean doesServiceNumbersExist(String db, List<String> numbers)
    throws Exception
  {
    Connection connection = getConnection(false);
    StringBuffer numberStringBuffer = new StringBuffer();
    for (String number : numbers)
    {
      if (numberStringBuffer.length() > 0) {
        numberStringBuffer.append(",");
      }
      numberStringBuffer.append("'" + 
        StringUtil.standardizeNumber(number) + "'");
    }
    String sql = "select * from " + db + 
      ".service_number where service_number in (" + 
      numberStringBuffer.toString() + ")";
    Statement statement = connection.createStatement();
    
    ResultSet resultSet = statement.executeQuery(sql);
    boolean result = false;
    if (resultSet.next()) {
      result = true;
    }
    cleanup(resultSet, false);
    return result;
  }
```

* Method insertSERRecord in EventDAOImpl.class: the review did not identify whether the supplied serRecord can come from an untrusted source.

```java
  public void insertSERRecord(TelstraSER serRecord)
  {
    Statement statement = null;
    try
    {
      statement = getSession().connection().createStatement();
      ResultSet rs = statement
        .executeQuery("select * from telstra_ser where service_number = '" + 
        serRecord.getServiceNumber() + 
        "' and call_type = '" + 
        serRecord.getCallTypeCode() + 
        "' and (date_off = 'null' or date_off = '') and quantity = '" + 
        serRecord.getQuantity() + "' order by id");
```

* Method doesServiceNumbersExist in TestServiceNumberAlreadyExists.class:  might be vulnerable.

```java
public boolean doesServiceNumbersExist(String db, List<String> numbers, Connection connection)
    throws Exception
  {
    StringBuffer numberStringBuffer = new StringBuffer();
    for (String number : numbers)
    {
      if (numberStringBuffer.length() > 0) {
        numberStringBuffer.append(",");
      }
      numberStringBuffer.append("'" + StringUtil.standardizeNumber(number) + "'");
    }
    String sql = "select * from " + db + ".service_number where service_number in (" + numberStringBuffer.toString() + ")";
    System.out.println(sql);
    Statement statement = connection.createStatement();
    
    ResultSet resultSet = statement.executeQuery(sql);
```

Overall there were a large number of SQL queries that did not make use of parameterised statements, but did not appear to draw their input from sources that could be user controlled. A full list has not been compiled but should be readily identified by searching the source code for the string "executeQuery".

### Treatments
<div class="treatment">
#. Use prepared statements to construct all SQL queries. https://www.owasp.org/index.php/SQL_Injection_Prevention_Cheat_Sheet contains more information including alternative treatments if prepared statements are not practical.
</div>

BTB have have reviewed the code and either updated methods to use prepared statements or deprecated them. BTB have provided code snippets as evidence.

### References

* [SQL Injection](#### SQL Injection})
