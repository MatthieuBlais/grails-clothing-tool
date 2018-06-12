manualLabelling = (typeof manualLabelling == 'undefined' || !manualLabelling) ? {} : manualLabelling
validationLabelling = (typeof validationLabelling == 'undefined' || !validationLabelling) ? {} : validationLabelling

manualLabelling.init = function(){
	drawer.init(document.getElementById('canvas'), manualLabelling.getCoordinate)
    manualLabelling.init_clear_button("#clear-button")
    manualLabelling.previous_image("#previous-btn")
    manualLabelling.next_image("#next-btn")
    
    
    manualLabelling.save("#save-btn")
    // var a = $("#current-image-id").data("id")


    $.ajax({url: '/computerVision/loadImages', data:{ label: $("#label").data("value"), offset:0 }, method: "POST", success: function(result){
        	 $("#gallery").append(result)		
        	 asyncPicture()    
        	 manualLabelling.init_click_product(".img-gallery.new")
        	 $("#gallery").find("img").first().addClass("active")
        	 $("#canvas img").attr("src", $("#gallery").find("img").first().attr("src")) 
        	 $("#canvas img").data("counter", $("#gallery").find("img").first().data("counter"))    
           manualLabelling.load_more(".load-more")   
           $("#gallery img.new").removeClass("new")    	 
    	}
	});
}

manualLabelling.getCoordinate = function(x1,y1,x2,y2){
	$("#coordinates-info").html("xmin:"+x1+" ymin:"+y1+" xmax:"+x2+" ymax:"+y2+"")
}

manualLabelling.init_clear_button = function(selector){
  $(selector).click(function(){
     var rectangles = $("#canvas .rectangle")
     if(rectangles.length==0) return
     var rec = $(rectangles[rectangles.length-1])
 	 if($(rec).data('id')){
 	 	var id = $(rec).data('id')
		$.ajax({url: '/computerVision/deleteLabel', data:{ id: id }, method: "POST", success: function(result){ 
				var labels = $("#gallery img[data-counter="+$("#canvas img").data("counter")+"]").data("labels")
				for(var i=0; i<labels.length;i++){
					if(labels[i]["id"]==id) labels.splice(i, 1)
				}        	 
        	}
    	});
	}
     $(rec).remove();
     if($("#canvas .rectangle").length ==0 && $("#gallery img[data-counter="+$("#canvas img").data("counter")+"]").hasClass("labelled")){
     	$("#gallery img[data-counter="+$("#canvas img").data("counter")+"]").removeClass("labelled")
     }
  })
}

manualLabelling.init_click_product = function(selector){
  $(selector).click(function(){
  	 manualLabelling.clear_labels()
  	 $(".img-gallery[data-counter="+(parseInt($("#canvas img").data("counter")))+"]").removeClass("active")
  	 $("#canvas img").attr("src", $(this).data("src"))
  	 $("#canvas img").data("counter", $(this).data("counter"))
  	 $(this).addClass("active")
  	 manualLabelling.reload_features(this)
  })
}

manualLabelling.clear_labels=function(){
  $("#coordinates-info").text("")
  var rectangles = $("#canvas .rectangle")
    for(var i=0; i<rectangles.length ;i++){
    	
    	$(rectangles[i]).remove();
    }
   var list_label = $("#label-list .list-group-item-action")
   for(var i =0; i<list_label.length; i++){
   	   $(list_label[i]).text($(list_label[i]).data("value").charAt(0).toUpperCase() + $(list_label[i]).data("value").substr(1))
   }
}

manualLabelling.next_image =function(selector){
  $(selector).click(function(){
  	 var current = parseInt($("#canvas img").data("counter"))
  	 var image = $(".img-gallery[data-counter="+(current+1)+"]")
  	 $(".img-gallery[data-counter="+(current)+"]").removeClass("active")
  	 console.log(current+1)
  	 if(image){
  	 	manualLabelling.clear_labels()
  	 	$("#canvas img").attr("src", $(image).data("src"))
  	 	$("#canvas img").data("counter", $(image).data("counter"))
  	 	$(image).addClass("active")
  	 	manualLabelling.reload_features(image)
  	 }
  })
}

manualLabelling.previous_image = function(selector){
  $(selector).click(function(){
  	 var current = parseInt($("#canvas img").data("counter"))
  	 var image = $(".img-gallery[data-counter="+(current-1)+"]")
  	 $(".img-gallery[data-counter="+(current)+"]").removeClass("active")
  	 console.log(current-1)
  	 if(image){
  	 	manualLabelling.clear_labels()
  	 	$("#canvas img").attr("src", $(image).data("src"))
  	 	$("#canvas img").data("counter", $(image).data("counter"))
  	 	$(image).addClass("active")
  	 	manualLabelling.reload_features(image)
  	 }
  })
}

manualLabelling.load_more =function(selector){
	
	$(selector+" button").click(function(){
    $(selector).remove()
		$.ajax({url: '/computerVision/loadImages', data:{ label: $("#label").data("value"), offset:$("#gallery img").length }, method: "POST", success: function(result){
            	 $("#gallery").append(result)		
            	 asyncPicture()    
            	 manualLabelling.init_click_product(".img-gallery.new")
               manualLabelling.load_more(".load-more")
            	 $("#gallery").find("img").first().addClass("active")
            	 $("#canvas img").attr("src", $("#gallery").find("img").first().attr("src")) 
            	 $("#canvas img").data("counter", $("#gallery").find("img").first().data("counter"))   
               $("#gallery img.new").removeClass("new")              	 
        	}
    	});
	})
}

manualLabelling.save = function(selector){
	$(selector).click(function(){
		if($("#label-list .list-group-item-action.active").length==0) return
		var coordinates = $("#coordinates-info").text()
		coordinates = coordinates.split(" ")
		$.ajax({url: '/computerVision/saveLabelling', data:{ label: $("#label-list .list-group-item-action.active").data("value"), original:$("#label").data("value"), src:$("#gallery img").attr("src"), xmin: coordinates[0].split(":")[1], ymin: coordinates[1].split(":")[1], xmax: coordinates[2].split(":")[1], ymax: coordinates[3].split(":")[1], width:Math.round($("#canvas img").width()), height: Math.round($("#canvas img").height())  }, method: "POST", success: function(result){
            	 var image = $("#canvas img")
            	 $("#gallery img[data-counter="+$("#canvas img").data("counter")+"]").addClass("labelled")
            	 var labels = []
            	 if($("#gallery img[data-counter="+$("#canvas img").data("counter")+"]").data("labels")!=undefined) labels = $("#gallery img[data-counter="+$("#canvas img").data("counter")+"]").data("labels")
            	 console.log(labels)
            	 labels.push({"name":$("#label-list .list-group-item-action.active").data("value"), 'xmin': coordinates[0].split(":")[1], 'ymin': coordinates[1].split(":")[1], 'xmax': coordinates[2].split(":")[1], 'ymax': coordinates[3].split(":")[1], "id": result.id})
            	$("#gallery img[data-counter="+$("#canvas img").data("counter")+"]").data("labels", labels)
            	console.log($("#gallery img[data-counter="+$("#canvas img").data("counter")+"]").data("labels"))
            	$("#next-btn").click()
        	}
    	});
	})
}

manualLabelling.reload_features=function(image){
	var labels = []
	 	if($(image).data("labels")!=undefined){
	 		labels = $(image).data("labels");
	 		for(var i=0; i<labels.length; i++){
	 			$("#label-list .list-group-item-action[data-value="+labels[i]["name"]+"]").text(labels[i]["name"].charAt(0).toUpperCase() + labels[i]["name"].substr(1)+" - Selected")
	 			var x1 = (parseInt(labels[i]["xmin"]) + Math.round(parseInt($("#canvas img").css("margin-left").replace("px", "")))+15)
	 			var y1 = (parseInt(labels[i]["ymin"]))
	 			var x2 = (parseInt(labels[i]["xmax"]) + Math.round(parseInt($("#canvas img").css("margin-left").replace("px", "")))+15)-x1
	 			var y2 = (parseInt(labels[i]["ymax"]))-y1
	 			$("#canvas").append('<div class="rectangle" data-id="'+labels[i]["id"]+'" style="left: '+x1+'px; top: '+y1+'px; width: '+x2+'px; height: '+y2+'px;"></div>')
	 		}
	 	}
}



/**
*     VALIDATION
**/


validationLabelling.init = function(){

    validationLabelling.unselect_all("#unselect-button")
    validationLabelling.delete_all("#delete-button")
    validationLabelling.crop_top('.crop-button[data-type=top-up]', "up")
    validationLabelling.crop_top('.crop-button[data-type=top-down]', "down")
    validationLabelling.crop_left('.crop-button[data-type=left-left]', "left")
    validationLabelling.crop_left('.crop-button[data-type=left-right]', "right")
    validationLabelling.crop_right('.crop-button[data-type=right-left]', "left")
    validationLabelling.crop_right('.crop-button[data-type=right-right]', "right")
    validationLabelling.crop_bottom('.crop-button[data-type=bottom-up]', "up")
    validationLabelling.crop_bottom('.crop-button[data-type=bottom-down]', "down")
    validationLabelling.save("#save-btn")
    validationLabelling.load_more(".load-more")

    var auto = null 
    var isPrimary = true
    var autoValue = $("#labelling-type .list-group-item-action.active").data("value").split("-")

    if(autoValue[0]=="auto") auto = true
    if(autoValue.length>1){
      if(autoValue[1]=="secondary") isPrimary = false
    }
    // manualLabelling.init_clear_button("#clear-button")
    // manualLabelling.previous_image("#previous-btn")
    // manualLabelling.next_image("#next-btn")
    // manualLabelling.load_more(".load-more")
    
    // manualLabelling.save("#save-btn")
    // var a = $("#current-image-id").data("id")


    $.ajax({url: '/computerVision/loadImages', data:{ label: $("#label").data("value"), offset:0, type:'validation', auto:auto, isprimary:isPrimary }, method: "POST", success: function(result){
           $("#gallery").append(result)   
           asyncPicture()       
           validationLabelling.crop()    
           validationLabelling.click_product("#gallery img.new")     
           $("#offset-info").text($("#gallery img").length)
           $("#total-info").text($("#total").data("value"))
           $("#total").remove()
      }
    });
}


validationLabelling.crop = function(){

  var images = $("#gallery img.new");
  for(var i=0; i<images.length; i++){
      var width = Math.floor($(images[i]).parent().width())
      var height = Math.floor($(images[i]).parent().height())
      if(height==0) height = 200

      var xmin = $(images[i]).data('xmin')
      var ymin = $(images[i]).data('ymin')
      var xmax = $(images[i]).data('xmax')
      var ymax = $(images[i]).data('ymax')

      var marginLeft= Math.round(xmin * width)*-1
      var marginTop = Math.round(ymin * height)*-1
      var totalWidth = Math.round((xmax-xmin) * width)
      var totalHeight = Math.round((ymax-ymin) * height)

      console.log(marginLeft, marginTop)

      $(images[i]).data('original-width', width)
      $(images[i]).data('original-height', height)
      $(images[i]).css('width', width+"px")
      $(images[i]).css('height', height+"px")
      $(images[i]).css('margin-left', marginLeft+"px")
      $(images[i]).css('margin-top', marginTop+"px")
      $(images[i]).parent().css('width', totalWidth+"px")
      $(images[i]).parent().css('height', totalHeight+"px")
  }

}

validationLabelling.click_product = function(selector){
  $(selector).click(function(){
      if($(this).parent().parent().hasClass("active")){
        $(this).parent().parent().removeClass("active")
        if($(this).hasClass("updating")){
          validationLabelling.redraw_cropping(this, "stop")
        }
        $("#selected-info").text($("#gallery .crop-container.active").length)
      }else{
        $(this).parent().parent().addClass("active")
        $("#selected-info").text($("#gallery .crop-container.active").length)
      }
  })
  $(selector).removeClass("new")
}

validationLabelling.unselect_all = function(selector){
  $(selector).click(function(){
      var containers = $(".crop-container.active")
      for(var i=0; i<containers.length; i++){
        if($(containers[i]).find("img").hasClass("updating")){
           validationLabelling.redraw_cropping($(containers[i]).find("img"), "stop")
        }
        $(containers[i]).removeClass("active")
      }
      $("#selected-info").text($("#gallery .crop-container.active").length)
  })
}

validationLabelling.delete_all = function(selector){
  $(selector).click(function(){
      var detections = $(".crop-container.active")
      var ids = []
      for(var i=0; i<detections.length; i++){
        ids.push($(detections[i]).find("img").data("id"))
      }

      $.ajax({url: '/computerVision/deleteDetection', data:{ ids: ids.join(",") }, method: "POST", success: function(result){
             $(detections).remove()    
             $("#selected-info").text($("#gallery .crop-container.active").length) 
        }
      });

  })
}

validationLabelling.crop_top = function(selector, type){
  $(selector).click(function(){
      var detections = $(".crop-container.active")
      var step = 0.05
      if(type=="up") step= (-0.05)
      for(var i=0; i<detections.length; i++){
         if(!$(detections[i]).find("img").hasClass("updating")) $(detections[i]).find("img").addClass('updating')
         var ymin = $($(detections[i]).find("img")[0]).data('ymin') + step
         console.log(ymin, $($(detections[i]).find("img")[0]).data('ymin'))
         if($(detections[i]).find("img").first().data('ymin-update')) { ymin = $($(detections[i]).find("img")[0]).data('ymin-update') + step }
          console.log("YMIN", ymin)
         $($(detections[i]).find("img")[0]).data("ymin-update", ymin)
      }
      validationLabelling.redraw_cropping("img.updating", "updating")
  })
}

validationLabelling.crop_left = function(selector, type){
  $(selector).click(function(){
      var detections = $(".crop-container.active")
      var step = 0.05
      if(type=="left") step= (-0.05)
      for(var i=0; i<detections.length; i++){
          if(!$(detections[i]).find("img").hasClass("updating")) $(detections[i]).find("img").addClass('updating')
          var xmin = $($(detections[i]).find("img")[0]).data('xmin') + step
          if($(detections[i]).find("img").first().data('xmin-update')) { xmin = $($(detections[i]).find("img")[0]).data('xmin-update') + step }
          $($(detections[i]).find("img")[0]).data("xmin-update", xmin)
      }
      validationLabelling.redraw_cropping("img.updating", "updating")
  })
}

validationLabelling.crop_right = function(selector, type){
  $(selector).click(function(){
      var detections = $(".crop-container.active")
      var step = 0.05
      if(type=="left") step=-0.05
      for(var i=0; i<detections.length; i++){
         if(!$(detections[i]).find("img").hasClass("updating")) $(detections[i]).find("img").addClass('updating')
          var xmax = $($(detections[i]).find("img")[0]).data('xmax') + step
          if($(detections[i]).find("img").first().data('xmax-update')) { xmax = $($(detections[i]).find("img")[0]).data('xmax-update') + step }
         
          $($(detections[i]).find("img")[0]).data("xmax-update", xmax)
      }
      validationLabelling.redraw_cropping("img.updating", "updating")
  })
}

validationLabelling.crop_bottom = function(selector, type){
  $(selector).click(function(){
      var detections = $(".crop-container.active")
      var step = 0.05
      if(type=="up") step=-0.05
      for(var i=0; i<detections.length; i++){
         if(!$(detections[i]).find("img").hasClass("updating")) $(detections[i]).find("img").addClass('updating')
         var ymax = $($(detections[i]).find("img")[0]).data('ymax') + step
          if($(detections[i]).find("img").first().data('ymax-update')) { ymax = $($(detections[i]).find("img")[0]).data('ymax-update') + step }
          $($(detections[i]).find("img")[0]).data("ymax-update", ymax)
      }
      validationLabelling.redraw_cropping("img.updating", "updating")
  })
}

validationLabelling.redraw_cropping = function(selector, type){
  var images = $(selector);

  for(var i=0; i<images.length;i++){
      var width = $(images[i]).data('original-width')
      var height = $(images[i]).data('original-height')

      var xmin = $(images[i]).data('xmin')
      var ymin = $(images[i]).data('ymin')
      var xmax = $(images[i]).data('xmax')
      var ymax = $(images[i]).data('ymax')
      if(type!="stop" && $(images[i]).data('xmin-update')) xmin = $(images[i]).data('xmin-update')
      if(type!="stop" && $(images[i]).data('ymin-update')) ymin = $(images[i]).data('ymin-update')
      if(type!="stop" && $(images[i]).data('xmax-update')) xmax = $(images[i]).data('xmax-update')
      if(type!="stop" && $(images[i]).data('ymax-update')) ymax = $(images[i]).data('ymax-update')
      if(type=="stop"){
          $(images[i]).removeData('xmin-update')
          $(images[i]).removeData('ymin-update')
          $(images[i]).removeData('xmax-update')
          $(images[i]).removeData('ymax-update')
      }
      console.log(xmin,ymin,xmax,ymax)

      var marginLeft= Math.round(xmin * width)* -1
      var marginTop = Math.round(ymin * height)*-1
      var totalWidth = Math.round((xmax-xmin) * width)
      var totalHeight = Math.round((ymax-ymin) * height)

      $(images[i]).css('width', width+"px")
      $(images[i]).css('height', height+"px")
      $(images[i]).css('margin-left', marginLeft+"px")
      $(images[i]).css('margin-top', marginTop+"px")
      $(images[i]).parent().css('width', totalWidth+"px")
      $(images[i]).parent().css('height', totalHeight+"px")
  }

}


validationLabelling.save = function(selector){
  $(selector).click(function(){
      var detections = $("#gallery img.updating")
      var data = []
      for(var i=0; i<detections.length; i++){
        var xmin = $(detections[i]).data('xmin')
        var ymin = $(detections[i]).data('ymin')
        var xmax = $(detections[i]).data('xmax')
        var ymax = $(detections[i]).data('ymax')
        if($(detections[i]).data('xmin-update')) xmin = $(detections[i]).data('xmin-update')
        if($(detections[i]).data('ymin-update')) ymin = $(detections[i]).data('ymin-update')
        if($(detections[i]).data('xmax-update')) xmax = $(detections[i]).data('xmax-update')
        if($(detections[i]).data('ymax-update')) ymax = $(detections[i]).data('ymax-update')
        var tmp = [$(detections[i]).data('id'),xmin, xmax, ymin, ymax]
         data.push(tmp.join(","))
      }
      $.ajax({url: '/computerVision/updateDetection', data:{ data: data.join("|") }, method: "POST", success: function(result){
             for(var i=0; i<detections.length; i++){
                var xmin = $(detections[i]).data('xmin')
                var ymin = $(detections[i]).data('ymin')
                var xmax = $(detections[i]).data('xmax')
                var ymax = $(detections[i]).data('ymax')
                if($(detections[i]).data('xmin-update')) xmin = $(detections[i]).data('xmin-update')
                if($(detections[i]).data('ymin-update')) ymin = $(detections[i]).data('ymin-update')
                if($(detections[i]).data('xmax-update')) xmax = $(detections[i]).data('xmax-update')
                if($(detections[i]).data('ymax-update')) ymax = $(detections[i]).data('ymax-update')
                $(detections[i]).data('xmin',xmin)
                $(detections[i]).data('ymin',ymin)
                $(detections[i]).data('xmax',xmax)
                $(detections[i]).data('ymax',ymax)
             }    
             $("#unselect-button").click()
        }
      });
      
  })
}


validationLabelling.load_more =function(selector){
  
  $(selector+".btn").click(function(){
      var auto = null 
      var isPrimary = true
      var autoValue = $("#labelling-type .list-group-item-action.active").data("value").split("-")

      if(autoValue[0]=="auto") auto = true
      if(autoValue.length>1){
        if(autoValue[1]=="secondary") isPrimary = false
      }
     $.ajax({url: '/computerVision/loadImages', data:{ label: $("#label").data("value"), offset:$("#gallery img").length +1 , type:'validation', auto:auto, isprimary:isPrimary }, method: "POST", success: function(result){
           $("#gallery").append(result)   
           asyncPicture()       
           validationLabelling.crop()    
           validationLabelling.click_product("#gallery img.new")     
           $("#offset-info").text($("#gallery img").length)
           $("#total").remove()
      }
    });
  })
}

//width: 400px;height: 300px;margin: -75px 0 0 -100px;