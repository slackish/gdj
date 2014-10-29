<html>

<style type="text/css">
html, body {
    background-color: #000000;
}

.wrapper {
    min-height: 100%;
    height: auto !important;
    height: 100%;
    margin: 0 auto -15%;
}

#img{
    position: fixed;
    width: 100%;
    height: 100%;
    max-width: 100%;
    max-height: 100%;
    background: url("/static/logo.png") no-repeat center center fixed;
    -webkit-background-size: contain;
    -moz-background-size: contain;
    -o-background-size: contain;
    background-size: contain;
}

#logo {
    position: fixed;
    opacity: 1;
    z-index: 2;
    right: 5px;
    bottom: 5px;
    width: 15%;
    height: 15%;
    max-height: 15%;
    max-width: 15%;
    background: url("/static/logo.png") no-repeat center center fixed;
    -webkit-background-size: contain;
    -moz-background-size: contain;
    -o-background-size: contain;
    background-size: contain;
}


</style>

<!--
<div class="body">
    <img src='next'>
</div>

--!>

<head>
    <meta charset="UTF-8">
    <script type="text/javascript" src="/static/jquery/dist/jquery.min.js"></script>
</head>


<body>
    <div id="logo"></div>
    <div id="img"></div>
    

    <script>
        var next_url;
        var next_time;
        var state = "directive";

        newDirective();

        function newDirective() {
            console.log("new directive called");
            $.ajax({
                type: 'get',
                url: '/next',
                dataType: 'json',
                success: function(json){
                    next_time = json['switchTime'];
                    next_time = next_time * 1000;
                    next_url = json['nextImg'];
                    cur_time = new Date().getTime();
                    offset = next_time - cur_time;
                    console.log("offset is " + offset);
                    console.log("next_time is " + next_time);
                    console.log("cur_time is " + cur_time);
                    // preload
                    preloadimg = new Image();
                    preloadimg.src = next_url;
                    setTimeout(swapGif, offset);
                },
                error: function(xhr, ajaxOptions, thrownError) {
                    setTimeout(newDirective, 1000);
                    console.log(xhr.status);
                    console.log(thrownError);
                }
            });
        }
        
        function swapGif() {
            console.log("swapGif called");
            console.log(next_url);
            $("#img").fadeOut(function(){
                var imgstyle = document.getElementById("img").style;
                imgstyle.background = "url(" + next_url + ") no-repeat center center fixed";
                imgstyle["-webkit-background-size"] = "contain";
                imgstyle["-moz-background-size"] = "contain";
                imgstyle["-o-background-size"] = "contain";
                imgstyle["background-size"] = "contain";
            $("#img").fadeIn();
            });
            setTimeout(newDirective, 1000);
        };

    </script>

</body>


</html>
