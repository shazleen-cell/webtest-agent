# Site map: ludus (https://site.ludus-game.com/)

Explored 2026-11-24 in Chrome 1440x900 (desktop) and an iPhone 14 view (390x844, DPR 3, mobileEmulation).
Screenshots: website-tests/ludus/explore/ (git-ignored). The test user is written as {TEST_USER_ID}.

## Pages

| # | URL | Tab title | Notes |
|---|-----|-----------|-------|
| 1 | https://site.ludus-game.com/ | LUDUS - Merge Battle Arena PvP Web Shop | Home |
| 2 | https://site.ludus-game.com/store | LUDUS - Merge Battle Arena PvP Web Shop | Store (one long page with all shop sections) |
| 3 | https://site.ludus-game.com/store#loyalty-shop | (same page) | Header "Loyalty shop" link scrolls to the Loyalty shop section |
| 4 | https://site.ludus-game.com/de-DE | LUDUS - Merge Battle Arena PvP Web Shop | Home in German (any language: /<locale>, /<locale>/store) |
| 5 | https://site.ludus-game.com/fr-FR | LUDUS - Merge Battle Arena PvP Web Shop | Home in French (LOGGED IN check) |
| 6 | https://site.ludus-game.com/this-page-does-not-exist | "Page Not Found" for a moment | answers 404, then shows Home at / |

Popups: Login ("Log in to make purchases"), News, Referral program panel, burger menu (phone), cookie banner.
External links (never opened): App Store, Google Play, Web-Version (ludus-game.com), YouTube, Twitter, TikTok, Discord, Instagram, Telegram, Facebook, Support (help.xsolla.com), Powered by Xsolla Web Shop, Join Affiliate Program (x.la/xpn).

## LOGGED OUT facts

- F-01 Home: tab title "LUDUS - Merge Battle Arena PvP Web Shop", `<html lang="en">`, canonical https://site.ludus-game.com/, og:title the same as the title. The page has no H1 heading. Meta description is "Your Game takes players on a grand adventure filled with detractors, monsters, gold hunters and grave danger." (generic template text, not about Ludus).
- F-02 Cookie banner on every new session (desktop and phone): heading "How we use cookies", text "We only use essential cookies that allow us to run this service. Read our cookie policy to learn more.", a "cookie policy" link, a "Dismiss" button and a round close icon. "Dismiss" closes it.
- F-03 Header on Home (LOGGED OUT): LUDUS logo (link to /), "Home" (yellow, current page), "Store", green "Login" button on the right. Header on Store: "Home", "Store" (yellow), "Loyalty shop", "Login".
- F-04 Home hero: big LUDUS logo and three badges: "Download on the App Store" (apps.apple.com, new tab), "GET IT ON Google Play" (play.google.com, new tab), "GET IT ON Web-Version" (ludus-game.com/game, new tab).
- F-05 Home "Special offer" card (LOGGED OUT): ribbon "Special offer", "230%" badge, "URUK BUNDLE", "Your chance to snatch a unique Astral hero!", "You will get:" 6 / 2000 / 100000, "Available: 5/5", loyalty points 550, and a green "Check our store" button (to /store). There is no price button on Home.
- F-06 Home block "Check out our Store and shop with profit" with text "Buy game resources and Passes at lower prices and make savings with each purchase!" and a green "To the store" button (to /store).
- F-07 "Latest news": two cards, "The Clan Competition is about to start!" (November 10) and "v1.38 is live!" (October 15). Clicking a card opens a "News" popup with an image, the title, the date and the full text, and a white X close button.
- F-08 "About the game": a video with a "Play video" button, a carousel with "Previous" / "Next" arrows and five dots ("Go to slide 1" to "Go to slide 5"). "Next" moves to slide 2 (the second dot becomes the long one).
- F-09 "Don't have the game? Download it today!": three badges (Home: Google Play, App Store, Web-Version).
- F-10 "Follow us in social media!": 7 icon links: YouTube (@playludus), Twitter (playludus), TikTok (@playludus), Discord (discord.gg), Instagram (play.ludus.game), Telegram (t.me/playludusglobal), Facebook (play.ludus).
- F-11 Footer: "© 2026 LUDUS", "Support" (help.xsolla.com), "Powered by Xsolla Web Shop", "Join Affiliate Program" (x.la/xpn), "Privacy settings" button, language selector "EN".
- F-12 Language selector: 15 languages in this order: English, Français, Deutsch, Español, Português, Italiano, Türkçe, 한국어, 日本語, 繁體中文, 简体中文, Русский, Bahasa Indonesia, Tiếng Việt, ไทย.
- F-13 Choosing "Deutsch" opens https://site.ludus-game.com/de-DE, `lang="de"`, header "Hauptseite", "Shop", "Anmelden"; Home shows "Sonderangebot", "URUK-PAKET", "Du erhältst:", "Verfügbar: 5/5", "Besuche unseren Shop", "Referral-Programm"; selector shows "DE". The choice is remembered: opening https://site.ludus-game.com/ afterwards goes to /de-DE until English is chosen again.
- F-14 "Referral program" button (white, bottom right, on every page). It opens a panel: "Invite friends — get bonuses together!", "Bring friends and enjoy bonuses when they make first purchases. Your friends will also get rewards.", "You will get:" "Emeralds x100, Gold x1000" ×1, "Your friend will get:" "Emeralds x650, Gold x10000" ×1, a green "Invite friends" button, "My rewards" with "Log in to view rewards". The button turns into a round X that closes the panel. At 1440x900 the top of the panel touches the top of the window and the heading is partly cut off.
- F-15 "Login" button opens a dialog "LOG IN TO MAKE PURCHASES", "Scan the QR code with your mobile device", a QR code, and a red X close button. X closes it.
- F-16 Store top: "LUDUS・Official Webshop!", "Enjoy lower prices - buy game resources and passes much cheaper!", and the "Special offer" URUK BUNDLE card, here with a green price button "USD 54.00" (old price 59.99 struck through), points 50 and loyalty points 550.
- F-17 Store headings in order (LOGGED OUT): Special offers, Seasonal, Store, Free wares, Battle Passes, Gifts to friends, Licenses, Might Passes, Ludus Royal, Ethereal Crystals, Spells, Runes, Dice of Fortune, Gold, Emeralds, Reward Chain, Loyalty shop, Don't have the game? Download it today!, FAQ.
- F-18 Under the "Store" heading a tab bar: Free wares, Battle Passes, Gifts to friends, Licenses, Might Passes, Ludus Royal, Ethereal Crystals, Spells, Runes, Dice of Fortune, Gold, Emeralds, with a "More categories" arrow on the right (and "Previous categories" on the left after scrolling). The current tab is yellow. Clicking "Runes" scrolls the page to the "Runes" heading and makes "Runes" yellow; the tab bar then sticks below the header. The URL stays /store.
- F-19 Every paid card shows its name, an amount, a points badge, a loyalty points badge and a green price button with the USD price and the old price struck through. The whole card is also clickable (never click it).
- F-20 Free wares (LOGGED OUT): "Free emeralds" 100 ("Available weekly: 1/1", countdown), "Free Gold" 500 ("Available daily: 1/1"), "Atlantis Tokens" 50 ("Available daily: 1/1"), each with a green "Claim" button.
- F-21 Reward Chain: "Reward system" with the text "Reward system adds a layer of motivation and enjoyment to the gaming experience, …", "0/3 points", "Step 1 of 10", 10 progress bars, reward tiles (5000, 15, 1, 50, 2, 25000, 1, 20, 5000, 3) with point targets (3, 5, 10, 30, 50, 70, 100, 200, 350, 500), a green "Log in to claim" button and a "Limited time" ribbon with a countdown.
- F-22 Loyalty shop (LOGGED OUT), 13 cards with green buttons priced in loyalty points: Astral Hero 550 (Available weekly: 2/2), Astral Hero 550 (2/2), Astral hero 1100, Astral Echo 750, Outlaws 550, Unique Emote 550 (Available: 1/1), Unique Avatar 300, Unique Frame 160, Spell chest 650, Essence Bundle 180 (3/3), Small pile of Golden Runes 240, Barrel of Runes 350 (2/2), Handful of dice 160 (3/3).
- F-23 Header "Loyalty shop" (on Store) scrolls to the "Loyalty shop" section and turns yellow.
- F-24 FAQ: six questions, all closed: "How does purchasing from Web Shop benefit me?", "Is it safe to purchase on Web Shop?", "Who can help me with my purchase issue?", "What payment methods does Web Shop support?", "How to make a purchase?", "What's a referral program?". Clicking "Is it safe to purchase on Web Shop?" opens the answer "Web Shop is provided by our partner Xsolla. Xsolla is PCI DSS Level 1 …" and the arrow turns up.
- F-25 Store "Don't have the game? Download it today!" badges: Google Play, App Store, Web-Version (ludus-game.com).
- F-26 Unknown page /this-page-does-not-exist: the server answers 404 (tab title "Page Not Found" for a moment), then the Home page is shown at https://site.ludus-game.com/. No error message is shown.
- F-27 Phone (390x844): header with a green burger button (no accessible name) and "Login". Burger opens a menu with the logo, "Home", "Store", "Login" and a red X; on /store the menu also has "Loyalty shop". "Store" in the menu opens /store. No horizontal scrolling (page width 390).
- F-28 Phone: a bottom bar "Add It to Home Screen" / "To got a quicker access !" with an app icon, a green "Claim" button and an X ("Close pwa banner"). The second line has a spelling mistake ("To got"). The "Claim" is an install prompt, not a reward.
- F-29 Store failed requests (LOGGED OUT): 404 on store.xsolla.com/api/v2/project/253824/user/offer_chain/1310, /1511 and /1512.
- F-30 Home timing: DOMContentLoaded about 0.3 s, load about 0.5 s. HTTPS. All 40 images have an alt attribute.
- F-31 Once, opening https://site.ludus-game.com/ answered "504 Gateway Time-out"; opening it again worked.

### Real-money price buttons seen LOGGED OUT (Step 2.4; prices are the current USD price shown)

| Section | Item | Price |
|---|---|---|
| Special offer (Store top) | URUK BUNDLE | USD 54.00 |
| Special offers | Small welcome bundle | USD 5.40 |
| Special offers | Medium welcome bundle | USD 54.00 |
| Special offers | Big welcome bundle | USD 108.00 |
| Seasonal | Atlantis Ruby Permit | USD 32.40 |
| Seasonal | Atlantis Super Permit | USD 43.20 |
| Seasonal | Atlantis Sapphire Permit | USD 10.80 |
| Seasonal | Atlantis Diamond Ticket | USD 32.40 |
| Seasonal | Atlantis Golden Ticket | USD 10.80 |
| Battle Passes | Atlantis Diamond Ticket | USD 32.40 |
| Battle Passes | Atlantis Golden Ticket | USD 10.80 |
| Battle Passes | Double Seal | USD 18.00 |
| Battle Passes | Runes Seal | USD 10.80 |
| Battle Passes | Heroes Seal | USD 10.80 |
| Battle Passes | Tournament Diamond Ticket | USD 21.60 |
| Battle Passes | Tournament Golden Ticket | USD 10.80 |
| Battle Passes | Battle Pass Diamond Ticket | USD 43.20 |
| Battle Passes | Battle Pass Golden Ticket | USD 10.80 |
| Battle Passes | Clan War Diamond Ticket | USD 32.40 |
| Battle Passes | Clan War Golden Ticket | USD 16.20 |
| Gifts to friends | Tournament Diamond Ticket | USD 21.60 |
| Gifts to friends | Tournament Golden Ticket | USD 10.80 |
| Gifts to friends | Clan War Golden Ticket | USD 16.20 |
| Gifts to friends | Clan War Diamond Ticket | USD 32.40 |
| Gifts to friends | Battle Pass Diamond Ticket | USD 32.40 |
| Gifts to friends | Battle Pass Golden Ticket | USD 10.80 |
| Licenses | Divisions License x4 | USD 21.60 |
| Licenses | Divisions License | USD 7.65 |
| Licenses | Atlantis Super Permit | USD 43.20 |
| Licenses | Atlantis Ruby Permit | USD 32.40 |
| Licenses | Atlantis Sapphire Permit | USD 10.80 |
| Might Passes | Might Pass 1000% | USD 21.60 |
| Might Passes | Might Pass 500% | USD 16.20 |
| Might Passes | Might Pass 250% | USD 10.80 |
| Might Passes | Might Pass 120% | USD 5.40 |
| Might Passes | Might Pass 0% | USD 2.25 |
| Ludus Royal | Ludus Royal for 30 days | USD 10.80 |
| Ludus Royal | Ludus Royal for 10 days | USD 5.40 |
| Ethereal Crystals | A Casket of Crystals | USD 15.05 |
| Ethereal Crystals | A Tub of Crystals | USD 41.92 |
| Spells | Earth Essense | USD 6.43 |
| Spells | Water Essense | USD 6.43 |
| Spells | Fire Essense | USD 6.43 |
| Runes | Horn of Runes | USD 4.12 |
| Runes | Barrel of Runes | USD 9.99 |
| Runes | Chest of Runes | USD 18.07 |
| Runes | Wagon of Runes | USD 32.89 |
| Runes | Longship of Runes | USD 58.72 |
| Runes | Small pile of Golden Runes | USD 10.71 |
| Runes | Crate of Golden Runes | USD 18.07 |
| Runes | Cauldron of Golden Runes | USD 31.60 |
| Dice of Fortune | Handful of dice | USD 5.40 |
| Dice of Fortune | Bowl of dice | USD 13.39 |
| Dice of Fortune | Heap of dice | USD 38.70 |
| Gold | Small pile of gold | USD 2.88 |
| Gold | Piggy bank of gold | USD 10.71 |
| Gold | Carpetbag of gold | USD 20.07 |
| Gold | Goblet of gold | USD 38.70 |
| Gold | Strongbox of gold | USD 73.40 |
| Emeralds | Small pile of emeralds | USD 5.40 |
| Emeralds | Pouch of emeralds | USD 10.80 |
| Emeralds | Sack of emeralds | USD 21.60 |
| Emeralds | Chest of emeralds | USD 54.00 |
| Emeralds | Pot of emeralds | USD 108.00 |

## LOGGED IN facts (test user {TEST_USER_ID})

- P-01 Opening https://site.ludus-game.com/store?user-id={TEST_USER_ID} logs in. The suffix disappears from the address bar. After about 3 seconds the header shows a loyalty points badge (40) and a green button with a door icon and "Player{TEST_USER_ID}", and no "Login" button. No popup after login. The cookie banner is shown in the new session (closed first).
- P-02 Header LOGGED IN on Store: logo, "Home", "Store" (yellow), "Loyalty shop", loyalty points badge, player-name button. On Home: logo, "Home", "Store", badge, player-name button.
- P-03 Store headings LOGGED IN: Special offers, Store, Free wares, Gold, Reward Chain, Loyalty shop, Don't have the game? Download it today!, FAQ. Tab bar: "Free wares", "Gold" only. No URUK BUNDLE card at the top.
- P-04 Special offers LOGGED IN is a carousel showing one card at a time with white left/right arrows: Small welcome bundle (15000, 300, 1, 1; "Available: 1/1"; "460%"; points 5, loyalty 55; "USD 5.40"), Medium welcome bundle ("USD 54.00"), Big welcome bundle ("USD 108.00").
- P-05 Gold LOGGED IN: Small pile of gold USD 2.88, Piggy bank of gold USD 10.71, Carpetbag of gold USD 20.07, Goblet of gold USD 38.70, Strongbox of gold USD 73.40.
- P-06 Free wares LOGGED IN: "Free emeralds" 100 and "Free Gold" 500 only (no "Atlantis Tokens"). Both showed "Claimed" (green text) and "Available in 5d 8h" / "Available in 8h 53m"; no Claim button at that time.
- P-07 Reward Chain LOGGED IN: "0/3 points", "Step 1 of 10", first tile shows "0/3"; no "Log in to claim" button and no Claim button.
- P-08 Loyalty shop LOGGED IN: 7 cards: Astral Hero 550 (Available weekly: 2/2), Astral Hero 550 (2/2), Astral hero 1100 (1/1), Astral Echo 750 (1/1), Outlaws 550 (1/1), Unique Emote 550 (Available: 1/1), Unique Avatar 300 (Available: 1/1). The badge shows 40, fewer than the cheapest card (300). Not clicked during exploration.
- P-09 Home LOGGED IN: no "Special offer" URUK BUNDLE card; the first block under the hero is "Check out our Store and shop with profit" with "To the store".
- P-10 Still logged in after reloading /store without the suffix, after "Home" in the header, and after switching the language to Français (/fr-FR, header "Accueil", "Boutique", badge 40, player button, "Programme de parrainage").
- P-11 Phone LOGGED IN: header with the burger button, badge 40 and the player button. The burger menu shows the badge, a green "Player..." button (name cut off), "Home", "Store" (yellow on /store), "Loyalty shop", "Log out" and a red X.
- P-12 Shown LOGGED OUT but hidden LOGGED IN for this account: the URUK BUNDLE "Special offer", Seasonal, Battle Passes, Gifts to friends (so the gift flow is not reachable), Licenses, Might Passes, Ludus Royal, Ethereal Crystals, Spells, Runes, Dice of Fortune, Emeralds, the "Atlantis Tokens" free card and 6 Loyalty shop cards (Unique Frame, Spell chest, Essence Bundle, Small pile of Golden Runes, Barrel of Runes, Handful of dice).
- P-13 Failed requests LOGGED IN: 404 on store.xsolla.com/api/v2/project/253824/user/reward_chain/2137/balance, /3453/balance, /3521/balance (repeated), and 404 on site.ludus-game.com/navigation.json/navigation.json (also /fr-FR/navigation.json/navigation.json).

### Real-money price buttons seen LOGGED IN (Step 2.9)

| Section | Item | Price |
|---|---|---|
| Special offers (carousel) | Small welcome bundle | USD 5.40 |
| Special offers (carousel) | Medium welcome bundle | USD 54.00 |
| Special offers (carousel) | Big welcome bundle | USD 108.00 |
| Gold | Small pile of gold | USD 2.88 |
| Gold | Piggy bank of gold | USD 10.71 |
| Gold | Carpetbag of gold | USD 20.07 |
| Gold | Goblet of gold | USD 38.70 |
| Gold | Strongbox of gold | USD 73.40 |
