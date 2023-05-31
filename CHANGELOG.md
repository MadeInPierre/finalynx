# Changelog

<!--next-version-placeholder-->

## v1.18.1 (2023-05-31)
### Fix

* **fetch:** Skip malformed realt lines for now ([`3b55c43`](https://github.com/MadeInPierre/finalynx/commit/3b55c4305d2eab2c1c8a7f862be05da4a8426eeb))

## v1.18.0 (2023-05-31)
### Feature

* **fetch:** Add new RealT fetch source ([#106](https://github.com/MadeInPierre/finalynx/issues/106)) ([`ca00549`](https://github.com/MadeInPierre/finalynx/commit/ca0054980026980368da1addbc05f2e6dc5f6b4a))

## v1.17.0 (2023-05-30)
### Feature

* **console:** Add support for light/dark/custom console themes ([#115](https://github.com/MadeInPierre/finalynx/issues/115)) ([`7722e29`](https://github.com/MadeInPierre/finalynx/commit/7722e296ec0f869469ca39e97848b88d426d941c))

## v1.16.3 (2023-05-27)
### Fix
* **delta:** Align deltas when showing portfolio root ([`cb20954`](https://github.com/MadeInPierre/finalynx/commit/cb20954e2b6dfaea56c31394f58f4f977c647109))

## v1.16.2 (2023-05-26)
### Fix
* **fetch:** Spinner was hiding user prompts ([`8c5a78f`](https://github.com/MadeInPierre/finalynx/commit/8c5a78fc8df7e781783c1877b29b25589fe14bc3))

## v1.16.1 (2023-05-26)
### Performance
* **finary:** Fetch all finary investments in only one call ([`f119c49`](https://github.com/MadeInPierre/finalynx/commit/f119c49967f8fc20dc591f1525a678e024cfabe3))

## v1.16.0 (2023-05-26)
### Feature
* Add startup for exotic investiment in constant file ([#100](https://github.com/MadeInPierre/finalynx/issues/100)) ([`598f0e0`](https://github.com/MadeInPierre/finalynx/commit/598f0e0a026080e30de8c43e4b778e4bd80600ef))
* **fetch:** Add support for multiple fetch sources ([#97](https://github.com/MadeInPierre/finalynx/issues/97)) ([`903fc23`](https://github.com/MadeInPierre/finalynx/commit/903fc230b73c7a859a730b0faf83d51571485176))

## v1.15.1 (2023-05-25)
### Fix
* **envelope:** Fix optional parameter default value ([`0307352`](https://github.com/MadeInPierre/finalynx/commit/0307352c1d3312b82010772d69e232175cd6ada9))

## v1.15.0 (2023-05-24)
### Feature
* **fetch:** Add crowdlending & startups, update asset subclass constant ([`261b752`](https://github.com/MadeInPierre/finalynx/commit/261b7520ad83dfb43b01bbc836c930e553ad0fb0))

## v1.14.6 (2023-05-23)
### Fix
* **dashboard:** Use full page width ([`a054dae`](https://github.com/MadeInPierre/finalynx/commit/a054dae61bcdbf831ae05625454e10c0132c0174))

## v1.14.5 (2023-05-23)
### Fix
* **fetch:** Use the new get_credit_accounts from API ([#85](https://github.com/MadeInPierre/finalynx/issues/85)) ([`cb8a4f1`](https://github.com/MadeInPierre/finalynx/commit/cb8a4f1c78a7ed3c6729eb3f44a0c2c3c606012a))

## v1.14.4 (2023-05-10)
### Fix
* **dashboard:** Hide amounts if specified by user ([`440f8c1`](https://github.com/MadeInPierre/finalynx/commit/440f8c134297b22be538826ca4b221d61aab003f))

## v1.14.3 (2023-05-10)
### Fix
* **install:** Bump nicegui version dependency ([`8b5c7ad`](https://github.com/MadeInPierre/finalynx/commit/8b5c7ad71c0939da187749c29477508f2c33dd1d))

## v1.14.2 (2023-05-10)
### Fix
* **imports:** Forgot to expose AssetSubclass import ([`eaf3e99`](https://github.com/MadeInPierre/finalynx/commit/eaf3e99a59496376686bfc2413b17c2f7812e5d7))

## v1.14.1 (2023-05-10)
### Fix
* **fetch:** Skip fetched lines with no amount invested ([`05adaa1`](https://github.com/MadeInPierre/finalynx/commit/05adaa1650b77965553ab387ab5c1ca7eca1c18c))

## v1.14.0 (2023-05-10)
### Feature
* **assets:** Create asset subclass definitions & visualizations ([#64](https://github.com/MadeInPierre/finalynx/issues/64)) ([`14a1d3d`](https://github.com/MadeInPierre/finalynx/commit/14a1d3d3d1923235a13f35406dbb490705a0ce58))

### Documentation
* Add envelope docstrings ([`f9317fb`](https://github.com/MadeInPierre/finalynx/commit/f9317fb30ca073e7d468df01eaf50e23cc963ecf))
* **envelope:** Add envelope docstrings ([`b7f5989`](https://github.com/MadeInPierre/finalynx/commit/b7f5989a1ecbe846e22654b3c018a2a222caa716))

## v1.13.1 (2023-05-09)
### Fix
* **fetch:** Fixed filter to skip malformed line ([`279abaf`](https://github.com/MadeInPierre/finalynx/commit/279abaff1526a020101ba428ab42e4a78eb442d1))

## v1.13.0 (2023-05-08)
### Feature
* **fetch:** Set folder envelope to autofill children ([`87fc64b`](https://github.com/MadeInPierre/finalynx/commit/87fc64bdda556bfa386d9e5df34335f427cd262a))
* **fetch:** Add & match envelope keys, connected new logic ([`6049225`](https://github.com/MadeInPierre/finalynx/commit/6049225455f7ca98965d94061ebff849ebe2ae8e))
* **fetch:** Refactor, fetch account & currency [WIP] ([`c876d42`](https://github.com/MadeInPierre/finalynx/commit/c876d4237fe0f642001ac182285717de6baacac1))
* **fetch:** Create FetchKey & FetchLine pair ([`7b7bd16`](https://github.com/MadeInPierre/finalynx/commit/7b7bd162f74a266718e97f69aca94888f9c8b8e8))

### Fix
* **fetch:** Fond euro amount mistake ([`6bb1555`](https://github.com/MadeInPierre/finalynx/commit/6bb155518ec7a884e8cf424e78eaca06da782913))
* **fetch:** Solve warning for buckets ([`36d4ea6`](https://github.com/MadeInPierre/finalynx/commit/36d4ea6b597745cc47abb06c4e8f65d2e30507ff))

## v1.12.1 (2023-05-01)
### Fix
* **fetch:** Ignore invalid elements from API response ([#66](https://github.com/MadeInPierre/finalynx/issues/66)) ([`fcfa91a`](https://github.com/MadeInPierre/finalynx/commit/fcfa91ae4a56c6ce4bd0595cb19173f313ef3a8c))

## v1.12.0 (2023-04-30)
### Feature
* **fetch:** Support loans and credit accounts ([#61](https://github.com/MadeInPierre/finalynx/issues/61)) ([`c51acd2`](https://github.com/MadeInPierre/finalynx/commit/c51acd2ef8eaf351797ad27677b6122a844b61b7))

## v1.11.2 (2023-04-29)
### Fix
* **currency:** Use node currency everywhere, add default config ([`94f4711`](https://github.com/MadeInPierre/finalynx/commit/94f47113e3d233d640ce55b0cecdbb924e7ca71e))

## v1.11.1 (2023-04-28)
### Fix
* **folder:** Propagate currencies to orphan nodes ([#56](https://github.com/MadeInPierre/finalynx/issues/56)) ([`e1f0968`](https://github.com/MadeInPierre/finalynx/commit/e1f0968e138bd006c58362bce6eb5afa101edcbd))

## v1.11.0 (2023-04-28)
### Feature
* **portfolio:** Basic support for multi-currencies ([#55](https://github.com/MadeInPierre/finalynx/issues/55)) ([`9b0e8ff`](https://github.com/MadeInPierre/finalynx/commit/9b0e8ff70346be6fab474c1cb35b2b3c4cee7337))

## v1.10.1 (2023-04-28)
### Fix
* **delta:** Include shared folders in the delta list ([`63b3762`](https://github.com/MadeInPierre/finalynx/commit/63b3762ea30f55fc9a66078700a63190fdfec101))

## v1.10.0 (2023-04-27)
### Feature
* **json:** Export & import portfolio ([#53](https://github.com/MadeInPierre/finalynx/issues/53)) ([`4f852fb`](https://github.com/MadeInPierre/finalynx/commit/4f852fba8c365189eada3e3c3b1aa7f38b34805a))

## v1.9.0 (2023-04-24)
### Feature
* **perf:** Can now set & analyze expected yearly performance ([#51](https://github.com/MadeInPierre/finalynx/issues/51)) ([`44bde0a`](https://github.com/MadeInPierre/finalynx/commit/44bde0af65be001ea3cef101d6ccba37a78d7d57))

## v1.8.3 (2023-04-24)
### Fix
* **delta:** Fix envelope delta calculation + display tweaks ([`a44ee2c`](https://github.com/MadeInPierre/finalynx/commit/a44ee2c029625d89983c879f96df6629bf5602d4))

## v1.8.2 (2023-04-21)
### Fix
* **delta:** Solved misalignment when using collapsed folders ([`ef540e5`](https://github.com/MadeInPierre/finalynx/commit/ef540e51ddc2626c45d05194aa8f0af4138abbbe))
* **delta:** Add investment summary sorted by envelope ([`1d679be`](https://github.com/MadeInPierre/finalynx/commit/1d679be039e1458fb865844f080bf59dbbb36038))

## v1.8.1 (2023-04-21)
### Fix
* **delta:** Add format shorcuts as command line options ([`3eee961`](https://github.com/MadeInPierre/finalynx/commit/3eee9614042302d0de031d1ff8ddf55ab8b810b6))

## v1.8.0 (2023-04-21)
### Feature
* **portfolio:** New 'console_delta' output format ([`35757ed`](https://github.com/MadeInPierre/finalynx/commit/35757edb33451e05059f85c05703621df38454a8))
* **portfolio:** Display current amount to ideal delta ([`b9930fb`](https://github.com/MadeInPierre/finalynx/commit/b9930fbe1a156d3f2246ec9d901a73eee4c5b16b))

## v1.7.0 (2023-04-20)
### Feature
* **folder:** Display warning if the sum of ratios != 100 ([`88068b9`](https://github.com/MadeInPierre/finalynx/commit/88068b965cfbccad1f22b13b12634b0af04c6295))
* **portfolio:** Display account in front of lines ([`b4456ee`](https://github.com/MadeInPierre/finalynx/commit/b4456ee6b548a7860d52c15fc1a1597db5e89e24))
* **node:** Format option to display the tree with targets only ([`968506d`](https://github.com/MadeInPierre/finalynx/commit/968506d3f8d3adb8ded9a6679a910af0a72d896c))
* **simulator:** Create barebones simulation with invest states ([`04320f6`](https://github.com/MadeInPierre/finalynx/commit/04320f6e32f4d225d68a893c5f325f8109a84dce))
* Add envelopes and plot them in dashboard ([`c650ec3`](https://github.com/MadeInPierre/finalynx/commit/c650ec31a92442a931c8cce90555e6a6a17b7fce))
* **dashboard:** Add basic newline support ([`d55e7d2`](https://github.com/MadeInPierre/finalynx/commit/d55e7d263ee847bfc2b85746d5d3cca5b1f0fca4))
* **dashboard:** Nice web tree with colors and icons ([`3d5db42`](https://github.com/MadeInPierre/finalynx/commit/3d5db423942d7ec6a16f7136abf5cfee39c5f8ca))
* **portfolio:** Can set the asset class in parent for all children ([`6bba5df`](https://github.com/MadeInPierre/finalynx/commit/6bba5df09f95faae3174a6624840155a4e250a55))
* **dashboard:** Can now customize the color map ([`8e9b862`](https://github.com/MadeInPierre/finalynx/commit/8e9b8620181f15c2f3d3739ad73bc2ba448378ea))
* **dashboard:** Click on a node to show its asset classes ([`0136d9e`](https://github.com/MadeInPierre/finalynx/commit/0136d9ec68fdbc735a0c3418955efeea502db81d))
* **analyzer:** Add asset classes and plot chart ([`2343b65`](https://github.com/MadeInPierre/finalynx/commit/2343b654373a96ec2abb20f997634d0b4f332462))

### Fix
* **fetch:** Add amounts for lines with same id ([`8dbc7cf`](https://github.com/MadeInPierre/finalynx/commit/8dbc7cfc95bab7337275d93600e3b4a4bd22d620))
* **dashboard:** Display collapsed/line folders on the web ([`9914a0f`](https://github.com/MadeInPierre/finalynx/commit/9914a0fcbc9c007a080424d99b8842f8b5c2d071))

## v1.6.0 (2023-03-31)
### Feature
* **targets:** Ratio targets now show the ideal absolute amount to reach ([`8bf0aac`](https://github.com/MadeInPierre/finalynx/commit/8bf0aac72af3e7cb82e9af2f82c4af14bbea2b5b))
* **fetch:** Import precious metals ([`54ce9f6`](https://github.com/MadeInPierre/finalynx/commit/54ce9f6b56c17328b7b8ab20d241065c9714b1ae))

### Fix
* **portfolio:** Simplify newline behavior ([`5071a4d`](https://github.com/MadeInPierre/finalynx/commit/5071a4de19d073b013b424d4d051d3c1e1bf24fc))
* **fetch:** Increase cache time to 12h ([`d41ddb0`](https://github.com/MadeInPierre/finalynx/commit/d41ddb0d187144cac27e705800dc072c2ed6bfe1))

## v1.5.0 (2023-03-23)
### Feature
* Add cryptos ([#43](https://github.com/MadeInPierre/finalynx/issues/43)) ([`ea79c75`](https://github.com/MadeInPierre/finalynx/commit/ea79c7599f3c9c64e67a5dd32f000b0833402190))

### Documentation
* **fetch:** Add key/id usage for identical lines ([`ecfddee`](https://github.com/MadeInPierre/finalynx/commit/ecfddee0c5cebe20bb271be74a346b25837e4396))

## v1.4.2 (2023-03-22)
### Fix
* **fetch:** Add support for id differentiation ([`4f830b8`](https://github.com/MadeInPierre/finalynx/commit/4f830b86f822c37bfa815b302689beaff2133f8b))

## v1.4.1 (2023-03-22)
### Fix
* **fetch:** Ask to reuse credentials if already saved ([`df8bec1`](https://github.com/MadeInPierre/finalynx/commit/df8bec1054daa19fe1e96f55849713977a9750a8))

## v1.4.0 (2023-03-21)
### Feature
* **dashboard:** Show the portfolio tree on the web dashboard ([#35](https://github.com/MadeInPierre/finalynx/issues/35)) ([`fa48bfc`](https://github.com/MadeInPierre/finalynx/commit/fa48bfce6d94f538062a2e3d346f1da1a0340c2c))

## v1.3.0 (2023-03-19)
### Feature
* **render:** Ability to customize the output format ([#38](https://github.com/MadeInPierre/finalynx/issues/38)) ([`97a2462`](https://github.com/MadeInPierre/finalynx/commit/97a24622ee18fa7f1ecf4ad673e57ae69fbd0631))

## v1.2.0 (2023-03-17)
### Feature
* **fetch:** Can now cache data locally, defaults to 1h ([#36](https://github.com/MadeInPierre/finalynx/issues/36)) ([`86036e2`](https://github.com/MadeInPierre/finalynx/commit/86036e2002a28653ceaba6798815ac641c24aef3))

### Documentation
* Remove documentation warning ([`5185495`](https://github.com/MadeInPierre/finalynx/commit/51854955e77c28c3b2c67d5dbed7e15979cd101d))
* Write full documentation ([#32](https://github.com/MadeInPierre/finalynx/issues/32)) ([`835262c`](https://github.com/MadeInPierre/finalynx/commit/835262cac2b44fd6a72be653f2da26ad9f04a882))
* Autobuild documentation and upload to Read The Docs ([#29](https://github.com/MadeInPierre/finalynx/issues/29)) ([`9c2d2d4`](https://github.com/MadeInPierre/finalynx/commit/9c2d2d4533bbfabf81549a56f65ee6a5dacb3f55))

## v1.1.1 (2023-03-07)
### Fix
* **fetch:** Env vars get priority over cookies file ([`f664ed8`](https://github.com/MadeInPierre/finalynx/commit/f664ed876ab35ee3c348b8168994dfbd5f5dd3d6))

## v1.1.0 (2023-03-05)
### Feature
* **fetch:** Add real estate support ([#24](https://github.com/MadeInPierre/finalynx/issues/24)) ([`d973fc0`](https://github.com/MadeInPierre/finalynx/commit/d973fc025eeeafc67b11089987b45d73272389b5))

## v1.0.1 (2023-03-04)
### Fix
* **dependencies:** Added unidecode and numpy dependencies ([`7574eae`](https://github.com/MadeInPierre/finalynx/commit/7574eae6261a3fdd6650c28bd3f530ae1d2d2026))

## v1.0.0 (2023-03-04)
### Feature
* Renamed project to Finalynx ([`4753651`](https://github.com/MadeInPierre/finalynx/commit/4753651ceac0d51514effb0b5ac2723d7dc26d51))

### Fix
* **submodules:** Hopefully correctly moved finary_api ([`6b65d9c`](https://github.com/MadeInPierre/finalynx/commit/6b65d9c97365f325cd4aeb2649bcdd1f6f8a56a8))
* Renamed source folder ([`f78318f`](https://github.com/MadeInPierre/finalynx/commit/f78318f5b6ddcc13d97e53586bc6592541817022))

### Breaking
* Renamed all references of finary_assistant to finalynx ([`4753651`](https://github.com/MadeInPierre/finalynx/commit/4753651ceac0d51514effb0b5ac2723d7dc26d51))

## v0.2.1 (2023-02-21)
### Fix
* **ci:** Better release message ([`f097aaf`](https://github.com/MadeInPierre/finalynx/commit/f097aaf52337ef2f456308c720d79746887bb1e3))

## v0.2.0 (2023-02-20)
### Feature
* **presentation:** Updated README&CONTRIBUTING, project looks good! ([`2267bd3`](https://github.com/MadeInPierre/finalynx/commit/2267bd333242145b55a6393deed6c41014aeaf9f))

### Documentation
* **readme:** Created CONTRIBUTING.md guidelines ([`75e2d75`](https://github.com/MadeInPierre/finalynx/commit/75e2d758328cce9e18ee02dc2f8d2580677d1bf4))

## v0.1.8 (2023-02-20)
### Fix
* Static pypi badge ([`ed669ea`](https://github.com/MadeInPierre/finalynx/commit/ed669ea65bf946af2fa7bd8d53b762fa469260e2))

## v0.1.7 (2023-02-20)
### Fix
* **ci:** Forgot to recursively clone the repo ([`3a89f8e`](https://github.com/MadeInPierre/finalynx/commit/3a89f8e015b422ae86a232377f55e97adaf3a2b1))

## v0.1.6 (2023-02-20)
### Fix
* **ci:** Attempting new glob pattern to include finary_api ([`12d81ea`](https://github.com/MadeInPierre/finalynx/commit/12d81ea2c0bc2e7cdeacd4417e2e642cdf7a8d04))

## v0.1.5 (2023-02-20)
### Fix
* **ci:** Include finary_api to the PiPY package ([`6b058c7`](https://github.com/MadeInPierre/finalynx/commit/6b058c7abda05d78896389289f6280e7b7f8a5dc))

## v0.1.4 (2023-02-19)
### Fix
* Relative import in module init ([`126fc6e`](https://github.com/MadeInPierre/finalynx/commit/126fc6eda9dbc75b9e1af66ac617e7e46062b6f3))

## v0.1.3 (2023-02-19)
### Fix
* Trying to remove custom commit message ([`89bed31`](https://github.com/MadeInPierre/finalynx/commit/89bed317f66a4a27ac83e17586a9e8994abae632))
* Manual set to version 0.1.2 ([`d8284d1`](https://github.com/MadeInPierre/finalynx/commit/d8284d13c02bf4a525b9204948968c37a673a7b2))

## v0.1.0 (2023-02-19)
### Feature
* Forcing bump to 0.1 ([`a2fa623`](https://github.com/MadeInPierre/finalynx/commit/a2fa623d10a1ea20f236bf6784fa21599014de09))

## v0.0.1 (2023-02-19)
### Fix
* Readme image urls ([`89e1d7b`](https://github.com/MadeInPierre/finalynx/commit/89e1d7b169ffa59e9c869f03da6e740c90acf854))
* Cleaner path management, new command option to force signin ([`a29d1bb`](https://github.com/MadeInPierre/finalynx/commit/a29d1bb9bc4c3c0cf8cb152c5205f8e2b142c4f8))
* Can now login with cookies without saving credentials ([`5fe8dfe`](https://github.com/MadeInPierre/finalynx/commit/5fe8dfe8645feba0ab2b55c73e610f6b9668472a))
* Skip credentials if envars available ([`c888a87`](https://github.com/MadeInPierre/finalynx/commit/c888a8756117d1087b4a943a1e4693ea6c2f7ee7))

### Documentation
* Added PyPI badge to README ([`af328e6`](https://github.com/MadeInPierre/finalynx/commit/af328e673691cbca4db73313aba7637ce4f20214))
