# Site map: demoblaze (https://www.demoblaze.com/)

Explored on 2026-10-30, LOGGED OUT only (settings.md has no "Login (LOGGED IN mode)" section; the site only has a username/password login).
Desktop: Chrome 1440x900. Phone: Chrome mobile emulation 390x844 (iPhone 14 size).
Screenshots: explore/

## Pages

| # | Page | URL | Screenshot |
|---|------|-----|------------|
| 1 | Home (product list, page 1 and 2) | https://www.demoblaze.com/ | 01-home, 02-home-footer, 03-home-page2 |
| 2 | Home filtered by category | https://www.demoblaze.com/# | 04-category-laptops |
| 3 | Product page (3 visited: phone, laptop, monitor) | prod.html?idp_=1, 15, 14 | 05, 06, 07 |
| 4 | Product page with an unknown id | prod.html?idp_=999 | 08-product-unknown-id |
| 5 | Cart (empty) | https://www.demoblaze.com/cart.html | 09-cart-empty |
| 6 | Contact, About us, Log in, Sign up popups | (on any page) | 10 to 13 |
| 7 | Unknown page | https://www.demoblaze.com/this-page-does-not-exist | 14-error-page |
| 8 | Phone view | https://www.demoblaze.com/ | 15-mobile-home-menu, 16-mobile-footer |

## Facts (LOGGED OUT)

### Home
- F-01: The tab title is "STORE" on Home, product pages and Cart.
- F-02: No cookie banner is shown.
- F-03: Header, left to right: logo image and "PRODUCT STORE" (both link to index.html), then "Home", "Contact", "About us", "Cart", "Log in", "Sign up". "Home" has the hidden text "(current)" on every page, including product pages and Cart.
- F-04: A carousel with 3 slides ("First slide", "Second slide", "Third slide"), previous / next arrows and 3 indicators. It rotates by itself. Clicking the next arrow shows the next slide and adds "#carouselExampleIndicators" to the address.
- F-05: A "CATEGORIES" box with "Phones", "Laptops" and "Monitors".
- F-06: Page 1 of the product list shows 9 products, each with an image, a title link, a price and a short description: "Samsung galaxy s6" $360, "Nokia lumia 1520" $820, "Nexus 6" $650, "Samsung galaxy s7" $800, "Iphone 6 32gb" $790, "Sony xperia z5" $320, "HTC One M9" $700, "Sony vaio i5" $790, "Sony vaio i7" $790.
- F-07: Below the list are "Previous" and "Next" buttons. "Next" shows page 2 with 6 products: "Apple monitor 24" $400, "MacBook air" $700, "Dell i7 8gb" $700, "2017 Dell 15.6 Inch" $700, "ASUS Full HD" $230, "MacBook Pro" $1100. On page 2 only "Previous" is shown.
- F-08: Possible bug: on page 2 the product images link to "#" (nowhere), while on page 1 and in the category views they link to the product page. The titles on page 2 do link to the product page (for example prod.html?idp_=10).
- F-09: "Phones" shows 7 products (the 7 phones of F-06), "Laptops" shows 6 ("Sony vaio i5", "Sony vaio i7", "MacBook air", "Dell i7 8gb", "2017 Dell 15.6 Inch", "MacBook Pro") and "Monitors" shows 2 ("Apple monitor 24", "ASUS Full HD"). The address becomes https://www.demoblaze.com/#. In a category view only "Previous" is shown.
- F-10: Footer: "About Us" with "We believe performance needs to be validated at every stage of the software development cycle and our open source compatible, massively scalable platform makes that a reality.", "Get in Touch" with "Address: 2390 El Camino Real", "Phone: +440 123456", "Email: demo@blazemeter.com", the logo with "PRODUCT STORE", and "Copyright © Product Store". The footer has no links.

### Product pages
- F-11: A product page (for example prod.html?idp_=1) shows the product image, the name as a heading ("Samsung galaxy s6"), the price with "*includes tax" ("$360 *includes tax"), "Product description" with text, and a green "Add to cart" button. Laptop (idp_=15 "MacBook Pro" $1100) and monitor (idp_=14 "ASUS Full HD" $230) pages look the same.
- F-12: On product pages and Cart the header is laid out differently from Home: the logo starts further right (about 165 px from the left instead of 16 px) and the menu is in the middle.
- F-13: Bug: prod.html?idp_=999 (a product that does not exist) shows "undefined" as the name, "$undefined *includes tax", "undefined" as the description, a broken image and a working-looking "Add to cart" button, instead of an error message.

### Cart
- F-14: Cart (cart.html), with nothing added: heading "Products", a table with the columns "Pic", "Title", "Price" and "x" and no rows, heading "Total" with no amount, and a green "Place Order" button. "Place Order" opens the order form (not clicked: Never).
- F-15: On Cart the "Products" heading and table touch the left edge of the window (no side margin).

### Popups
- F-16: "Contact" opens a "New message" popup with "Contact Email:", "Contact Name:" and "Message:" fields, a "×", "Close" and "Send message". "Close" closes it.
- F-17: "About us" opens an "About us" popup with a video player (poster image, "Play Video" button, not autoplaying) and a "Close" button. "Close" closes it. The video was not played.
- F-18: "Log in" opens a "Log in" popup with "Username:" and "Password:" fields, a "×", "Close" and "Log in". The "×" closes it.
- F-19: "Sign up" opens a "Sign up" popup with "Username:" and "Password:" fields, a "×", "Close" and "Sign up". Pressing Escape closes it.
- F-20: Accessibility: the "Username:" and "Password:" labels in the Log in popup and the "Contact Email:" label in the Contact popup are not linked to their fields (no label "for"), so screen readers announce the fields without a name. The Sign up fields, "Contact Name:" and "Message:" are linked.

### Error page
- F-21: https://www.demoblaze.com/this-page-does-not-exist answers 404 with a plain server page: tab title "404 Not Found", "Error: Not Found" and "The requested URL /this-page-does-not-exist was not found on this server." It has no header, no styling and no link back to the shop.

### Phone (390x844)
- F-22: On a phone the header shows the logo and "PRODUCT STORE", and the menu items are already shown below it without tapping anything, wrapped onto two lines ("About / us", "Log / in", "Sign / up").
- F-23: The burger button ("Toggle navigation") is at the top right but has no visible icon (no border, no background, no icon image). The first tap changes nothing visible; the second tap hides the menu.
- F-24: On a phone the carousel is hidden, which leaves an empty blue area of about 500 px below the menu.
- F-25: On a phone the products are shown 1 per row, and the footer sections are stacked. The body is 405 px wide in a 390 px window, so the page can be moved sideways a little (a light strip shows at the right edge).

## Non-functional facts (LOGGED OUT)

Measured on 2026-10-30 in a new Chrome session.

- N-01: Home timing: time to first byte 0.25 s, first contentful paint 1.16 s, load event 1.45 s; 29 resource requests. No failed requests.
- N-02: No broken images on Home (14 images).
- N-03: http://www.demoblaze.com/ redirects to https://www.demoblaze.com/ with a 302 (temporary) redirect. https://demoblaze.com/ (without www) answers 200 itself and does not redirect to www. No resources load over http.
- N-04: Response headers of https://www.demoblaze.com/: none of Strict-Transport-Security, Content-Security-Policy, X-Frame-Options, X-Content-Type-Options, Referrer-Policy or Permissions-Policy is sent ("server: Google Frontend").
- N-05: html lang is "en".
- N-06: Home has no h1 heading (products are h4, prices h5). The meta description is empty, and there is no canonical link and no og: tags. A favicon is present (blazemeter-favicon-32x32.png).
- N-07: Home: 2 images have no alt attribute (including the header logo) and 9 have an empty alt (the product images), so the 9 product image links have no accessible name.
- N-08: The viewport meta tag is "width=device-width, initial-scale=1, shrink-to-fit=no", which allows zooming.
- N-09: Keyboard: Tab reaches "Home" in the header and shows a visible blue focus outline.

## Not explored (and why)
- LOGGED IN mode: the site only has a username/password login, and the agent never types into fields.
- "Add to cart", "Place Order" and the order form: they lead to a purchase (Never).
- "Send message", the "Log in" and "Sign up" submit buttons: they need typing.
- The About us video was not played.
