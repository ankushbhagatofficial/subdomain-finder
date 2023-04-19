<h1 align="center">subdomainfinder</h1>

<p align="center">
A program to find subdomain of any domain.
</p>

<kbd> <img src = "https://user-images.githubusercontent.com/63346676/233093306-9efb8f9a-d5f5-49d3-8fbc-6943fdf4e99c.jpeg"></kbd>

Following program enumaretes possible list of sub-domains using Securitytrails API

## Register

Register account in [SecurityTrails.com](https://securitytrails.com/)
Activate Account to get the API Key

>**PREREQUISITES**

```python3```

>**SETUP PROGRAM**

```pip3 install subdomainfinder```

**Setup API KEY:**

>**For Linux/Macos:**
```
export SD_API_KEY="api_key_value"
```
>**For Windows:**
```
setx [SD_API_KEY] "[api_key_value]"
```
>**Usage:**

```subdomainfinder```

```subdomainfinder --help```
```python3
subdomainfinder --domain vulnweb.com --filepath vulnweb_sd.txt
```
