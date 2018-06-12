window.addEventListener('load', function(){
    asyncPicture()
}, false)


function asyncPicture(){
	var allimages= document.getElementsByTagName('img');
    for (var i=0; i<allimages.length; i++) {
        if (allimages[i].getAttribute('data-src') && (!allimages[i].getAttribute('src') || allimages[i].getAttribute('src') == "/assets/placeholder.jpg" )) {
            allimages[i].setAttribute('src', allimages[i].getAttribute('data-src'));
        }
    }
}