# Misca bot
**Mi**rage cinema **sc**hedule **a**ccessing bot - a small tool for checking for upcoming showtimes in mirage cinema theaters.
## Usage
The main idea behind the project is that the bot is convenient to use through third-party apis as well as via spartan command-line interface.
### Cli
That is, the tool can be used via command line interface like this:
```sh
python -m misca trace-schedule -m Служанка -t 14 -n 3
```
The output is presented in the following format:
```sh
Служанка                                           🌎 ЕВРОПОЛИС [14] 🗺️ пр.Полюстровский, д.84а          @ Зал №9               📅 29.05.2022 (Sunday)   🕑 21:20 💰 430
Служанка                                           🌎 ЕВРОПОЛИС [14] 🗺️ пр.Полюстровский, д.84а          @ Зал №9               📅 30.05.2022 (Monday)   🕑 21:20 💰 150
Служанка                                           🌎 ЕВРОПОЛИС [14] 🗺️ пр.Полюстровский, д.84а          @ Зал №9               📅 31.05.2022 (Tuesday)  🕑 21:20 💰 350
```
