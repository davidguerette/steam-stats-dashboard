## Overview
Steam Stats Dashboard is a Django application that aims to give [Steam](http://store.steampowered.com) users high-level insights into their game collection and play statistics, using aggregated public profile data available on the Steam API.

** This is a work in progress. Current master has functional backend but front end is not yet implemented. **

## Game Collection Insights
This crux of the web app is to give Steam users the ability to see how many PC games they own vs. how many they have ever installed and played. For those unfamiliar, this can be a sobering reality as Steam sales are Internet-famous for offering prices that challenge willpower and wallets alike. It's not uncommon to find a library primarily comprised of unplayed games.

### Currently implemented

* Game collection score: games actually played / total games in library 
* Avg daily time played since joining Steam
* Avg daily time played in the past two weeks
* Top n games by total playtime

## Authentication and user accounts:
All authentication occurs on Steam directly, with Steam acting as an OpenID provider. This login is implemented using [django-allauth](https://github.com/pennersr/django-allauth).

Upon successfully logging in, the user's public 64-bit Steam ID is returned and used the populate the user model. The Steam ID is then used for all subsequent API requests that populate the user profile.
