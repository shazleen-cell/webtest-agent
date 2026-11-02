# Site map: ludus (https://site.ludus-game.com/)

First explored on 2026-10-28. Explored again on 2026-10-29 (LOGGED OUT and LOGGED IN): F-01 to F-41, P-01 to P-13 and N-01 to N-15 were checked again and still hold unless a note says otherwise. New facts from 2026-10-29: F-42 to F-53 and P-14 to P-21.
Desktop: Chrome 1440x900. Mobile: Chrome mobile emulation 390x844 (iPhone 14 size).
Screenshots (2026-10-29): explore/

## Pages

| # | Page | URL | Screenshot |
|---|------|-----|------------|
| 1 | Home | https://site.ludus-game.com/ | 01-home-cookie-banner, 02-home-middle, 03-home-footer, 06-home-about-carousel |
| 2 | Store (one long page with sections) | https://site.ludus-game.com/store/ | 07 to 13 |
| 3 | Login popup (on any page) | - | 04-login-popup |
| 4 | Referral program panel (on any page) | - | 05-referral-panel |
| 5 | Store and Home in French | https://site.ludus-game.com/fr-FR/store, https://site.ludus-game.com/fr-FR | 14-store-french, 15-home-french-remembered |
| 6 | Unknown page | https://site.ludus-game.com/this-page-does-not-exist | 16-error-page-redirects-home |
| 7 | Mobile home, burger menu, store | same URLs | 17, 18, 19 |
| 8 | LOGGED IN: Store, Home, Referral panel, German Store, mobile | same URLs + ?user-id={TEST_USER_ID} | loggedin-01 to loggedin-09 |

The site has only two real pages (Home and Store). "Reward chain", "Clan reward" and "Loyalty shop" are not separate pages: they are sections of the Store page.

## Facts (LOGGED OUT)

### Home
- F-01: The tab title on Home and Store is "LUDUS - Merge Battle Arena PvP Web Shop".
- F-02: On the first visit a cookie banner is shown: title "How we use cookies", text "We only use essential cookies that allow us to run this service. Read our cookie policy to learn more.", a "cookie policy" link, a "Dismiss" button and a round close (x) icon. After "Dismiss" the banner is gone and is not shown again on later page loads.
- F-03: Home header, left to right: LUDUS logo, "Home", "Store", "Reward chain", "Clan reward", "Loyalty shop", and a green "Login" button on the right. "Home" is shown in yellow (current page).
- F-04: On Home, the header links "Store", "Reward chain", "Clan reward" and "Loyalty shop" all point to https://site.ludus-game.com/store/. Clicking "Clan reward" or "Loyalty shop" on Home opens the Store page at the very top (scroll position 0), not at the matching section.
- F-05: Hero area: big LUDUS logo and three badges: "Download on the App Store" (https://apps.apple.com/ae/app/ludus-strategy-card-rpg-battle/id6446642912), "GET IT ON Google Play" (https://play.google.com/store/apps/details?id=com.studion.mergearena&hl=en&pli=1) and "GET IT ON Web-Version" (https://ludus-game.com/game). All open in a new tab.
- F-06: A "Special offer" card shows a bundle (seen: "URUK BUNDLE", "230%"), "You will get:", item amounts, "Available: 5/5" and a green "Check our store" button that links to https://site.ludus-game.com/store. The bundle content can change.
- F-07: Banner with heading "Check out our Store and shop with profit", text "Buy game resources and Passes at lower prices and make savings with each purchase!" and a green "Check Our Store" button linking to https://site.ludus-game.com/store (target _blank).
- F-08: "Latest news" section with one news card (seen: "v1.38 is live!", "October 15").
- F-09: "About the game" section: a carousel of 5 slides with previous / next arrows, including a YouTube video (not played).
- F-10: "Don’t have the game? Download it today!" section with Google Play, App Store and Web-Version (https://ludus-game.com/) badges.
- F-11: "Follow us in social media!" section with 6 icon links, all in a new tab: YouTube (https://www.youtube.com/@playludus), X/Twitter (https://twitter.com/playludus), TikTok (https://www.tiktok.com/@playludus), Discord (https://discord.gg/5qFQGUXQTD), Instagram (https://www.instagram.com/play.ludus.game), Facebook (https://www.facebook.com/play.ludus).
- F-12: Footer: LUDUS logo, "TOP APP GAMES" logo, a copyright line "© <year> LUDUS", links "Support" (https://help.xsolla.com/), "Powered by Xsolla Web Shop" (https://xsolla.com/mobile-web-shop?...), "Join Affiliate Program" (https://influencer.xsolla.com/...), all in a new tab, a "Privacy settings" button and a blue language button "EN".
- F-13: The language selector has 15 options: English, Français, Deutsch, Español, Português, Italiano, Türkçe, 한국어, 日本語, 繁體中文, 简体中文, Русский, Tiếng Việt, ไทย, Bahasa Indonesia.
- F-14: Choosing "Français" opens https://site.ludus-game.com/fr-FR (html lang "fr"). The header becomes "Accueil", "Boutique", "Chaîne de récompenses", "Récompense de clan", "Boutique de fidélité" and the button "Connexion". "Special offer" becomes "Offre spéciale", "Referral program" becomes "Programme de parrainage".
- F-15: The chosen language is remembered: after choosing Français, opening https://site.ludus-game.com/ goes to https://site.ludus-game.com/fr-FR.
- F-16: Possible bug: the news card date is "October 15" in English but "10 mars" (10 March) in French for the same "v1.38" news.
- F-17: A floating white "Referral program" button is shown bottom right on every page. It opens a panel: "Invite friends — get bonuses together!", "Bring friends and enjoy bonuses when they make first purchases. Your friends will also get rewards.", "You will get:" "Emeralds x100, Gold x1000", "Your friend will get:" "Emeralds x650, Gold x10000", an "Invite friends" button, "My rewards" and a "Log in to view rewards" button. While the panel is open, the floating button becomes a close (X) button and clicking it closes the panel.
- F-18: At 1440x900 the top of the Referral panel is cut off above the window (the "Invite friends —" line is only half visible).
- F-19: The "Login" button opens a popup titled "Log in to make purchases" (shown in capitals) with a QR code and a red close (x) button. Closing it returns to the page.

### Store
- F-20: Store header: LUDUS logo, "Home", "Store", "Reward chain", "Loyalty shop", green "Login". There is NO "Clan reward" item on the Store page (desktop and mobile), although Home has one. On the Store page "Store", "Reward chain" and "Loyalty shop" are buttons that scroll the page; the active one is yellow.
- F-21: Store top: heading "LUDUS・Official Webshop" and text "Enjoy lower prices - buy game resources and passes much cheaper!", then the "Special offer" card with a price button "USD 54.00" plus a struck-through old price "59.99" and two point badges.
- F-22: "Special offers" section: "Small welcome bundle", "Medium welcome bundle", "Big welcome bundle", each with "Available: 1/1" and a USD price. Then a "Seasonal" section with "Limited time" cards and countdown timers.
- F-23: "Store" section with a tab bar: "Free wares", "Battle Passes", "Licenses", "Might Passes", "Ludus Royal", "Ethereal Crystals", "Spells", "Runes", "Dice of Fortune", "Gold", "Emeralds", "Gift to friends". "Free wares" is yellow at first. At 1440 wide the last tab is cut off at the right edge (only "Gift" is visible).
- F-24: Clicking a tab (for example "Gold") scrolls to that category. "Gold" has 5 cards: "Small pile of gold" (5000), "Piggy bank of gold" (25000), "Carpetbag of gold" (60000), "Goblet of gold" (140000), "Strongbox of gold" (350000), each with a green USD price button and a struck-through old price (for example "USD 2.88" and "3.20").
- F-25: "Free wares": "Free emeralds" 100, "Available weekly: 1/1", green "Claim" button; "Free Gold" 500, "Available daily: 1/1", green "Claim" button. Claim was not clicked.
- F-26: "Emeralds": "Small pile of emeralds", "Pouch of emeralds", "Sack of emeralds", "Chest of emeralds", "Pot of emeralds", each with a "1st purchase" label and "Available: 1/1". Below it is a "Log in to see more offers" button.
- F-27: (the number of cards changes: 10 on 2026-10-28/29, 8 on 2026-10-30 after the limited-time Clan Competition tickets ended and two Astral Key tickets were added) "Gifts to friends" section with the ribbon "Buy Tickets as gifts for your friends and fellow Clan members!" and 10 ticket cards (first: "Tournament Diamond Ticket"), each with a "Gift" badge, "Send to friends" and a USD price button.
- F-28: The header "Reward chain" scrolls to the "Rewards Market" section: "Limited time" with a countdown, text "Make purchases, earn Store points, and claim cool rewards! More purchases mean more Store points. Gotta claim them all!", "0/500 points", "Step 1 of 10", a row of reward cards with point costs, carousel arrows and dots, and a green "Login to claim" button.
- F-29: The header "Loyalty shop" scrolls to the "Loyalty Shop" section: 12 cards, each with a name, amount, an "Available weekly: x/y" or "Available: x/y" line and a green button with a point price (for example "Astral Echo" 750, "Unique Avatar" 300). Some cards have a countdown.
- F-30: Possible content bug: two Loyalty Shop cards have almost the same name: "Astral hero" (1100) and "Astral Hero" (550).
- F-31: "Don't have the game? Download it today!" section with Google Play, App Store and Web-Version badges.
- F-32: "FAQ" section with 6 questions: "How does purchasing from Web Shop benefit me?", "Is it safe to purchase on Web Shop?", "Who can help me with my purchase issue?", "What payment methods does Web Shop support?", "How to make a purchase?", "What's a referral program?". Clicking the first opens the answer "In Web Shop, you can purchase game items at lower prices, find some special offers, and claim free rewards. ..." and the arrow points up.
- F-33: Store footer: game app icon, 6 social icon buttons (YouTube, X, TikTok, Discord, Instagram, Facebook), LUDUS and TOP APP GAMES logos, copyright line, "Support", "Powered by Xsolla Web Shop", "Join Affiliate Program", "Privacy settings", "EN" language button.
- F-34: The browser console shows 404 errors for https://site.ludus-game.com/store/manifest.json and some store.xsolla.com offer_chain requests (not visible to users).

### Error page
- F-35: https://site.ludus-game.com/this-page-does-not-exist answers 404 ("Page Not Found" title for a moment) and then shows the Home page at https://site.ludus-game.com/. No error message is shown.

### Mobile (390x844)
- F-36: Mobile header: green burger button, LUDUS logo, green "Login" button. The page has no horizontal scroll.
- F-37: The cookie banner is shown on mobile too, with the "Dismiss" button.
- F-38: On mobile a bottom banner is shown: app icon, "Add It to Home Screen", "To got a quicker access !" (typo), a green "Claim" button and an X ("Close pwa banner"). The X closes it. The banner's "Claim" was not clicked.
- F-39: The burger menu shows the LUDUS logo, a red close (x) button and "Home" (yellow), "Store", "Reward chain", "Clan reward", "Loyalty shop", then "Login".
- F-40: Mobile Store: the tab bar scrolls sideways (first visible: "Free wares", "Battle Passes", "Licenses", "Might Pass..."), cards are 2 per row. The Store burger menu has no "Clan reward" (same as F-20).
- F-41: On mobile the floating "Referral program" button shows only its icon.

## Facts (LOGGED IN as user {TEST_USER_ID})

Explored on 2026-10-28 with https://site.ludus-game.com/store/?user-id={TEST_USER_ID} in a new session. Screenshots: explore/loggedin-*.

- P-01: Opening a page with "?user-id={TEST_USER_ID}" logs in. The address then changes to the page without the suffix (https://site.ludus-game.com/store/).
- P-02: Logged-in check: the header shows a teal loyalty-points balance ("200" on 2026-10-28, "40" on 2026-10-29, see P-14), a gold store-points balance ("0") and a green button with a door icon and "Player{TEST_USER_ID}". There is no "Login" button.
- P-03: No popup is shown after login. The "How we use cookies" banner is still shown in a new session.
- P-04: Clicking the green "Player{TEST_USER_ID}" button on desktop logs out at once, with no confirmation: the header shows "Login" again and the Rewards Market shows "Login to claim". (Found by accident while exploring; logging back in with the link worked.)
- P-05: (still true 2026-10-29, but see P-17 for Special offers) Logged-in Store tab bar has only "Free wares", "Might Passes" and "Gold" (12 tabs when logged out). There is no "Seasonal" section, no "Emeralds", no "Gifts to friends" section and no "Log in to see more offers" button.
- P-06: The "Might Passes" category says "The store is empty for now. Come back later!" but its tab is still shown.
- P-07: (2026-10-28, changed: see P-15) Free wares: "Free emeralds" 100, "Available weekly: 1/1", green "Claim" (enabled); "Free Gold" 500, "Available daily: 1/1", green "Claim" (enabled). Both can be claimed now. Not clicked.
- P-08: Rewards Market: "0/500 points", "Step 1 of 10", first card "5000" shows "0/3" instead of a point cost, no "Login to claim" button and no claim button. Nothing can be claimed (0 store points).
- P-09: (2026-10-28, changed: see P-16) Loyalty Shop shows 7 cards (12 when logged out), prices in loyalty points (teal icon): "Astral hero" 1100 (Available weekly: 1/1), "Astral Hero" 550 (Available weekly: 2/2, countdown), "Astral Echo" 750, "Magical Order" 550 (countdown), "Unique Emote" 550 (Available: 1/1), "Unique Avatar" 300 (Available: 1/1), "Unique Frame" 160 (Available: 1/1). All 7 price buttons are enabled, even the ones above the 200 balance. Only "Unique Frame" (160) is affordable. Not clicked.
- P-10: Logged-in Home: header "Home", "Store", "Reward chain", "Clan reward", "Loyalty shop", the two balances and "Player{TEST_USER_ID}". The "Special offer" card is not shown on Home when logged in; the hero is followed directly by the "Check out our Store" banner.
- P-11: Still logged in after a reload, after going Store → Home, and after switching to Français (https://site.ludus-game.com/fr-FR shows the balances and "Player{TEST_USER_ID}") and back to English.
- P-12: Phone (390x844): header has burger, logo, balances "200" and "0", and the player button cut to "Play…". The burger menu shows the balances, the "Play…" button, "Home", "Store", "Reward chain", "Loyalty shop" and "Logout" (no "Clan reward" on the Store page).
- P-13: No clan reward section was found when logged in either, and the "Gifts to friends" section is missing, so the gift flow cannot be tested with this user.

## New facts from 2026-10-29 (LOGGED OUT)

- F-42: The header stays fixed at the top of the window while scrolling (Home and Store).
- F-43: Pressing Escape closes the "Log in to make purchases" popup.
- F-44: The footer button "Privacy settings" opens the "How we use cookies" banner again. The banner's round close (x) icon closes it. The "cookie policy" link points to https://xsolla.com/cookie (new tab).
- F-45: On the Store page (logged out), "Login to claim" in the Rewards Market opens the "Log in to make purchases" popup.
- F-46: "About the game" carousel: slide 1 of 5 is a YouTube video; the next arrow moves to slide 2 / 5. The Rewards Market carousel has previous / next arrows; the next arrow moves the reward cards.
- F-47: FAQ: "Who can help me with my purchase issue?" opens "If you need assistance with your purchase or wish to request a refund, contact Xsolla Customer Support." (no link). Clicking an open question again closes it. "What's a referral program?" opens "After you make a purchase, you can invite your friends using your personal referral code. ..."
- F-48: Choosing "Français" on the Store page opens https://site.ludus-game.com/fr-FR/store: header "Accueil", "Boutique", "Chaîne de récompenses", "Boutique de fidélité", "Connexion"; heading "LUDUS・Jeu de combat stratégique en JcJ・Boutique en ligne officielle". The tab title stays "LUDUS - Merge Battle Arena PvP Web Shop". The French sub-heading says "10 % moins chers" while the English one says "much cheaper".
- F-49: Choosing "English" on https://site.ludus-game.com/fr-FR opens https://site.ludus-game.com/ (header "Home", "Store", ...).
- F-50: Store footer social links have accessible names ("Open https://www.youtube.com/@playludus" and so on); the Home social icons have none (see N-08).
- F-51: Mobile: the cookie banner appears about 1-2 s after the page loads. Its "Dismiss" button is partly covered by the "Add It to Home Screen" banner and the floating Referral button, but a click on it still works.
- F-52: Mobile: after closing the "Add It to Home Screen" banner with its X on Home, it is not shown again on Store in the same session.
- F-53: Mobile: the red close (x) of the burger menu closes the menu. It is a plain element with no button role and no accessible name.
- (Also seen) Home has a hidden h2 "Your game title" (placeholder text, not visible on screen).

## New facts from 2026-10-29 (LOGGED IN as user {TEST_USER_ID})

- P-14: Header balances: loyalty points "40" (teal), store points "0" (gold). Yesterday it was 200 loyalty points, so 160 points were spent in the 2026-10-28 test run (the 160-point "Unique Frame" is gone from the Loyalty Shop).
- P-15: Free wares: "Free emeralds" 100 shows "Available in 3d 16h" and a green text "Claimed" (no Claim button). "Free Gold" 500 shows "Available daily: 1/1" and an enabled green "Claim" button. Not clicked.
- P-16: Loyalty Shop shows 6 cards: "Astral hero" 1100 (Available weekly: 1/1), "Astral Hero" 550 (Available weekly: 2/2, countdown), "Astral Echo" 750 (Available weekly: 1/1), "Magical Order" 550 (Available weekly: 1/1, countdown), "Unique Emote" 550 (Available: 1/1), "Unique Avatar" 300 (Available: 1/1). All 6 price buttons are enabled, but none is affordable with 40 points. Not clicked.
- P-17: The logged-in Store shows the "Special offer" card (USD price, points badges 50 and 550) and the "Special offers" section (Small / Medium / Big welcome bundle, each "Available: 1/1"). There is no "Seasonal" section. Rewards Market is the same as P-08.
- P-18: Logged-in Referral panel: same top texts as logged out, then a read-only field with "https://site.ludus-game.com/?referralCode=..." and a green "Copy" button, "No rewards to claim yet", "Make a purchase to get your bonus. Invite friends to receive more rewards." and a "Back to store" button. There is no "Invite friends" or "Log in to view rewards" button.
- P-19: Switching to "Deutsch" keeps the login: https://site.ludus-game.com/de-DE/store shows "Startseite", "Shop", "Belohnungskette", "Treue-Shop", the balances and "Player{TEST_USER_ID}". In German the Free Gold button says "Kostenlos" and the Free emeralds card says "Beansprucht".
- P-20: Switching back to "English" opens https://site.ludus-game.com/store and the user is still logged in.
- P-21: Phone (390x844) login with the suffix: the cookie banner and the "Add It to Home Screen" banner are shown; the header shows the burger, logo, "40", "0" and "Play…"; the burger menu shows the balances, "Play…", "Home", "Store" (yellow), "Reward chain", "Loyalty shop" and "Logout".

## Non-functional facts (LOGGED OUT)

Measured on 2026-10-28 in a new Chrome session (no cache) unless noted. On 2026-10-29 N-03, N-06, N-11, N-12 and N-13 were checked again and still hold.

- N-01: (2026-10-29 run: load event 21.1 s; 2026-10-30 run: first contentful paint 0.9 s, load event 2.5 s. Timing depends on the network.) Home timing (first visit): time to first byte 1.0 s, first contentful paint 1.8 s, DOMContentLoaded 2.7 s, load event 7.5 s; 142 resource requests.
- N-02: Store (same session, cache warm): first contentful paint 0.7 s, load event 1.0 s; 250 resource requests and 321 images.
- N-03: Failed requests: Home and Store both log 404s, for example store.xsolla.com/api/v2/project/253824/items/bundle/group, Store also site.ludus-game.com/store/manifest.json and store.xsolla.com/.../user/offer_chain/1511.
- N-04: No broken images (every loaded image has a size) on Home and Store.
- N-05: http://site.ludus-game.com/store/ redirects to https://site.ludus-game.com/store/. No resources are loaded over http (no mixed content).
- N-06: Response headers of the page: Strict-Transport-Security "max-age=63072000; includeSubDomains; preload" is present. Content-Security-Policy, X-Frame-Options, X-Content-Type-Options, Referrer-Policy and Permissions-Policy are all missing.
- N-07: html lang is "en" on the English page and "fr" on /fr-FR.
- N-08: Home: 17 images, 2 with no alt attribute; 14 links with no accessible name (logo, App Store / Google Play / Web-Version badges, 6 social icons); 8 buttons with no accessible name.
- N-09: Store: 321 images, 46 with no alt attribute; 13 buttons with no accessible name; no h1 heading (Home has one h1: "Check out our Store and shop with profit").
- N-10: Keyboard: Tab reaches the cookie banner "Dismiss" button and Enter closes the banner. Header menu items get focus with Tab but have outline "none" and no box shadow (no clear focus ring).
- N-11: The viewport meta tag is "width=device-width,initial-scale=1,maximum-scale=1,shrink-to-fit=no": maximum-scale=1 stops pinch zoom on phones.
- N-12: Meta description and og:description are placeholder text: "Your Game takes players on a grand adventure filled with detractors, monsters, gold hunters and grave danger."
- N-13: The canonical link and og:url point to https://ludus-merge-battle-arena-pvp-landing.xsolla.site/ instead of https://site.ludus-game.com/. og:image (1200x630) and a favicon are present.
- N-14: At 1280x800 all header items (Home, Store, Reward chain, Clan reward, Loyalty shop, Login) are fully visible and there is no horizontal scroll.
- N-15: At tablet size 768x1024 (iPad user agent) the header switches to burger + logo + Login, there is no horizontal scroll, and the page content fits.

## Not explored (and why)
- Claim buttons, loyalty point buttons, "Login to claim", "Log in to see more offers", "Invite friends", "Log in to view rewards", the mobile "Claim" (add to home screen): not plain navigation, so not clicked while exploring.
- All USD price buttons and "Send to friends": they lead to payment (Never).
- External links (app stores, socials, Support, Xsolla, affiliate): only their link targets were read.
- LOGGED IN: Claim, loyalty point buttons and Logout were not clicked on purpose (the one logout in P-04 was an accident). Session length was not measured.
- 2026-10-29: Loyalty Shop price buttons and Claim buttons were not clicked while logged out either ("Allowed when LOGGED OUT" does not list them). The "Copy" button in the logged-in Referral panel was not clicked.
