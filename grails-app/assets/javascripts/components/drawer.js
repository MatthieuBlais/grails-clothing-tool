drawer = (typeof drawer == 'undefined' || !drawer) ? {} : drawer


drawer.init = function(canvas, callback){
    function setMousePosition(e) {
        var ev = e || window.event; //Moz || IE
        if (ev.pageX) { //Moz
            mouse.x = ev.pageX + window.pageXOffset;
            mouse.y = ev.pageY + window.pageYOffset;
        } else if (ev.clientX) { //IE
            mouse.x = ev.clientX + document.body.scrollLeft;
            mouse.y = ev.clientY + document.body.scrollTop;
        }
    };

    var mouse = {
        x: 0,
        y: 0,
        startX: 0,
        startY: 0
    };
    var element = null;

    canvas.onmousemove = function (e) {
        setMousePosition(e);
        if (element !== null) {
            element.style.width = Math.abs(mouse.x - mouse.startX -440) + 'px';
            element.style.height = Math.abs(mouse.y - mouse.startY -145 - window.pageYOffset) + 'px';
            element.style.left = (mouse.x - mouse.startX  < 0) ? (mouse.x ) + 'px' : mouse.startX + 'px';
            element.style.top = (mouse.y - mouse.startY  < 0) ? (mouse.y) + 'px' : mouse.startY + 'px';
            console.log(mouse.x+" "+mouse.y)
        }
    }

    canvas.onclick = function (e) {
        if (element !== null) {
            console.log((parseInt(element.style.left.replace("px", ""))))
            var x1 = (parseInt(element.style.left.replace("px", "")) - Math.round(parseInt($("#canvas img").css("margin-left").replace("px", ""))) - 15)
            var y1 = (parseInt(element.style.top.replace("px", "")))
            var feature = callback(x1+"", y1+"", x1+parseInt(element.style.width.replace("px", "")), y1+parseInt(element.style.height.replace("px", "")))
            element.setAttribute("link", feature)
            element = null;
            canvas.style.cursor = "default";
            console.log("finsihed.");
        } else {
            console.log("begun."+mouse.x+" "+mouse.y);
            mouse.startX = mouse.x-440;
            mouse.startY = mouse.y-145-window.pageYOffset;
            element = document.createElement('div');
            element.className = 'rectangle'
            element.style.left = mouse.x + 'px';
            element.style.top = mouse.y + 'px';
            canvas.appendChild(element)
            canvas.style.cursor = "crosshair";
        }
    }
}