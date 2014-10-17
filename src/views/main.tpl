<html>

<style type="text/css">
body {
    background-color: #000000;
}

body.img {
    position: center;
    max-height: 100%;
    max-width: 100%;
    z-index: 0;
}

img.logo {
    position: bottom right;
    max-width: 15%;
    max-height: 15%;
    z-index: 1;
}

img.body {
}

</style>

<!--
<div class="body">
    <img src='next'>
</div>

--!>

<head>
    <meta charset="UTF-8">
    <title>Gif-player test page</title>
    <link rel="stylesheet" href="/static/gif-player/css/gif-player.css" type="text/css" media="screen">

    <script type="text/javascript" src="/static/jquery/dist/jquery.min.js"></script>
    <script type="text/javascript" src="/static/gif-player/js/src/gif-movie.js"></script>
    <script type="text/javascript" src="/static/gif-player/js/src/gif-player.js"></script>
    <script type="text/javascript" src="/static/gif-player/js/src/gif-player-plugin.js"></script>
</head>


<body>
    <a href="/static/imgs/halloween/fVsumll.gif" class="gif-player" id="g1">
       <img src="/static/logo.png" alt="huh, this should be playing" width="400" height="225">
    </a>
    <a href="/static/imgs/halloween/PCCigiJ.gif" class="gif-player" id="g2">
       <img src="/static/logo.png" alt="huh, this should be playing" width="400" height="225">
    </a>
                    
                    
    <script>
      $(function() {
         $('.gif-player').gifPlayer(play=true, fullscreen=true);
      });

      function fireEvent(element, eventName) {
         var event;

         if (document.createEvent) {
            event = document.createEvent("HTMLEvents");
            event.initEvent(eventName, true, true);
         } else {
            event = document.createEventObject();
            event.eventType = eventName;
         }

         event.eventName = eventName;

         if (document.createEvent) {
           element.dispatchEvent(event);
         } else {
           element.fireEvent("on" + event.eventType, event);
         }
      }

      var g1 = document.getElementById("g1");
      var g2 = document.getElementById("g2");
      var state = "g1";
      var delta = 5000;

      function swapGifs() {
          if ( state == "g1" ) {
              fireEvent(g1, "playGif");
              fireEvent(g1, "fscreenGif");
              fireEvent(g2, "stopGif");
              fireEvent(g2, "fscreenGif");
              state = "g2";
          } else {
              fireEvent(g2, "playGif");
              fireEvent(g2, "fscreenGif");
              fireEvent(g1, "stopGif");
              fireEvent(g1, "fscreenGif");
              state = "g1";
          }
          setTimeout(swapGifs, delta);
      }
      setTimeout(function(){fireEvent(g2, "fscreenGif")}, delta);
      setTimeout(swapGifs, delta);

    </script>

</body>

<div class="logo">
    <img src='/static/logo.png'>
</div>

</html>
