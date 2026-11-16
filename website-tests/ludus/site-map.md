# Site map: ludus (https://site.ludus-game.com/)

Explored from scratch on 2026-11-16 (the older site map and test cases are in archive/2026-11-16-before-fresh-start/).
Desktop: Chrome 1440x900 (also 1280x800). Tablet: mobile emulation 768x1024 (iPad user agent). Phone: mobile emulation 390x844 (iPhone 14 size).
The Reward Chain event was running during the exploration ("Limited time", ending the same day).
Screenshots: explore/fresh/ (git ignores explore/).

## Pages

| # | Page | URL | Screenshot |
|---|------|-----|------------|
| 1 | Home | https://site.ludus-game.com/ | 01-home-cookie-banner, 02-home-news-popup, 02-home-referral-panel, 03-home-about-carousel |
| 2 | Store (one long page with sections) | https://site.ludus-game.com/store | 03-store-reward-chain-from-home, 04-store-gold-tab, 05-store-faq |
| 3 | Login popup (on any page) | - | 11-login-popup |
| 4 | Referral program panel (on any page) | - | 02-home-referral-panel |
| 5 | News popup (Home) | - | 02-home-news-popup |
| 6 | Store and Home in French | https://site.ludus-game.com/fr-FR/store, https://site.ludus-game.com/fr-FR | 06-store-french-1280 |
| 7 | Unknown page | https://site.ludus-game.com/this-page-does-not-exist | - |
| 8 | Tablet Store | same URL | 07-tablet-store |
| 9 | Phone Home, burger menu, Store | same URLs | 08-mobile-home-cookie, 09-mobile-burger-home, 10-mobile-store-gold |
| 10 | LOGGED IN: Store, Home, Referral panel, German Store, phone | same URLs + ?user-id={TEST_USER_ID} | loggedin-01 to loggedin-07 |

The site has only two real pages (Home and Store). "Reward chain" and "Loyalty shop" are sections of the Store page.

## Facts (LOGGED OUT)

### Cookie banner and keyboard
- F-01: The tab title on Home and Store is "LUDUS - Merge Battle Arena PvP Web Shop" (also on the French pages).
- F-02: On the first visit a cookie banner is shown at the bottom: title "How we use cookies", text "We only use essential cookies that allow us to run this service. Read our cookie policy to learn more.", a "cookie policy" link (https://xsolla.com/cookie, new tab), a blue "Dismiss" button and a round close (x) icon. After "Dismiss" the banner is gone and is not shown again on later page loads.
- F-03: Closing the banner with the round close (x) icon hides it, but it is shown again on the next page load (the choice is not saved).
- F-04: The footer button "Privacy settings" opens the cookie banner again; "Dismiss" closes it.
- F-05: Keyboard: the first Tab focuses the banner's close (x) icon; more Tabs reach "Dismiss"; Enter on "Dismiss" closes the banner. Header links show a visible focus outline when focused with the keyboard.

### Home
- F-06: Home header, left to right: LUDUS logo, "Home" (yellow, current page), "Store", "Reward chain", "Loyalty shop", green "Login" button. Link targets: logo and "Home" → https://site.ludus-game.com, "Store" → https://site.ludus-game.com/store, "Reward chain" → https://site.ludus-game.com/store#rewards, "Loyalty shop" → https://site.ludus-game.com/store#loyalty-shop. A hidden "Clan reward" link (→ /store#clan, not displayed) is also in the page.
- F-07: The header stays at the top of the window while scrolling (Home and Store).
- F-08: Clicking "Reward chain" on Home opens https://site.ludus-game.com/store#rewards and scrolls to the "Reward Chain" section; "Reward chain" is then yellow in the header.
- F-09: Hero: big LUDUS logo and three badges "Download on the App Store" (https://apps.apple.com/ae/app/ludus-strategy-card-rpg-battle/id6446642912), "GET IT ON Google Play" (https://play.google.com/store/apps/details?id=com.studion.mergearena&hl=en&pli=1) and "GET IT ON Web-Version" (https://ludus-game.com/game), all in a new tab.
- F-10: A "Special offer" card shows a bundle name, a short text, a percentage badge, "You will get:" with item amounts, "Available: 5/5", a loyalty point badge and a green "Check our store" button linking to https://site.ludus-game.com/store. The bundle content can change.
- F-11: Banner "Check out our Store and shop with profit", text "Buy game resources and Passes at lower prices and make savings with each purchase!" and a green "To the store" button that opens https://site.ludus-game.com/store in the same tab.
- F-12: "Latest news" shows 2 news cards (picture, date, title). Clicking a card opens a popup titled "News" with a picture, the news title, a date, the news text and a white close (X) button named "Close". "Close" and the Escape key both close the popup. (News content changes.)
- F-13: "About the game": a carousel of 5 slides with "Previous" / "Next" arrows and 5 dots ("Go to slide 1" to "Go to slide 5"). Slide 1 is a video (not played). "Next" moves to slide 2; a dot jumps to its slide; "Next" on slide 5 goes back to slide 1.
- F-14: "Don’t have the game? Download it today!" section with Google Play, App Store and Web-Version (https://ludus-game.com/game) badges, all in a new tab.
- F-15: "Follow us in social media!" section with 6 icon links, all in a new tab: YouTube (https://www.youtube.com/@playludus), X (https://twitter.com/playludus), TikTok (https://www.tiktok.com/@playludus), Discord (https://discord.gg/5qFQGUXQTD), Instagram (https://www.instagram.com/play.ludus.game), Facebook (https://www.facebook.com/play.ludus). None of them has an accessible name.
- F-16: Footer: three logo images, the copyright line "© <year> LUDUS", links "Support" (https://help.xsolla.com/), "Powered by Xsolla Web Shop" (https://xsolla.com/mobile-web-shop?...) and "Join Affiliate Program" (https://x.la/xpn), all in a new tab, a "Privacy settings" button and a blue language button "EN".
- F-17: The language selector has 15 options: English, Français, Deutsch, Español, Português, Italiano, Türkçe, 한국어, 日本語, 繁體中文, 简体中文, Русский, Bahasa Indonesia, Tiếng Việt, ไทย.
- F-18: Choosing "Français" opens https://site.ludus-game.com/fr-FR (html lang "fr"). Header: "Accueil", "Boutique", "Chaîne de Récompense", "Boutique de Fidélité", button "Se connecter". "Latest news" becomes "Dernières infos" with the same dates as in English ("10 novembre"); the floating button becomes "Programme de parrainage".
- F-19: The French cookie banner says "Comment nous utilisons les cookies" and its button is "Rejeter" (French for "Reject"), while the English button is "Dismiss".
- F-20: French Store (https://site.ludus-game.com/fr-FR/store): heading "LUDUS・Boutique en ligne officielle", sub-heading "Profitez de réductions et obtenez des ressources et pass pour le jeu 10 % moins chers !" (English says "much cheaper").
- F-21: A floating white "Referral program" button is shown bottom right. It opens a panel: "Invite friends — get bonuses together!", "Bring friends and enjoy bonuses when they make first purchases. Your friends will also get rewards.", "You will get:" "Emeralds x100, Gold x1000", "Your friend will get:" "Emeralds x650, Gold x10000", a green "Invite friends" button, "My rewards" and a "Log in to view rewards" button. While open, the floating button becomes a round X; clicking it closes the panel.
- F-22: At 1440x900 the top of the Referral panel is cut off above the window (the "Invite friends —" line is not visible).
- F-23: The "Login" button opens a popup "LOG IN TO MAKE PURCHASES" with "Scan the QR code with your mobile device", a QR code and a red close (x) button. Escape closes it.

### Store
- F-24: Store header: LUDUS logo, "Home", "Store" (yellow), "Reward chain", "Loyalty shop", green "Login". "Reward chain" and "Loyalty shop" scroll to their sections, and the header item of the section on screen turns yellow.
- F-25: Store top: heading "LUDUS・Official Webshop!" and "Enjoy lower prices - buy game resources and passes much cheaper!", then the "Special offer" card with a green price button (for example "USD 54.00" with a struck-through "59.99") and two point badges (gold store points and teal loyalty points).
- F-26: "Special offers": "Small welcome bundle", "Medium welcome bundle", "Big welcome bundle", each with item amounts, "Available: 1/1", a percentage badge, point badges and a USD price button, with "Previous offer" / "Next offer" arrows.
- F-27: "Seasonal": "Limited time" cards with countdowns (Clan Competition items) and USD prices (content changes).
- F-28: "Store" heading with a tab bar of 12 tabs: "Free wares", "Battle Passes", "Gifts to friends", "Licenses", "Might Passes", "Ludus Royal", "Ethereal Crystals", "Spells", "Runes", "Dice of Fortune", "Gold", "Emeralds". "Free wares" is yellow at first. At 1440 wide a right arrow ("More categories") is shown at the right end; after two clicks "Emeralds" is fully visible, the right arrow is gone and a left arrow ("Previous categories") is shown.
- F-29: Clicking the "Gold" tab scrolls to the "Gold" category and "Gold" turns yellow. "Gold" has 5 cards: "Small pile of gold" 5000, "Piggy bank of gold" 25000, "Carpetbag of gold" 60000, "Goblet of gold" 140000, "Strongbox of gold" 350000, each with two point badges and a green USD price button with a struck-through old price (for example "USD 2.88" and "3.20").
- F-30: "Free wares" has 3 cards: "Free emeralds" 100 ("Available weekly: 1/1"), "Free Gold" 500 ("Available daily: 1/1"), "Regular cannonballs" 1 ("Available daily: 1/1"), each with a timer and a green "Claim" button (not clicked).
- F-31: "Emeralds" has 5 cards ("Small pile of emeralds", "Pouch of emeralds", "Sack of emeralds", "Chest of emeralds", "Pot of emeralds"), each with a "1st purchase" label, "2 X" and a USD price.
- F-32: "Gifts to friends": ribbon "Buy Tickets as gifts for your friends and fellow Clan members!" and ticket cards (first: "Tournament Diamond Ticket"), each with a "Gift" badge, "Send to friends" and a USD price button.
- F-33: The other categories ("Battle Passes", "Licenses", "Might Passes", "Ludus Royal", "Ethereal Crystals", "Spells", "Runes", "Dice of Fortune") each show cards with a name, an amount and a USD price button.
- F-34: "Reward Chain" section (event): sub-heading "Reward system", text "Reward system adds a layer of motivation and enjoyment to the gaming experience, ...", a "Limited time" countdown, "0/1 points", "Step 1 of 8", 8 reward cards with point costs (1, 3, 5, 10, 30, 50, 70, 100) and a green "Log in to claim" button. "Log in to claim" opens the "LOG IN TO MAKE PURCHASES" popup.
- F-35: "Loyalty shop": 12 cards, each with a name, an amount, an "Available weekly: x/y" or "Available: x/y" line and a green button with a teal loyalty point price; some cards have a countdown. Two cards have almost the same name: "Astral hero" (1100) and "Astral Hero" (550). (Offers rotate.)
- F-36: "Don’t have the game? Download it today!" section with the three download badges.
- F-37: "FAQ" with 6 questions: "How does purchasing from Web Shop benefit me?", "Is it safe to purchase on Web Shop?", "Who can help me with my purchase issue?", "What payment methods does Web Shop support?", "How to make a purchase?", "What's a referral program?". Clicking a question opens its answer and its arrow points up; opening another question closes the first one. "Is it safe to purchase on Web Shop?" answers "Web Shop is provided by our partner Xsolla. Xsolla is PCI DSS Level 1 ...".
- F-38: Store footer: 6 social icon links (no accessible names), logos, copyright line, "Support", "Powered by Xsolla Web Shop", "Join Affiliate Program", "Privacy settings", "EN".
- F-39: Below the Store heading the tab bar sticks under the header. While "Reward Chain", "Loyalty shop" or "FAQ" is on screen, it still highlights "Emeralds" in yellow, and it covers the top of the "Reward Chain" and "Loyalty shop" heading ribbons.
- F-40: The browser console shows 404 errors for store.xsolla.com/api/v2/project/253824/user/offer_chain/1512, 1511 and 1310 on the Store page.

### Error page
- F-41: https://site.ludus-game.com/this-page-does-not-exist answers HTTP 404 ("Page Not Found" title for a moment) and then shows the Home page at https://site.ludus-game.com/. No error message is shown.

### Phone (390x844)
- F-42: Phone header: green burger button and green "Login" button (no logo). The page has no horizontal scroll.
- F-43: The cookie banner is shown on the phone too, with "Dismiss".
- F-44: A bottom banner is shown: "Add It to Home Screen", "To got a quicker access !" (grammar mistake), a green "Claim" button and an X ("Close pwa banner"). The X closes it (the banner's "Claim" was not clicked).
- F-45: The burger menu shows the LUDUS logo, a red close button named "Close", "Home" (yellow), "Store", "Reward chain", "Loyalty shop" and "Login".
- F-46: Phone Store: the tab bar scrolls sideways and cards are 2 per row. While the "Gold" category is on screen, the sticky tab bar highlights "Dice of Fortune" instead of "Gold".
- F-47: On the phone the floating "Referral program" button shows only its icon.

## Non-functional facts (LOGGED OUT)

- N-01: Home, first visit (no cache): time to first byte 0.7 s, first contentful paint 2.0 s, DOMContentLoaded 3.3 s, load event 4.1 s; 227 resource requests.
- N-02: Store (same session): first contentful paint 0.9 s, load event 3.2 s; 130 requests; 381 images.
- N-03: Failed requests: Store logs 404s for store.xsolla.com/.../user/offer_chain/...; logged in also .../user/reward_chain/.../balance and site.ludus-game.com/navigation.json/navigation.json.
- N-04: No broken images on Home and Store; every image has an alt attribute.
- N-05: http://site.ludus-game.com/store answers 308 with Location https://site.ludus-game.com/store. No resources are loaded over http.
- N-06: Response headers: Strict-Transport-Security "max-age=63072000; includeSubDomains; preload" is present. Content-Security-Policy, X-Frame-Options, X-Content-Type-Options, Referrer-Policy and Permissions-Policy are missing.
- N-07: html lang is "en" on English pages and "fr" on /fr-FR.
- N-08: Home: 16 links and 5 buttons with no accessible name. Store: 4 buttons with no accessible name. Neither Home nor Store has an h1 heading.
- N-09: The viewport meta tag is "width=device-width,initial-scale=1,maximum-scale=1,shrink-to-fit=no" (maximum-scale=1 blocks pinch zoom).
- N-10: The meta description is placeholder text: "Your Game takes players on a grand adventure filled with detractors, monsters, gold hunters and grave danger."
- N-11: Canonical link: Home https://site.ludus-game.com/, Store https://site.ludus-game.com/store; og:url points to the site; og:image and a favicon are present.
- N-12: At 1280x800 all header items are fully visible and there is no horizontal scroll (checked on the French Store, the longest labels).
- N-13: At 768x1024 (tablet) the header shows the burger and "Login", there is no horizontal scroll, and "Special offers" is a carousel with arrows and dots.

## Facts (LOGGED IN as user {TEST_USER_ID})

New sessions with https://site.ludus-game.com/store?user-id={TEST_USER_ID} and https://site.ludus-game.com/?user-id={TEST_USER_ID}.

- P-01: Opening a page with "?user-id={TEST_USER_ID}" logs in; the address then loses the suffix (https://site.ludus-game.com/store or https://site.ludus-game.com/).
- P-02: Logged-in check: the header shows "Home", "Store", "Reward chain", "Loyalty shop", a gold store points balance ("0"), a teal loyalty points balance ("40") and a green button with a door icon and "Player{TEST_USER_ID}". There is no "Login" button. No popup after login; the cookie banner is shown in a new session.
- P-03: Logged-in Home has no "Special offer" card: the hero is followed directly by the "Check out our Store and shop with profit" banner.
- P-04: Logged-in Referral panel: the same top texts, a read-only field "https://site.ludus-game.com/?referralCode=..." with a green "Copy" button, "No rewards to claim yet", "Make a purchase to get your bonus. Invite friends to receive more rewards." and a "Back to store" button. There is no "Invite friends" or "Log in to view rewards" button.
- P-05: The logged-in Store starts with the "Special offers" carousel ("Small welcome bundle" first, "Previous offer" / "Next offer" arrows). There is no "LUDUS・Official Webshop!" heading, no "Special offer" card and no "Seasonal" section.
- P-06: The logged-in tab bar has only "Free wares" and "Gold".
- P-07: Free wares: "Free emeralds" 100 ("Available weekly: 1/1") and "Free Gold" 500 ("Available daily: 1/1"), both with an enabled green "Claim" button. There is no "Regular cannonballs" card.
- P-08: Reward Chain: "0/1 points", "Step 1 of 8", the first card shows "0/1" instead of its cost; there is no claim button and no "Log in to claim" button.
- P-09: Loyalty shop shows 6 cards ("Astral hero" 1100, "Astral Hero" 550, "Astral Echo" 750, "Legion of Darkness" 550, "Unique Emote" 550, "Unique Avatar" 300), all with an enabled price button. None is affordable with 40 points.
- P-10: Still logged in after Store → Home, after a reload, after switching to "Deutsch" (https://site.ludus-game.com/de-DE/store: "Hauptseite", "Shop", "Belohnungskette", "Treue-Laden", balances and "Player{TEST_USER_ID}"; Free wares "Kostenlose Waren" with "Abholen" buttons) and after switching back to "English" (https://site.ludus-game.com/store).
- P-11: Phone (390x844): header shows the burger, "0", "40" and "Player{TEST_USER_ID}". The burger menu shows the balances, "Player…", "Home", "Store" (yellow), "Reward chain", "Loyalty shop", "Log out" and a "Close" button.

## Not explored (and why)
- Claim buttons, Loyalty shop price buttons, "Invite friends", "Log in to view rewards", "Copy", "Back to store", the phone banner's "Claim": not plain navigation, so not clicked while exploring.
- Logout ("Player{TEST_USER_ID}" on desktop, "Log out" on the phone): not clicked while exploring. settings.md says the desktop "Player{TEST_USER_ID}" button logs out at once with no confirmation.
- All USD price buttons and "Send to friends": they lead to payment (Never).
- External links (app stores, socials, Support, Xsolla, affiliate): only their link targets were read.
- Gift flow: no "Gifts to friends" section when logged in, so it cannot be started with this user.
