Path: /
Navbar: about
Title: Nuvola Player Project
Snippets: apps gallery, Nuvola News
Datasets: apps
Nuvola_News_Limit: 5

<h1>Nuvola Player</h1>
<div class="row align-items-center justify-content-left">
<div class="col-12 col-lg-8 col-xl-7">
<p class="lead my-1 px-1 text-justify">
<strong>Nuvola Player</strong> provides a tight Linux desktop integration for
<a href="#services">web-based media streaming services such as Spotify, YouTube Music, Apple Music and others</a>.
The goal is to achieve <a href="#features">more native user experience and tighter integration
with Linux desktop environments</a> than usual web browsers can offer.
It tries to feel and look like a native application as much as possible.
Nuvola offers background playback, handling of media key, integration with media player applets,
Last.fm scrobbling, lyrics fetching, and much more.
</p>
</div>
<div class="col-12 col-lg-4 col-xl-3 offset-xl-1">
<div class="row">
<div class="col-12 col-sm-4 col-lg-12 text-center">
<a href="/index/" class="btn btn-primary btn-lg btn-block m-1">Install Nuvola</a>
</div>
<div class="col-6 col-sm-4 col-lg-12 text-center">
<div class="dropdown">
  <button class="btn btn-lg btn-secondary btn-block dropdown-toggle m-1" type="button" id="follownuvola" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">Keep in Touch</button>
  <div class="dropdown-menu" aria-labelledby="follownuvola">
    <a class="dropdown-item" href="https://medium.com/nuvola-news" target="_blank">Read Nuvola News blog</a>
    <a class="dropdown-item" href="https://www.facebook.com/nuvolaplayer" target="_blank">Follow Nuvola on Facebook</a>
    <a class="dropdown-item" href="https://twitter.com/NuvolaPlayer" target="_blank">Follow Nuvola on Twitter</a>
    <a class="dropdown-item" href="https://mastodon.cloud/@nuvola" target="_blank">Follow Nuvola on Mastodon</a>
    <a class="dropdown-item" href="http://eepurl.com/dhxrQT" target="_blank">Subscribe to mailing list</a>
  </div>
</div>
</div>
<div class="col-6 col-sm-4 col-lg-12 text-center">
<a href="/help/" class="btn btn-secondary btn-block btn-lg m-1">Get Help</a>
</div>
</div>
</div>
</div>

<bootstrap>
  <accordion id="acordion" class="my-5">
    <entry show="false" class="border-primary">
       <header class="border-primary">{. fas fa-music} 34 Music streaming 
       services</header>
       <body>
         Nuvola supports the largest amount of [music streaming services](#services).
       </body>
    </entry>
    <entry class="border-primary">
       <header class="border-primary">{. fab fa-linux} Tailor-made for Linux desktop</header>
       <body>
         For us, Linux is not a secondary platform but the system we love and use every day.
        </body>
    </entry>
    <entry class="border-primary">
       <header class="border-primary">{. fas fa-cubes} Cross-distribution sandboxed packages</header>
       <body>
         We provide sandboxed [Flatpak packages](/index/) that can be installed on every modern distribution.
       </body>
    </entry>
    <entry class="border-primary">
       <header class="border-primary">{. fab fa-github} Open source software</header>
       <body>
         The source code of [Nuvola Player](https://github.com/tiliado/nuvolaplayer) and individual
         [integration scripts](https://github.com/topics/nuvola-app) are available on
         [GitHub](https://github.com).
       </body>
    </entry>
  </accordion>
</bootstrap>

Music Streaming Services {: #services}
--------------------------------------

The following web-based music streaming services[^1] are supported by Nuvola Player:

[Snippet: apps gallery]

Desktop Integration {: #features}
-------------------

Although Nuvola should work in all Linux desktop environments, we currently test only
[GNOME](/docs/4/desktops/gnome.html) (Ubuntu, Fedora),
[Cinnamon](/docs/4/desktops/cinnamon.html) (Linux Mint),
[Mate](:4/desktops/mate.html) (Linux Mint),
[Unity](/docs/4/desktops/unity.html) (Ubuntu),
and [Pantheon](/docs/4/desktops/pantheon.html) (elementaryOS).
We hope to explore other desktops in the future.

<div class="row align-items-center justify-content-center text-center">
<div class="col-12 col-md-6 my-2">
<a href="/docs/4/desktops/gnome.html"><img height="192" width="256"
src="https://tiliado.github.io/nuvolaplayer/documentation/images/3.0/gnome/gnome_add_to_favorites[256x192].png"/></a>
<br><a class="btn btn-secondary my-2" href="/docs/4/desktops/gnome.html"
role="button">GNOME</a>
</div>
<div class="col-12 col-md-6 my-2">
<a href="/docs/4/desktops/cinnamon.html"><img height="192" width="330"
src="https://nuvola.tiliado.eu/docs/images/4/desktops/cinnamon/mpris[330x].png"/></a>
<br><a class="btn btn-secondary my-2" href="/docs/4/desktops/cinnamon.html"
role="button">Cinnamon</a>
</div>
<div class="col-12 col-md-6 my-2">
<a href="/docs/4/desktops/pantheon.html"><img height="192" width="320"
src="https://tiliado.github.io/nuvolaplayer/documentation/images/3.1/pantheon/pantheon_dock_thumbs_up_done_with_window[320x].png" /></a>
<br><a class="btn btn-secondary my-2" href="/docs/4/desktops/pantheon.html"
role="button">elementaryOS</a>
</div>
<div class="col-12 col-md-6 my-2">
<a href="/docs/4/desktops/unity.html"><img height="192" width="256"
src="https://tiliado.github.io/nuvolaplayer/documentation/images/3.0/unity/unity_google_play_music_launcher_thumbs_up[256x192].png"/></a>
<br><a class="btn btn-secondary my-2" href="/docs/4/desktops/unity.html"
role="button">Unity</a>
</div>
<div class="col-12 col-md-6 my-2">
<a href="/docs/4/desktops/mate.html"><img height="192" width="256"
src="https://nuvola.tiliado.eu/docs/images/4/desktops/cinnamon/mpris[330x].png"/></a>
<br><a class="btn btn-secondary my-2" href="/docs/4/desktops/mate.html"
role="button">Mate</a>
</div>
</div>

Latest Nuvola News
-------------------

You can follow Nuvola on
[Medium](https://medium.com/nuvola-news),
[Facebook](https://www.facebook.com/nuvolaplayer),
[Twitter](https://twitter.com/NuvolaPlayer),
[Mastodon](https://mastodon.cloud/@nuvola),
or [subscribe to the maling list](http://eepurl.com/dhxrQT)
to receive the latest news.

[Snippet: Nuvola News]

[^1]:
    The streaming services are provided by third parties (the Providers). Nuvola Player project is not affiliated with,
    nor endorsed by, nor supported by the Providers. The service names and logos may be trademarks or registered
    trademarks owned by the Providers.
