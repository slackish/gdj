 % include("admin_header.tpl", title="Main")
    <div class="container">

      <div class="starter-template">
        <h1>Snap that chat</h1>
        <p>Current = <div id="snapchat"></div></p>
        <form name="chatform" action="" onsubmit="return validateChat()">
          <input type="text" id="inputchat" name="chat">
          <input type="submit" value="submit">
        </form>
      </div>

      <script>
      function validateChat() {
          ws.send("1,"+document.forms["chatform"]["inputchat"].value);
          return false;
      }
      // well crap, no relative paths to websockets
      var loc = window.location, ws_uri;
      if (loc.protocol === "https:") {
          ws_uri = "wss:";
      } else {
          ws_uri = "ws:";
      }
      ws_uri += "//" + loc.host + "/websocket";

      var ws = new WebSocket(ws_uri);
    
      ws.onopen = function() {
          ws.send("0,chkin")
      }
      ws.onmessage = function(evt) {
          op = evt.data.split(",", 1);
          op = String(op);
          msg = evt.data.slice(op.length + 1);
          console.log(op.length + 1);
          op = parseInt(op);
          handle_ws(op, msg);
      };

      function handle_ws(op, msg) {
          // nothing really needs to happen here
      }  
      </script>

    </div><!-- /.container -->

 % include("admin_footer.tpl")
