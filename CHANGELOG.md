# CHANGELOG



## v1.23.1 (2024-01-21)

### Chore

* chore: fix readme img ([`a3ed9a0`](https://github.com/MadeInPierre/finalynx/commit/a3ed9a0e2af4b732002bcc6adbe340a10515f064))

### Ci

* ci: manual bump to v1.23.0 ([`0daa0cc`](https://github.com/MadeInPierre/finalynx/commit/0daa0cc0ec3318db07f946779e0f7c6269efe00b))

### Fix

* fix: update finary-uapi to 0.2.0 ([`a547db0`](https://github.com/MadeInPierre/finalynx/commit/a547db016ca22ebfe56672d400379ce35566ea2b))


## v1.23.0 (2024-01-15)

### Ci

* ci: manual bump to v1.22.4 ([`8e8ec72`](https://github.com/MadeInPierre/finalynx/commit/8e8ec723eb6f3db2f03170cf28a155b9c08c3f2f))

* ci: add permissions for semantic release ([`7e986a5`](https://github.com/MadeInPierre/finalynx/commit/7e986a57fd9db0f6ce098bef59d88b164d94d68c))

### Feature

* feat(dashboard): add layered evolution graphs (#150)

More graphs available in the dashboard with view per classification (envelopes, asset classes, line by line, ...) by @gcoue ([`6f0d1b3`](https://github.com/MadeInPierre/finalynx/commit/6f0d1b39d72682fc005fc0e7e28101c725f6b7c5))


## v1.22.4 (2024-01-13)

### Chore

* chore: update full example ([`00138dd`](https://github.com/MadeInPierre/finalynx/commit/00138dd2fcaf2226402b5d1881ee9993624c8cc7))

### Ci

* ci: manual update to v1.22.3 ([`c2d7d82`](https://github.com/MadeInPierre/finalynx/commit/c2d7d8286ad289222fecafcdf4456356a7ffcebc))

* ci: use trusted auth for PyPI publishing ([`ea2a814`](https://github.com/MadeInPierre/finalynx/commit/ea2a814b091d3c47987645b1ce9ac1bead5b61f8))

### Fix

* fix(fetch): change credit card to negative amount (#147)

* Change credit card to negative amount

* Rollback source_finary.py

* Change credit card to negative amount

* [pre-commit.ci lite] apply automatic fixes

* Add a flag to allow the potfolio restitution for each simulation step

* Add a flag to allow the potfolio restitution for each simulation step

* fix: correct the recurrence function to be more precise on Yearly recurrence

* [pre-commit.ci lite] apply automatic fixes

* style: minor refactoring ([`d9478db`](https://github.com/MadeInPierre/finalynx/commit/d9478db0bcd4db01887ddee5ed542dcc6204116b))


## v1.22.3 (2023-09-18)

### Chore

* chore: manual bump to version 1.22.2 ([`2316fdd`](https://github.com/MadeInPierre/finalynx/commit/2316fdd2dcee5846f6cf6af5890fc9074e88cc33))

### Ci

* ci: fix semantic release (breaking config changes) ([`a383983`](https://github.com/MadeInPierre/finalynx/commit/a3839832d07dfcc60d8f65d3273faa046b6ee5fb))

### Documentation

* docs: add simulation template tutorial ([`c15b97c`](https://github.com/MadeInPierre/finalynx/commit/c15b97c9dac452a306745eb0849e13d2b1be75f0))

* docs: add full example ([`de11f6e`](https://github.com/MadeInPierre/finalynx/commit/de11f6ed290e6f510a055b6ab727959538e03608))

* docs: add budget tutorial ([`0fe1513`](https://github.com/MadeInPierre/finalynx/commit/0fe1513c5aeb191eea7cce77ff8fdaa535ddb56e))

* docs: update readme french (#141)

docs : update readme french

Correction orthographique ([`98108d9`](https://github.com/MadeInPierre/finalynx/commit/98108d9cc47360c4f090efb9e2c57ab1e82f9d8b))

* docs: add simulation tutorial, fix typos ([`8c6ab9a`](https://github.com/MadeInPierre/finalynx/commit/8c6ab9a9e9557d18399fa8562fec93701f8da5d7))

### Fix

* fix: clarify signup for 2FA, simulation progress bar ([`3b5c9c4`](https://github.com/MadeInPierre/finalynx/commit/3b5c9c4e34f8101e3b0ea1095dbaa83a06e55959))

### Style

* style: minor improvements ([`57b2424`](https://github.com/MadeInPierre/finalynx/commit/57b2424ead1ab1c9a9cc4c89519850a4a732b02b))


## v1.22.2 (2023-08-10)

### Fix

* fix(simulation): add salary income &amp; expense growth ([`84e6524`](https://github.com/MadeInPierre/finalynx/commit/84e6524cba7b47fb1e4a4d87dc895d68e796506b))


## v1.22.1 (2023-08-10)

### Fix

* fix(simulator): show portfolio evolution in dashboard, cleanup ([`78c1782`](https://github.com/MadeInPierre/finalynx/commit/78c17827b994b83ee4ebac529c141d77a09b8b9a))


## v1.22.0 (2023-07-31)

### Build

* build: bump finary_uapi to 0.1.4 ([`dc4bab6`](https://github.com/MadeInPierre/finalynx/commit/dc4bab68a89e6a9df57b9cc64a7acbdb8166cb0b))

### Documentation

* docs: add readme french (#137)

* docs: add readme french

* docs: readme tweaks ([`064d126`](https://github.com/MadeInPierre/finalynx/commit/064d1261aae19f2ff6e2ba0da865acd52f8de587))

### Feature

* feat(simulation): simulate your portfolio&#39;s future (#136)

* feat(simulation): create timeline structure, display worth evolution

* refactor: split simulator classes in separate files

* fix: ask before fetching from N26

* feat: add default event to apply yearly performance

* feat: add autobalance default quarterly event

* docs: add docstrings ([`3349f66`](https://github.com/MadeInPierre/finalynx/commit/3349f660c183ada495110349706958ab7cc5d39a))


## v1.21.0 (2023-07-15)

### Chore

* chore: update &amp; add screenshots to readme ([`2d17afa`](https://github.com/MadeInPierre/finalynx/commit/2d17afabbee22cd2e4e955b523d505f3cfcc7996))

### Documentation

* docs: visual tweaks, update screenshots ([`efaa8b8`](https://github.com/MadeInPierre/finalynx/commit/efaa8b86d24578db10c3c3ce81774413b0d189a3))

* docs: add envelopes and sources tutorials ([`20a9a82`](https://github.com/MadeInPierre/finalynx/commit/20a9a823d20bd5bd2b37ca8abaca02e013062d63))

* docs: organize tutorials, add awesome badge ([`62b249d`](https://github.com/MadeInPierre/finalynx/commit/62b249d11b8e14e98f137286bd160d518f4a174e))

* docs: improve installation guide readability ([`a57f996`](https://github.com/MadeInPierre/finalynx/commit/a57f996ffa25028b332f9628946d7c4039a1c932))

* docs: create tutorials table of contents online ([`e690ab0`](https://github.com/MadeInPierre/finalynx/commit/e690ab09189be56fbd1109abc21c9ac51b5fcc3d))

### Feature

* feat(budget): manage your daily expenses (N26 only) (#135)

* feat(budget): manage your daily expenses! (N26 only)

* refactor(budget): move table render in separate file

* feat(budget): interactively set expense fields

* fix: remove default imports to budget

* refactor: rearrange budget methods to fetch/render/review

* fix(budget): exit review gracefully on CTRL+C

* feat(budget): add command line &amp; Assistant options

* refactor: inherit N26 from SourceBaseExpense

* build: add budget dependencies

* build: add pytz dependency

* chore: update readme with screenshots

* feat: add budget summary console panel

* feat: add monthly mean to summary

* refactor(n26): prompt user credentials like Finary

* test: disable finary tests for now

* feat: hide expense table when empty ([`6209b40`](https://github.com/MadeInPierre/finalynx/commit/6209b4088d8a37640a71832e5bb275ab851b5ac6))

### Refactor

* refactor: move recommendations in copilot submodule ([`8b9f7ee`](https://github.com/MadeInPierre/finalynx/commit/8b9f7ee1d7ade194b489be12b3e13da8e27c7c87))


## v1.20.3 (2023-06-07)

### Chore

* chore: add sponsors badge :) thank you! ([`5601d5d`](https://github.com/MadeInPierre/finalynx/commit/5601d5d4c254d0fee15cf57f5cb53252b7c7e615))

### Documentation

* docs: write tutorial for targets, tweaks ([`3dd0883`](https://github.com/MadeInPierre/finalynx/commit/3dd08837c66d103301d16b9b26038a47f09a38c4))

* docs: update readme tutorial links ([`c4beabf`](https://github.com/MadeInPierre/finalynx/commit/c4beabf6be961da5150170c544c39c983938ac92))

### Fix

* fix: import error caused crash in v1.20.2

closes #132 ([`bcd0171`](https://github.com/MadeInPierre/finalynx/commit/bcd01715929a2e28721339b4a41ea9b3574aa953))

### Style

* style(recommendations): show message if envelopes not set ([`342fd75`](https://github.com/MadeInPierre/finalynx/commit/342fd757f6724d38d1b9418c57184ba381f70a4c))


## v1.20.2 (2023-06-06)

### Ci

* ci: fix stuck ci because of dashboard launch ([`d2d863d`](https://github.com/MadeInPierre/finalynx/commit/d2d863dd851344ccea3539cef039d23dbe344adb))

### Documentation

* docs: fix screenshot url ([`4556af7`](https://github.com/MadeInPierre/finalynx/commit/4556af73af91be4af3515d31802e20bb59a45fcc))

* docs: create tutorials ([`93780d2`](https://github.com/MadeInPierre/finalynx/commit/93780d28c3c81bcf54a0238219413733898d4c45))

### Fix

* fix(sidecar): add option to hide renders for expanded folders ([`560d4fa`](https://github.com/MadeInPierre/finalynx/commit/560d4fac58b65e62eee5152c03ba66c73303f597))

* fix(recommendations): sort by total delta ([`5e686ef`](https://github.com/MadeInPierre/finalynx/commit/5e686ef26417611f3cc309c9b71abe962f284d14))

### Refactor

* refactor(sidecar): create sidecar configuration class ([`96ba022`](https://github.com/MadeInPierre/finalynx/commit/96ba022a3637d8449711bf6437b5a6cc297d6389))


## v1.20.1 (2023-06-04)

### Fix

* fix(recommendations): classify folders by parent name

closes #131 ([`d2e4d22`](https://github.com/MadeInPierre/finalynx/commit/d2e4d2218dcf8f22ed8eb4598a480c6610aa4bb4))

### Refactor

* refactor: small assistant cleanup &amp; minor bugfixes ([`d42961b`](https://github.com/MadeInPierre/finalynx/commit/d42961bad86edce39c3f8da4f733ee17408bd2f3))

* refactor(assistant): split the run method to give the user choice ([`e32ca45`](https://github.com/MadeInPierre/finalynx/commit/e32ca452a58fa4b6ee89ef36539e2b8f4c16e23e))


## v1.20.0 (2023-06-04)

### Feature

* feat(sidecar): add configurable sidecar title ([`59ded22`](https://github.com/MadeInPierre/finalynx/commit/59ded22b7efadcdd7a863cd76c3fe348cbe11385))

* feat(sidecar): add support for multiple sidecars

closes #129 ([`81df340`](https://github.com/MadeInPierre/finalynx/commit/81df34028f80b34304b0a9e56298b05c5382a53f))

* feat(sidecar): customizable sidecar formats

closes #69 ([`6c4759a`](https://github.com/MadeInPierre/finalynx/commit/6c4759a1c070814ae409a9e2921d3372853c55c4))

### Fix

* fix(envelope): make created date optional

closes #114 ([`18d5873`](https://github.com/MadeInPierre/finalynx/commit/18d5873d84f6f078f1fd558f0bf4b388aee4daf3))

* fix: notify user if a bucket was not fully used ([`1709068`](https://github.com/MadeInPierre/finalynx/commit/17090688cb7331b939ca7b4d1d7f1894e00377f2))

* fix(target): fix the previous fix... ([`0ad360a`](https://github.com/MadeInPierre/finalynx/commit/0ad360a33ba2fe7afde437995f9f603f498c930b))


## v1.19.1 (2023-06-03)

### Chore

* chore(telegram): add telegram bot example ([`9187418`](https://github.com/MadeInPierre/finalynx/commit/91874185b54024a7c9c07e4eafe2e5185538bc44))

### Fix

* fix(target): more intuitive displayed node ratio

Until now, the percentages next to the amounts showed the ratio between
the current and ideal amounts.

However this wasn&#39;t intuitive with the current layout,
so the ratios now show their relative percentage in the parent folder. ([`20da9c8`](https://github.com/MadeInPierre/finalynx/commit/20da9c892d96c4cf7f165c306d1778e1c448c4c5))


## v1.19.0 (2023-06-02)

### Feature

* feat(export): export the portfolio tree to PNG

closes #50 ([`f35606a`](https://github.com/MadeInPierre/finalynx/commit/f35606aa7a38c9d849b02c160b608f46a89a361c))


## v1.18.4 (2023-06-02)

### Fix

* fix(portfolio): folder attributes weren&#39;t propagating to all successors

closes #123 ([`4a0cbf3`](https://github.com/MadeInPierre/finalynx/commit/4a0cbf3a6dfbe3a862a0eba3a92c3c300a939f0b))


## v1.18.3 (2023-06-01)

### Fix

* fix(recommendations): redo delta render rules ([`d0fe97c`](https://github.com/MadeInPierre/finalynx/commit/d0fe97c62cfc910102054a42366fbc8f58848d33))


## v1.18.2 (2023-05-31)

### Fix

* fix(fetch): customizable per-source cache validity

5 days default for RealT

12h default for Finary and all other sources

Users can set their preferred values when instantiating their sources. ([`964fd55`](https://github.com/MadeInPierre/finalynx/commit/964fd5557e3ed0cb1d9e478c053501198363bf5f))

* fix(fetch): fetch from RealT using &#39;contractAddress/uuid&#39; instead of &#39;symbol&#39; (#119)

* fix: Ignoring invalid elements from API respone

* fix(fetch): Ignore invalid elements from API response

* fix(fetch): Use get_accounts_credits from API Finary

* feat(fetch): add RealT wallet fetch source

* feat(fetch): add RealT wallet fetch source

* feat(fetch): add RealT wallet fetch source

* refactor(fetch): unify parameter inputs &amp; console output

* style(console): display node ratio next to amount (#111)

* feat(ratio): display node % when no target is defined

closes #110

* style(console): display node ratios next to amounts

* test: use finary demo account to test Finalynx (#112)

* test: use finary demo account to test Finalynx

* ci: attempt to use env from github actions syntax

* feat(console): add support for light/dark/custom console themes (#115)

* feat(console): add option to change the console render theme

closes #77

* feat(theme): connect theme class to elements

* fix(theme): fix cross-module reference access, set dark theme

* fix(theme): these dark colors look more compatible

* fix: tweaks

* chore(release): auto bump version to 1.17.0

Automatically generated by python-semantic-release

* fix(fetch): reviewed token lookup by &#39;contractAddess&#39;/&#39;uuid&#39; instead of symbol

* [pre-commit.ci lite] apply automatic fixes

* fix(fetch): reviewed token lookup by &#39;contractAddess&#39;/&#39;uuid&#39; instead of symbol

* fix(fetch): reviewed token lookup by &#39;contractAddress&#39;/&#39;uuid&#39; instead of symbol

* fix(fetch): reviewed token lookup by &#39;contractAddress&#39;/&#39;uuid&#39; instead of symbol

* fix(fetch): realt refactor, fix auto-add currency ([`441fb66`](https://github.com/MadeInPierre/finalynx/commit/441fb66231155b36ba1bcdaa3e714277ff309c1c))


## v1.18.1 (2023-05-31)

### Fix

* fix(fetch): skip malformed realt lines for now ([`3b55c43`](https://github.com/MadeInPierre/finalynx/commit/3b55c4305d2eab2c1c8a7f862be05da4a8426eeb))


## v1.18.0 (2023-05-31)

### Chore

* chore(theme): forgot to test.. rename element name ([`3969f76`](https://github.com/MadeInPierre/finalynx/commit/3969f764d77241c7aa0e921dab4c7ecc461203e8))

* chore(theme): add theme element descriptions ([`332fe7e`](https://github.com/MadeInPierre/finalynx/commit/332fe7ea05aefdb7e9fcc67588805dc0371bf6e5))

### Feature

* feat(fetch): add new RealT fetch source (#106)

* fix: Ignoring invalid elements from API respone

* fix(fetch): Ignore invalid elements from API response

* fix(fetch): Use get_accounts_credits from API Finary

* feat(fetch): add RealT wallet fetch source

* feat(fetch): add RealT wallet fetch source

* feat(fetch): add RealT wallet fetch source

* refactor(fetch): unify parameter inputs &amp; console output

* style(console): display node ratio next to amount (#111)

* feat(ratio): display node % when no target is defined

closes #110

* style(console): display node ratios next to amounts

---------

Co-authored-by: nmathey &lt;20896232+nmathey@users.noreply.github.com&gt;

* test: use finary demo account to test Finalynx (#112)

* test: use finary demo account to test Finalynx

* ci: attempt to use env from github actions syntax

* feat(console): add support for light/dark/custom console themes (#115)

* feat(console): add option to change the console render theme

closes #77

* feat(theme): connect theme class to elements

* fix(theme): fix cross-module reference access, set dark theme

* fix(theme): these dark colors look more compatible

* fix: tweaks

* chore(release): auto bump version to 1.17.0

Automatically generated by python-semantic-release ([`ca00549`](https://github.com/MadeInPierre/finalynx/commit/ca0054980026980368da1addbc05f2e6dc5f6b4a))


## v1.17.0 (2023-05-30)

### Feature

* feat(console): add support for light/dark/custom console themes (#115)

* feat(console): add option to change the console render theme

closes #77

* feat(theme): connect theme class to elements

* fix(theme): fix cross-module reference access, set dark theme

* fix(theme): these dark colors look more compatible

* fix: tweaks ([`7722e29`](https://github.com/MadeInPierre/finalynx/commit/7722e296ec0f869469ca39e97848b88d426d941c))

### Style

* style(console): display node ratio next to amount (#111)

* feat(ratio): display node % when no target is defined

closes #110

* style(console): display node ratios next to amounts

---------

Co-authored-by: nmathey &lt;20896232+nmathey@users.noreply.github.com&gt; ([`b324562`](https://github.com/MadeInPierre/finalynx/commit/b324562b48339cc7e841347c599184d495aea61e))

### Test

* test: use finary demo account to test Finalynx (#112)

* test: use finary demo account to test Finalynx

* ci: attempt to use env from github actions syntax ([`bc06556`](https://github.com/MadeInPierre/finalynx/commit/bc06556c7a04f077969559d495f326a6540f0ee6))


## v1.16.3 (2023-05-27)

### Fix

* fix(delta): align deltas when showing portfolio root

closes #105 ([`cb20954`](https://github.com/MadeInPierre/finalynx/commit/cb20954e2b6dfaea56c31394f58f4f977c647109))


## v1.16.2 (2023-05-26)

### Fix

* fix(fetch): spinner was hiding user prompts

closes #102 ([`8c5a78f`](https://github.com/MadeInPierre/finalynx/commit/8c5a78fc8df7e781783c1877b29b25589fe14bc3))


## v1.16.1 (2023-05-26)

### Performance

* perf(finary): fetch all finary investments in only one call ([`f119c49`](https://github.com/MadeInPierre/finalynx/commit/f119c49967f8fc20dc591f1525a678e024cfabe3))


## v1.16.0 (2023-05-26)

### Feature

* feat: add startup for exotic investiment in constant file (#100)

feat: add startup asset subclass ([`598f0e0`](https://github.com/MadeInPierre/finalynx/commit/598f0e0a026080e30de8c43e4b778e4bd80600ef))

* feat(fetch): add support for multiple fetch sources (#97)

* feat(fetch): add crowdlending &amp; startups, update asset subclass constant

* chore(release): auto bump version to 1.15.0

Automatically generated by python-semantic-release

* refactor(fetch): move common fetch logic to abstract FetchBase class

* refactor(fetch): renamed fetch_finary to source

* feat(fetch): add support for multiple sources, activate any combination

* feat(fetch): create example source, tweaks

* fix(envelope): fix optional parameter default value

* chore(release): auto bump version to 1.15.1

Automatically generated by python-semantic-release ([`903fc23`](https://github.com/MadeInPierre/finalynx/commit/903fc230b73c7a859a730b0faf83d51571485176))


## v1.15.1 (2023-05-25)

### Feature

* feat(fetch): add crowdlending &amp; startups, update asset subclass constant

closes #91
closes #71

Co-authored-by: sebfar9172 &lt;52531214+sebfar9172@users.noreply.github.com&gt; ([`92c3f2d`](https://github.com/MadeInPierre/finalynx/commit/92c3f2daa6de2536b535ee048a16d35a1121177a))

### Fix

* fix(envelope): fix optional parameter default value

closes #98

Co-authored-by: sebfar9172 &lt;52531214+sebfar9172@users.noreply.github.com&gt; ([`0307352`](https://github.com/MadeInPierre/finalynx/commit/0307352c1d3312b82010772d69e232175cd6ada9))


## v1.14.6 (2023-05-23)

### Fix

* fix(dashboard): use full page width

closes #90 ([`a054dae`](https://github.com/MadeInPierre/finalynx/commit/a054dae61bcdbf831ae05625454e10c0132c0174))


## v1.14.5 (2023-05-23)

### Build

* build: replace api submodule with finary_uapi from pip (#94)

* build: remove finary_api submodule

* build: add finary_uapi pip dependency

* build: use finary_uapi in finalynx instead of finary_api

* build: remove the need to append syspath 🎉

* build: bump python to 3.10 for readthedocs ([`8116827`](https://github.com/MadeInPierre/finalynx/commit/8116827601ffdf07ae96c7af117bc08f466a90c9))

### Fix

* fix(fetch): use the new get_credit_accounts from API (#85)

* fix: Ignoring invalid elements from API respone

* fix(fetch): Ignore invalid elements from API response

* fix(fetch): Use get_accounts_credits from API Finary ([`cb8a4f1`](https://github.com/MadeInPierre/finalynx/commit/cb8a4f1c78a7ed3c6729eb3f44a0c2c3c606012a))


## v1.14.4 (2023-05-10)

### Fix

* fix(dashboard): hide amounts if specified by user

Closes #80 ([`440f8c1`](https://github.com/MadeInPierre/finalynx/commit/440f8c134297b22be538826ca4b221d61aab003f))


## v1.14.3 (2023-05-10)

### Fix

* fix(install): bump nicegui version dependency

Co-authored-by: yovanoc &lt;yovano_c@outlook.com&gt; ([`8b5c7ad`](https://github.com/MadeInPierre/finalynx/commit/8b5c7ad71c0939da187749c29477508f2c33dd1d))


## v1.14.2 (2023-05-10)

### Fix

* fix(imports): forgot to expose AssetSubclass import

Co-authored-by: yovanoc &lt;yovano_c@outlook.com&gt; ([`eaf3e99`](https://github.com/MadeInPierre/finalynx/commit/eaf3e99a59496376686bfc2413b17c2f7812e5d7))


## v1.14.1 (2023-05-10)

### Fix

* fix(fetch): skip fetched lines with no amount invested ([`05adaa1`](https://github.com/MadeInPierre/finalynx/commit/05adaa1650b77965553ab387ab5c1ca7eca1c18c))


## v1.14.0 (2023-05-10)

### Documentation

* docs: add envelope docstrings ([`f9317fb`](https://github.com/MadeInPierre/finalynx/commit/f9317fb30ca073e7d468df01eaf50e23cc963ecf))

* docs(envelope): add envelope docstrings ([`b7f5989`](https://github.com/MadeInPierre/finalynx/commit/b7f5989a1ecbe846e22654b3c018a2a222caa716))

### Feature

* feat(assets): create asset subclass definitions &amp; visualizations (#64)

* feat(assets): create asset subclass definitions

* feat(asset): add asset subclass optional parameter

* fix: asset subclass recursive set

* feat(dashboard): double pie chart for asset classes &amp; subclasses

* fix(dashboard): autohide labels when slice too small ([`14a1d3d`](https://github.com/MadeInPierre/finalynx/commit/14a1d3d3d1923235a13f35406dbb490705a0ce58))


## v1.13.1 (2023-05-09)

### Fix

* fix(fetch): fixed filter to skip malformed line

Closes #73 ([`279abaf`](https://github.com/MadeInPierre/finalynx/commit/279abaff1526a020101ba428ab42e4a78eb442d1))


## v1.13.0 (2023-05-08)

### Feature

* feat(fetch): set folder envelope to autofill children ([`87fc64b`](https://github.com/MadeInPierre/finalynx/commit/87fc64bdda556bfa386d9e5df34335f427cd262a))

* feat(fetch): add &amp; match envelope keys, connected new logic ([`6049225`](https://github.com/MadeInPierre/finalynx/commit/6049225455f7ca98965d94061ebff849ebe2ae8e))

* feat(fetch): refactor, fetch account &amp; currency [WIP] ([`c876d42`](https://github.com/MadeInPierre/finalynx/commit/c876d4237fe0f642001ac182285717de6baacac1))

* feat(fetch): create FetchKey &amp; FetchLine pair ([`7b7bd16`](https://github.com/MadeInPierre/finalynx/commit/7b7bd162f74a266718e97f69aca94888f9c8b8e8))

### Fix

* fix(fetch): fond euro amount mistake ([`6bb1555`](https://github.com/MadeInPierre/finalynx/commit/6bb155518ec7a884e8cf424e78eaca06da782913))

* fix(fetch): solve warning for buckets ([`36d4ea6`](https://github.com/MadeInPierre/finalynx/commit/36d4ea6b597745cc47abb06c4e8f65d2e30507ff))

### Refactor

* refactor: small code cleanup ([`4ff3a2b`](https://github.com/MadeInPierre/finalynx/commit/4ff3a2b14a6d0e1f0e06001ef556897969e219d1))

* refactor(fetch): remove FetchKey, useless complexity ([`46c4e46`](https://github.com/MadeInPierre/finalynx/commit/46c4e46d63cb57313fd0b040f5d53a2c8773fdfc))

### Style

* style(console): small perf print adjustment ([`0a8979f`](https://github.com/MadeInPierre/finalynx/commit/0a8979f4cff557ac9e48a6286e3418efe5cbd64e))


## v1.12.1 (2023-05-01)

### Fix

* fix(fetch): ignore invalid elements from API response (#66)

* fix: Ignoring invalid elements from API respone

* fix(fetch): Ignore invalid elements from API response ([`fcfa91a`](https://github.com/MadeInPierre/finalynx/commit/fcfa91ae4a56c6ce4bd0595cb19173f313ef3a8c))


## v1.12.0 (2023-04-30)

### Feature

* feat(fetch): support loans and credit accounts (#61)

* feat(fetch): support loans

* feat(fetch): add credit accounts

* fix(fetch): fix credit accounts name ([`c51acd2`](https://github.com/MadeInPierre/finalynx/commit/c51acd2ef8eaf351797ad27677b6122a844b61b7))


## v1.11.2 (2023-04-29)

### Fix

* fix(currency): use node currency everywhere, add default config

Closes #59 ([`94f4711`](https://github.com/MadeInPierre/finalynx/commit/94f47113e3d233d640ce55b0cecdbb924e7ca71e))


## v1.11.1 (2023-04-28)

### Fix

* fix(folder): propagate currencies to orphan nodes (#56)

fix(folder): Propagate currencies to orphan nodes ([`e1f0968`](https://github.com/MadeInPierre/finalynx/commit/e1f0968e138bd006c58362bce6eb5afa101edcbd))


## v1.11.0 (2023-04-28)

### Feature

* feat(portfolio): basic support for multi-currencies (#55)

* fix(fetch): use display_current_value

* feat(portfolio): set any node&#39;s currency symbol

* fix(currency): set a global currency in the Portfolio object ([`9b0e8ff`](https://github.com/MadeInPierre/finalynx/commit/9b0e8ff70346be6fab474c1cb35b2b3c4cee7337))


## v1.10.1 (2023-04-28)

### Fix

* fix(delta): include shared folders in the delta list ([`63b3762`](https://github.com/MadeInPierre/finalynx/commit/63b3762ea30f55fc9a66078700a63190fdfec101))


## v1.10.0 (2023-04-27)

### Feature

* feat(json): export &amp; import portfolio (#53)

* feat(json): export assistant state to json

* fix(json): add command line option to set save path

* fix(json): adapted demo file

* fix: render bug for deltas panel

* feat(parse): partial loading from json

* feat(parse): can now import the portfolio structure

* feat(import): connected buckets/envelopes to nodes

* refactor: project cleanup before merge ([`4f852fb`](https://github.com/MadeInPierre/finalynx/commit/4f852fba8c365189eada3e3c3b1aa7f38b34805a))


## v1.9.0 (2023-04-24)

### Feature

* feat(perf): can now set &amp; analyze expected yearly performance (#51) ([`44bde0a`](https://github.com/MadeInPierre/finalynx/commit/44bde0af65be001ea3cef101d6ccba37a78d7d57))


## v1.8.3 (2023-04-24)

### Fix

* fix(delta): fix envelope delta calculation + display tweaks ([`a44ee2c`](https://github.com/MadeInPierre/finalynx/commit/a44ee2c029625d89983c879f96df6629bf5602d4))


## v1.8.2 (2023-04-21)

### Chore

* chore(demo): fix demo ([`0486a74`](https://github.com/MadeInPierre/finalynx/commit/0486a74a44658a31a92b34fb387b30358d36a12c))

### Fix

* fix(delta): solved misalignment when using collapsed folders ([`ef540e5`](https://github.com/MadeInPierre/finalynx/commit/ef540e51ddc2626c45d05194aa8f0af4138abbbe))

* fix(delta): add investment summary sorted by envelope ([`1d679be`](https://github.com/MadeInPierre/finalynx/commit/1d679be039e1458fb865844f080bf59dbbb36038))


## v1.8.1 (2023-04-21)

### Chore

* chore: readme &amp; styling tweaks for delta ([`956c16a`](https://github.com/MadeInPierre/finalynx/commit/956c16a6f5af39ab1c2c66bd0b44938b05ccd22b))

### Fix

* fix(delta): add format shorcuts as command line options ([`3eee961`](https://github.com/MadeInPierre/finalynx/commit/3eee9614042302d0de031d1ff8ddf55ab8b810b6))


## v1.8.0 (2023-04-21)

### Chore

* chore: created PEE, small dashboard tweaks ([`cbd5b09`](https://github.com/MadeInPierre/finalynx/commit/cbd5b09391d56ce16092d201617f8eb7681acb82))

### Feature

* feat(portfolio): new &#39;console_delta&#39; output format ([`35757ed`](https://github.com/MadeInPierre/finalynx/commit/35757edb33451e05059f85c05703621df38454a8))

* feat(portfolio): display current amount to ideal delta ([`b9930fb`](https://github.com/MadeInPierre/finalynx/commit/b9930fbe1a156d3f2246ec9d901a73eee4c5b16b))


## v1.7.0 (2023-04-20)

### Feature

* feat(folder): display warning if the sum of ratios != 100 ([`88068b9`](https://github.com/MadeInPierre/finalynx/commit/88068b965cfbccad1f22b13b12634b0af04c6295))

* feat(portfolio): display account in front of lines ([`b4456ee`](https://github.com/MadeInPierre/finalynx/commit/b4456ee6b548a7860d52c15fc1a1597db5e89e24))

* feat(node): format option to display the tree with targets only

Simply use the [console_targets] output format ([`968506d`](https://github.com/MadeInPierre/finalynx/commit/968506d3f8d3adb8ded9a6679a910af0a72d896c))

* feat(simulator): create barebones simulation with invest states ([`04320f6`](https://github.com/MadeInPierre/finalynx/commit/04320f6e32f4d225d68a893c5f325f8109a84dce))

* feat: add envelopes and plot them in dashboard ([`c650ec3`](https://github.com/MadeInPierre/finalynx/commit/c650ec31a92442a931c8cce90555e6a6a17b7fce))

* feat(dashboard): add basic newline support

Still has to be improved, because newlines don&#39;t show up
when folders are collapsed ([`d55e7d2`](https://github.com/MadeInPierre/finalynx/commit/d55e7d263ee847bfc2b85746d5d3cca5b1f0fca4))

* feat(dashboard): nice web tree with colors and icons ([`3d5db42`](https://github.com/MadeInPierre/finalynx/commit/3d5db423942d7ec6a16f7136abf5cfee39c5f8ca))

* feat(portfolio): can set the asset class in parent for all children ([`6bba5df`](https://github.com/MadeInPierre/finalynx/commit/6bba5df09f95faae3174a6624840155a4e250a55))

* feat(dashboard): can now customize the color map ([`8e9b862`](https://github.com/MadeInPierre/finalynx/commit/8e9b8620181f15c2f3d3739ad73bc2ba448378ea))

* feat(dashboard): click on a node to show its asset classes ([`0136d9e`](https://github.com/MadeInPierre/finalynx/commit/0136d9ec68fdbc735a0c3418955efeea502db81d))

* feat(analyzer): add asset classes and plot chart ([`2343b65`](https://github.com/MadeInPierre/finalynx/commit/2343b654373a96ec2abb20f997634d0b4f332462))

### Fix

* fix(fetch): add amounts for lines with same id

If you invested in the same line in multiple accounts, the id stays
the same accross all accounts.
Fod now, it&#39;s best to simply add the amounts
to the first encountered line in the tree ([`8dbc7cf`](https://github.com/MadeInPierre/finalynx/commit/8dbc7cfc95bab7337275d93600e3b4a4bd22d620))

* fix(dashboard): display collapsed/line folders on the web ([`9914a0f`](https://github.com/MadeInPierre/finalynx/commit/9914a0fcbc9c007a080424d99b8842f8b5c2d071))


## v1.6.0 (2023-03-31)

### Chore

* chore: add pull request template

This is simply to help everyone understand what is happening
and keep similar styles between PRs ([`0f0b773`](https://github.com/MadeInPierre/finalynx/commit/0f0b7735badb8170cccfdaff947b990e0c0aa28f))

### Feature

* feat(targets): ratio targets now show the ideal absolute amount to reach ([`8bf0aac`](https://github.com/MadeInPierre/finalynx/commit/8bf0aac72af3e7cb82e9af2f82c4af14bbea2b5b))

* feat(fetch): import precious metals ([`54ce9f6`](https://github.com/MadeInPierre/finalynx/commit/54ce9f6b56c17328b7b8ab20d241065c9714b1ae))

### Fix

* fix(portfolio): simplify newline behavior

Now, it is mandatory to set the newline=True option at the correct node,
nothing is propagated. Simpler to use imo

Also, collapsed folders are now shown as blue but not bold. ([`5071a4d`](https://github.com/MadeInPierre/finalynx/commit/5071a4de19d073b013b424d4d051d3c1e1bf24fc))

* fix(fetch): increase cache time to 12h ([`d41ddb0`](https://github.com/MadeInPierre/finalynx/commit/d41ddb0d187144cac27e705800dc072c2ed6bfe1))


## v1.5.0 (2023-03-23)

### Documentation

* docs(fetch): add key/id usage for identical lines

Provides documentation for #41 ([`ecfddee`](https://github.com/MadeInPierre/finalynx/commit/ecfddee0c5cebe20bb271be74a346b25837e4396))

### Feature

* feat: add cryptos (#43)

* feat: add cryptos

close #42 ([`ea79c75`](https://github.com/MadeInPierre/finalynx/commit/ea79c7599f3c9c64e67a5dd32f000b0833402190))


## v1.4.2 (2023-03-22)

### Fix

* fix(fetch): add support for id differentiation

Closes #41 ([`4f830b8`](https://github.com/MadeInPierre/finalynx/commit/4f830b86f822c37bfa815b302689beaff2133f8b))


## v1.4.1 (2023-03-22)

### Fix

* fix(fetch): ask to reuse credentials if already saved ([`df8bec1`](https://github.com/MadeInPierre/finalynx/commit/df8bec1054daa19fe1e96f55849713977a9750a8))


## v1.4.0 (2023-03-21)

### Chore

* chore(empty): attempt to trigger workflow ([`3a1ce4e`](https://github.com/MadeInPierre/finalynx/commit/3a1ce4e860dc801e25a40815579680195756369a))

### Feature

* feat(dashboard): show the portfolio tree on the web dashboard (#35)

* feat(rich): command-line option to hide fetched data

* chore: readme tweaks

* feat(dashboard): show tree with a simple interface

* feat(fetch): can now cache data locally, defaults to 1h (#36)

* feat(fetch): data is now cached locally (auto-fetch after 1h)

* refactor(fetch): fetch is now in a class, added clear cache option

* refactor(fetch): file cleanup, add docstrings

* chore(release): auto bump version to 1.2.0

Automatically generated by python-semantic-release

* chore(parse): created parse subpackage and structure (#34)

* chore: created parser subpackage and structure

* refactor: small usage and parser docs cleanup

* chore: small syntax cleanup

Automatically generated by python-semantic-release

* fix: forgot dashboard option while merging

* feat: generate portfolio tree in different formats

* feat(dashboard): ugly but functional web tree

* chore(dashboard): draft color style

* refactor(options): changed hide_data to show_data

* refactor: dashboard uses a custom rendering format

* fix(fetch): fix missing unidecode if no cache

* refactor(dashboard): small style tweaks to merge

---------

Co-authored-by: github-actions &lt;github-actions@github.com&gt; ([`fa48bfc`](https://github.com/MadeInPierre/finalynx/commit/fa48bfce6d94f538062a2e3d346f1da1a0340c2c))


## v1.3.0 (2023-03-19)

### Chore

* chore(usage): added help and version usage rules ([`04d3d82`](https://github.com/MadeInPierre/finalynx/commit/04d3d824853980b91298dfd6ce7dd3b11909b5fd))

* chore(parse): created parse subpackage and structure (#34)

* chore: created parser subpackage and structure

* refactor: small usage and parser docs cleanup

* chore: small syntax cleanup

Automatically generated by python-semantic-release ([`56afd8a`](https://github.com/MadeInPierre/finalynx/commit/56afd8affd7b84edf8ac6a9e53636044723381bf))

### Feature

* feat(render): ability to customize the output format (#38)

* feat(render): created base render class and empty docs page

* feat(render): ability to customize the output format

* docs(render): added format documentation ([`97a2462`](https://github.com/MadeInPierre/finalynx/commit/97a24622ee18fa7f1ecf4ad673e57ae69fbd0631))


## v1.2.0 (2023-03-17)

### Ci

* ci(test): fixed dryrun test ([`a6a26f0`](https://github.com/MadeInPierre/finalynx/commit/a6a26f07bc8a30d7de23d6d86c069b449cba34f8))

### Documentation

* docs: remove documentation warning ([`5185495`](https://github.com/MadeInPierre/finalynx/commit/51854955e77c28c3b2c67d5dbed7e15979cd101d))

* docs: write full documentation (#32)

* docs: added autodoc2 for better autogenerated docs

* docs: toctree adjustments

* refactor(mypy): added type hints everywhere

* ci(mypy): add type checking in CI

* ci(mypy): fix call to mypy through python

* ci(mypy): install mypy through pip

* ci(mypy): removed it, looks too strict actually

* docs: fixed API reference title, moved usage from readme

* docs: add docstrings for analyzer, copilot, fetch, simulator

* docs: toc and notes tweaks, documented dashboard

* docs: documented portfolio subpackage root

* docs: documented bucket, constants, folder, hierarchy, portfolio

* docs: documented dashboard, line, node, portfolio, targets ([`835262c`](https://github.com/MadeInPierre/finalynx/commit/835262cac2b44fd6a72be653f2da26ad9f04a882))

* docs: autobuild documentation and upload to Read The Docs (#29)

* docs: created sphinx project and basic structure

* docs: using poetry install

* docs: include submodules in readthedocs build

* docs: set theme to rtd

* docs: using relative image paths in README

* docs: fixed image paths

* docs: created empty modules for analyzer and dashboard

* docs: added project management guidelines

* build(dashboard): add nicegui dependency ([`9c2d2d4`](https://github.com/MadeInPierre/finalynx/commit/9c2d2d4533bbfabf81549a56f65ee6a5dacb3f55))

### Feature

* feat(fetch): can now cache data locally, defaults to 1h (#36)

* feat(fetch): data is now cached locally (auto-fetch after 1h)

* refactor(fetch): fetch is now in a class, added clear cache option

* refactor(fetch): file cleanup, add docstrings ([`86036e2`](https://github.com/MadeInPierre/finalynx/commit/86036e2002a28653ceaba6798815ac641c24aef3))


## v1.1.1 (2023-03-07)

### Ci

* ci(test): trying to call pytest from poetry ([`5b2ab86`](https://github.com/MadeInPierre/finalynx/commit/5b2ab864acf751506eaffdb4a1368ca1be2efb1f))

* ci(test): trying out pytest in CI ([`ddf3490`](https://github.com/MadeInPierre/finalynx/commit/ddf34901107e09341aea20a9fdfd1844ba365eed))

* ci(pr): check conventional naming for PR titles ([`73abe75`](https://github.com/MadeInPierre/finalynx/commit/73abe75d47de2040c81f98b10f20bf1b738a5efa))

### Fix

* fix(fetch): env vars get priority over cookies file ([`f664ed8`](https://github.com/MadeInPierre/finalynx/commit/f664ed876ab35ee3c348b8168994dfbd5f5dd3d6))

### Refactor

* refactor(fetch): slight readability improvements ([`c1a5811`](https://github.com/MadeInPierre/finalynx/commit/c1a58114a1a50ae57afde164f23d473a938edfba))

### Test

* test(dryrun): add a trivial run test of the demo ([`013c466`](https://github.com/MadeInPierre/finalynx/commit/013c46671e10bb807f5f83511b65754321265e4f))


## v1.1.0 (2023-03-05)

### Feature

* feat(fetch): add real estate support (#24)

add real estate support ([`d973fc0`](https://github.com/MadeInPierre/finalynx/commit/d973fc025eeeafc67b11089987b45d73272389b5))


## v1.0.1 (2023-03-04)

### Fix

* fix(dependencies): added unidecode and numpy dependencies

Closes #21 ([`7574eae`](https://github.com/MadeInPierre/finalynx/commit/7574eae6261a3fdd6650c28bd3f530ae1d2d2026))


## v1.0.0 (2023-03-04)

### Breaking

* feat: renamed project to Finalynx

BREAKING CHANGE: Renamed all references of finary_assistant to finalynx ([`4753651`](https://github.com/MadeInPierre/finalynx/commit/4753651ceac0d51514effb0b5ac2723d7dc26d51))

### Chore

* chore(readme): renamed project to Finalynx on README ([`cef81fe`](https://github.com/MadeInPierre/finalynx/commit/cef81fee781405756a7641bfe455a3a626392c19))

* chore(readme): added contributing CLI context ([`08a9558`](https://github.com/MadeInPierre/finalynx/commit/08a955859fdeb680d923e1001509d81629b4168f))

* chore: trying out github sponsors ([`2c87286`](https://github.com/MadeInPierre/finalynx/commit/2c872860dbffc2c31e2716ea6569c43401a288da))

### Fix

* fix(submodules): hopefully correctly moved finary_api ([`6b65d9c`](https://github.com/MadeInPierre/finalynx/commit/6b65d9c97365f325cd4aeb2649bcdd1f6f8a56a8))

* fix: renamed source folder ([`f78318f`](https://github.com/MadeInPierre/finalynx/commit/f78318f5b6ddcc13d97e53586bc6592541817022))


## v0.2.1 (2023-02-21)

### Chore

* chore: trigger ci to test it ([`2f09030`](https://github.com/MadeInPierre/finalynx/commit/2f09030af2fb2f35270e97b9e5404e1329c58667))

* chore(release): auto bump version to 0.2.0 ([`fefbd09`](https://github.com/MadeInPierre/finalynx/commit/fefbd094707bd7f18dc4a5aa44e35bac8c9b0220))

* chore: trying out pre-commit action ([`391b400`](https://github.com/MadeInPierre/finalynx/commit/391b400f7d9a56a5a1089cc3ebd140991c992520))

### Fix

* fix(ci): better release message ([`f097aaf`](https://github.com/MadeInPierre/finalynx/commit/f097aaf52337ef2f456308c720d79746887bb1e3))


## v0.2.0 (2023-02-20)

### Chore

* chore: added more precommit hooks

also set black&#39;s line length to 120, easier to read imo ([`2296918`](https://github.com/MadeInPierre/finalynx/commit/22969184bc48e6bb01e385de0e32dd5956442ade))

* chore: update readme badges ([`fe6f330`](https://github.com/MadeInPierre/finalynx/commit/fe6f3305c6fbd45be5dc8939623b47bd24cc1bca))

### Documentation

* docs(readme): created CONTRIBUTING.md guidelines

Closes #17 ([`75e2d75`](https://github.com/MadeInPierre/finalynx/commit/75e2d758328cce9e18ee02dc2f8d2580677d1bf4))

### Feature

* feat(presentation): updated README&amp;CONTRIBUTING, project looks good!

Closes #15 ([`2267bd3`](https://github.com/MadeInPierre/finalynx/commit/2267bd333242145b55a6393deed6c41014aeaf9f))

### Refactor

* refactor: added pre-commit linting and checks ([`b8cfae4`](https://github.com/MadeInPierre/finalynx/commit/b8cfae4dcee193f649020e507bbdcc0be2e32eb7))


## v0.1.8 (2023-02-20)

### Fix

* fix: static pypi badge ([`ed669ea`](https://github.com/MadeInPierre/finalynx/commit/ed669ea65bf946af2fa7bd8d53b762fa469260e2))


## v0.1.7 (2023-02-20)

### Fix

* fix(ci): forgot to recursively clone the repo ([`3a89f8e`](https://github.com/MadeInPierre/finalynx/commit/3a89f8e015b422ae86a232377f55e97adaf3a2b1))


## v0.1.6 (2023-02-20)

### Fix

* fix(ci): attempting new glob pattern to include finary_api ([`12d81ea`](https://github.com/MadeInPierre/finalynx/commit/12d81ea2c0bc2e7cdeacd4417e2e642cdf7a8d04))


## v0.1.5 (2023-02-20)

### Fix

* fix(ci): include finary_api to the PiPY package ([`6b058c7`](https://github.com/MadeInPierre/finalynx/commit/6b058c7abda05d78896389289f6280e7b7f8a5dc))


## v0.1.4 (2023-02-19)

### Fix

* fix: relative import in module init ([`126fc6e`](https://github.com/MadeInPierre/finalynx/commit/126fc6eda9dbc75b9e1af66ac617e7e46062b6f3))


## v0.1.3 (2023-02-19)

### Fix

* fix: trying to remove custom commit message ([`89bed31`](https://github.com/MadeInPierre/finalynx/commit/89bed317f66a4a27ac83e17586a9e8994abae632))

* fix: manual set to version 0.1.2 ([`d8284d1`](https://github.com/MadeInPierre/finalynx/commit/d8284d13c02bf4a525b9204948968c37a673a7b2))

### Unknown

* 0.1.2 ([`34db82e`](https://github.com/MadeInPierre/finalynx/commit/34db82e6ff968472bab859230055b1db3c0f57d3))


## v0.1.2 (2023-02-19)

### Fix

* fix(ci): attempting to fix missing CI version push ([`277c3f8`](https://github.com/MadeInPierre/finalynx/commit/277c3f8db4b5d2b80e643a83f144cc2a40327a61))


## v0.1.1 (2023-02-19)

### Ci

* ci: removed old PyPI workflow ([`a394a88`](https://github.com/MadeInPierre/finalynx/commit/a394a88654fa016e3e6945d2ce3b3f51746636e1))

### Fix

* fix(build): attempting to fix CI with version source as tags ([`552ad28`](https://github.com/MadeInPierre/finalynx/commit/552ad28e79a99fa824cf751d073a6fa02044795e))

* fix(build): updated dependencies, fixed commitizen format ([`002071a`](https://github.com/MadeInPierre/finalynx/commit/002071aa181ad7ea3b49958db4fe4c9e7bd7ed84))


## v0.1.0 (2023-02-19)

### Ci

* ci: trying poetry and semantic release with tokens ([`120230f`](https://github.com/MadeInPierre/finalynx/commit/120230f858d48465576e0014d85fc81ae3c13ea7))

* ci: added peoptry to toml ([`ae3e84c`](https://github.com/MadeInPierre/finalynx/commit/ae3e84c03d9119ca91b8fbe856eda58a90739274))

### Feature

* feat: forcing bump to 0.1 ([`a2fa623`](https://github.com/MadeInPierre/finalynx/commit/a2fa623d10a1ea20f236bf6784fa21599014de09))


## v0.0.1 (2023-02-19)

### Chore

* chore: setup semantic-release, import version in setup.py ([`4a9307b`](https://github.com/MadeInPierre/finalynx/commit/4a9307b80a1a16267dc9177a00cdf764a76d5d7d))

### Ci

* ci: removed -noop to enable semantic release ([`a70ca69`](https://github.com/MadeInPierre/finalynx/commit/a70ca69047285827e7414e8989d85c6c54d8d630))

* ci: fixed different version numbers ([`1b67f1c`](https://github.com/MadeInPierre/finalynx/commit/1b67f1cbeb83ac2bd4fdb12600c4f3863f71e525))

* ci: Attemping simple semantic release workflow ([`2174d3b`](https://github.com/MadeInPierre/finalynx/commit/2174d3be6566db9f91de8c1122bb682bfb246636))

* ci: attempting peotry, quality and semantic release ([`ae087c0`](https://github.com/MadeInPierre/finalynx/commit/ae087c00350a1bb08c5b4c7d6afed04f7b160cc7))

* ci: Added github action to publish to PyPI ([`faffb73`](https://github.com/MadeInPierre/finalynx/commit/faffb7368e01a3937076eb3596417deb6aeeb1c1))

### Documentation

* docs: Added PyPI badge to README ([`af328e6`](https://github.com/MadeInPierre/finalynx/commit/af328e673691cbca4db73313aba7637ce4f20214))

### Fix

* fix: readme image urls ([`89e1d7b`](https://github.com/MadeInPierre/finalynx/commit/89e1d7b169ffa59e9c869f03da6e740c90acf854))

* fix: cleaner path management, new command option to force signin ([`a29d1bb`](https://github.com/MadeInPierre/finalynx/commit/a29d1bb9bc4c3c0cf8cb152c5205f8e2b142c4f8))

* fix: can now login with cookies without saving credentials ([`5fe8dfe`](https://github.com/MadeInPierre/finalynx/commit/5fe8dfe8645feba0ab2b55c73e610f6b9668472a))

* fix: skip credentials if envars available ([`c888a87`](https://github.com/MadeInPierre/finalynx/commit/c888a8756117d1087b4a943a1e4693ea6c2f7ee7))

### Unknown

* Bumped version and uploaded to pypi! ([`adbd8d4`](https://github.com/MadeInPierre/finalynx/commit/adbd8d4a622862006a32558dc0edab0b84dcc96e))

* moved finary_api to src ([`e43ece6`](https://github.com/MadeInPierre/finalynx/commit/e43ece6bf8b695c659bcafcd88aac8ce6e6ed5ea))

* seutp.py adapted for pypi ([`86ad188`](https://github.com/MadeInPierre/finalynx/commit/86ad1881c30265f72876c3934f2c980c548bf31c))

* Readme pip install instructions ([`7f8be94`](https://github.com/MadeInPierre/finalynx/commit/7f8be945ea8ef3a519440b269f602387c135968d))

* Added setup.py, cleaned structure ([`f02e922`](https://github.com/MadeInPierre/finalynx/commit/f02e92298ed1720f3c6ace254dc4ebe232240c6f))

* Adapted installation instructions ([`6f723cd`](https://github.com/MadeInPierre/finalynx/commit/6f723cda3897b5d2b69c610d62eb23fa82f23102))

* Handling login prompt &amp; file save ([`6082ec8`](https://github.com/MadeInPierre/finalynx/commit/6082ec80148a85bcace759ccf949a6c53b14a051))

* Using syspath and root credentials, removed install script

However, it is still mandatory to use finary_assistant at
the root folder due to finary_api importing the credentials
using relative paths ([`4ce2506`](https://github.com/MadeInPierre/finalynx/commit/4ce2506e280208999700bcd55371f6dbf8122440))

* Fixed submodule ([`c105ee1`](https://github.com/MadeInPierre/finalynx/commit/c105ee1016f9b59cd2fd3d490c9ee81511e2fd41))

* Moved finary_api to submodules folder ([`53a3483`](https://github.com/MadeInPierre/finalynx/commit/53a3483e6bc28f120cbd73b98e2cc2ec3cb0b4d0))

* Expanded/Collapsed folders ([`85fb349`](https://github.com/MadeInPierre/finalynx/commit/85fb34907b936bc842c8819aa213d3c1c2561406))

* Hire me ([`94a8870`](https://github.com/MadeInPierre/finalynx/commit/94a88703af1c2339f7367408277871c3280f8160))

* Created check &amp; documentation scripts ([`d9c2428`](https://github.com/MadeInPierre/finalynx/commit/d9c2428c07dfdbfa798ad3548903ae6117e23209))

* Applied `black` to the entire project ([`89ed2bc`](https://github.com/MadeInPierre/finalynx/commit/89ed2bc6e1511a9ebb21092771b1c5d75560d6bf))

* Removed funding ([`8b4ab6d`](https://github.com/MadeInPierre/finalynx/commit/8b4ab6d42ab3e45104a4fc1ed939a453284f4097))

* Options available through command line ([`168bb0d`](https://github.com/MadeInPierre/finalynx/commit/168bb0d4fc5695f077f1613a0f942d638b8e3cf7))

* Separated demo and assistant files, pretty readme ([`25e8fc2`](https://github.com/MadeInPierre/finalynx/commit/25e8fc2fe8fba370abe73fc21928f01fc30fb4b1))

* README mascot logo! ([`3fd5f22`](https://github.com/MadeInPierre/finalynx/commit/3fd5f22ba15b41e4c61f95f792dac63b99db6e60))

* Merge branch &#39;master&#39; of https://github.com/MadeInPierre/finary_assistant ([`8bd664d`](https://github.com/MadeInPierre/finalynx/commit/8bd664db043c4571b218bea0f7080353795f0620))

* Hide amounts, repo cleanup ([`96f2e90`](https://github.com/MadeInPierre/finalynx/commit/96f2e9056884e5d7da2b5f8b5ec398de393d0d34))

* Create FUNDING.yml ([`beacb83`](https://github.com/MadeInPierre/finalynx/commit/beacb83eb991750dc1724614188f0cca03a8c3e7))

* Started creating template assistant.py ([`2bbe4c0`](https://github.com/MadeInPierre/finalynx/commit/2bbe4c080bfed08d9d44eb5cd7dbb03ebf5ae33e))

* Light theme screenshot ([`7b5c810`](https://github.com/MadeInPierre/finalynx/commit/7b5c810a6582025fd3f71a7449bc4fe698a94fbd))

* Better usage explanations ([`bd061d1`](https://github.com/MadeInPierre/finalynx/commit/bd061d14372800ba9f3a22671ee7a2dfb251fcf2))

* README Instructions tweaks ([`829f091`](https://github.com/MadeInPierre/finalynx/commit/829f091b94d1bc0422629a325a4dd87b8cd32aea))

* Fixed submodules ([`fe97b93`](https://github.com/MadeInPierre/finalynx/commit/fe97b9350517777ac22c2e3c9082b795f622231b))

* Added pythonpath to bashrc ([`8b88654`](https://github.com/MadeInPierre/finalynx/commit/8b88654e4405bdd04cf621aabf83227498a2e551))

* Created submodule and install script ([`a9b02ee`](https://github.com/MadeInPierre/finalynx/commit/a9b02ee730c53f2b9d24756fc6aab6890d6a44b9))

* Lerges readme features and status ([`f6ab26f`](https://github.com/MadeInPierre/finalynx/commit/f6ab26f08f6b8b0d39fc2f50473b81658ffa6837))

* All text is now english ([`85119e6`](https://github.com/MadeInPierre/finalynx/commit/85119e6dda0d2a581c1a7d64c2ae645ffeea6d5f))

* Improved README ([`868a454`](https://github.com/MadeInPierre/finalynx/commit/868a4547eed0587b17b61c7f2e92fe4b7ffd5e9d))

* Cleaned repo, README, and requirements ([`4d492e8`](https://github.com/MadeInPierre/finalynx/commit/4d492e8dd84654460ea574c12c605b08f2b59983))

* Fixed donate button ([`e71e59f`](https://github.com/MadeInPierre/finalynx/commit/e71e59f95fba5a69df5bc6429223ebcbf4b91238))

* Merge branch &#39;master&#39; of https://github.com/MadeInPierre/finary_assistant ([`427e27e`](https://github.com/MadeInPierre/finalynx/commit/427e27e149606c1e21307101423277056a4553c1))

* Added donation button :) ([`f6e0015`](https://github.com/MadeInPierre/finalynx/commit/f6e0015bf42407c6c3fc08947113dd4e4d859c81))

* Create LICENSE ([`a383408`](https://github.com/MadeInPierre/finalynx/commit/a383408e6aa8a31ccbf71c41229db4c2a4c13955))

* Portfolio tweaks ([`2297684`](https://github.com/MadeInPierre/finalynx/commit/229768443348f2263e8b1e9f60bc79b29cea6fb3))

* Created advisor &amp; simulator submodules ([`97b5f70`](https://github.com/MadeInPierre/finalynx/commit/97b5f70a3ccd6064771289732db90e9a334baf45))

* Organized classes in submodules ([`8493f26`](https://github.com/MadeInPierre/finalynx/commit/8493f264568ce4ee2b7d647c365547a9ecf43731))

* Cosmetic improvements (newline) ([`3b53a07`](https://github.com/MadeInPierre/finalynx/commit/3b53a073476cf3999bda4089a8d59bd48f484696))

* Created prehints for targets ([`08ae613`](https://github.com/MadeInPierre/finalynx/commit/08ae6136f1e8b564ce8b17b7428000cb760c449d))

* Created Buckets to share several lines between multiple folders ([`ac89875`](https://github.com/MadeInPierre/finalynx/commit/ac89875d9387b4e40fa5b716857ccccf938d8d70))

* Cleanup gitignore ([`acc7800`](https://github.com/MadeInPierre/finalynx/commit/acc780081383fef6b88545c0dfa0ad22601c099a))

* Cleanup, renaming finary methods ([`8c07b78`](https://github.com/MadeInPierre/finalynx/commit/8c07b781badb3a19e397765fbe686ffdfd6ccd98))

* Added demo image ([`9995f39`](https://github.com/MadeInPierre/finalynx/commit/9995f39e28ee3e9dd816c83667f7c8a60c147974))

* Added README, cleanup ([`4a3472f`](https://github.com/MadeInPierre/finalynx/commit/4a3472f8f3301d1e01b6624945ce9f51d30638ed))

* Separated classes to create a module structure ([`98bdbbb`](https://github.com/MadeInPierre/finalynx/commit/98bdbbbf26e5402fccaf1ba650da7cd345c9b67f))

* Rich tree, targets and finary fetching ([`53a4294`](https://github.com/MadeInPierre/finalynx/commit/53a42941bcd40d333b5f5b9631e85509a6030b77))
