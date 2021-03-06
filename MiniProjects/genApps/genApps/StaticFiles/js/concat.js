/*********************************
 And after a long time. I have decideed to devlpm my Own JS library 
 It's a collection of FAQ of js ?
 TOC is as below
**********************************/
/* This is base.js file */

/*********************************



 After serach a lot I decide  to write my own Operational Trsformbation chnage set library.,
 It should support:
 1. Crete OT diff
   a) Line by Line Diff to support line merge.
   b) Should have word offset
   c) Easy and fast merge.
 2. Apply OT to a text with uneven length
 3. [EX] Versioning
 4. [Ex] Serialization of chnage set.
 Dependency : 
**********************************/
/*
function dipankarOT(ops) {
  this.line_chnage_count=0
  this.lines =[]
  
  //define methods on lines
  this.addLineChange = function(lc){ this.lines.push(lc)}
  this.print =  function(){
    console.log('Here is the change set:')
    for (i = 0; i < lines.length; i++) { 
      console.log(lines[i])
    }
  }
  
  // buildLineDiff: Will generate our Own way to line diff.
  // output: An array of operation [..ops]
  // Ops =[operation,next/prev efefcted word, old cur index]
  
  this.buildLineDiff = function(line1,line2,mode){
    var dmp = new diff_match_patch();
    if (mode=='word'){
       diff = dmp.diff_main(line1, line2);//TBD
    }
    else{
      diff = dmp.diff_main(line1, line2);
    }
    console.log(diff)
    
    var DIFF_DELETE = -1;
    var DIFF_INSERT = 1;
    var DIFF_EQUAL = 0;
    
    var ops = [],curlen = 0;
    char_count_change=0;
    diff.forEach(function(d) {
      
      curlen+= d[1].length;
      
      if (DIFF_DELETE == d[0]) {
        ops.push({a:'del',el:d[1].length,cl:curlen,w:d[1]})
        char_count_change -= d[1].length;
      }      
      if (DIFF_INSERT == d[0]) {
        ops.push({a:'ins',el:d[1].length,cl:curlen,w:d[1]})
        char_count_change += d[1].length;
      }      
      if(DIFF_EQUAL == d[0]) {
       ops.push({a:'skip',el:d[1].length,cl:curlen,w:d[1]})
      }
    })
    if(line1.length+char_count_change != line2.length){console.log("Warn: Diff Generation failed!");}
    
    return { ops:ops,char_count_change:char_count_change,old_len:line1.length,new_len:line1.length+char_count_change};
    // Ops =[operation,next/prev efefcted word, old cur index]
  }
  
// this is my Merge Algorithm
// TBD
//  
//
  this.mergeToLine = function(old_line,diff,option='fource'){
    if(old_line.length != diff.old_len){
      console.log('Warn:[OldTextChange]# old text length doent match with line length');
    }
    old_max_len = old_line.length
    new_line=''
    new_line_len=0
    old_idx=0;
    diff.ops.forEach(function(op) {
      if (op.a == 'skip') {
        new_line += old_line.substring(old_idx,op.el+1)
        old_idx += op.el;
      }
      if (op.a == 'ins') {
        new_line += op.w;
      }
      if (op.a == 'del') {
        old_idx+=op.el; //ignore this part.. increase old index.
      }
    })
    new_line += old_line.substring(old_idx,old_line.length)
    //TODO -validation.
    return new_line
  
  }
  
  
}
//Unit Test Here..
t1 = 'I am don '
t2 = 'i am hanuman'
dot=new dipankarOT()
df = dot.buildLineDiff(t1,t2)
console.log(df)
t3= 'I am don '
dot.mergeToLine(t3,df)
*/

/* This file contsins common JS */
$(document).ready(function() {
 
/* ============== Start of code ============== */


/*== Q2 sliding tabs ========================= */
$("#hr-tab .tabs li").click(function(){
  console.log("#hr-tab .data div."+$(this).attr("target-id")) 
  $("#hr-tab .tabs li").removeClass("active");
  $(this).addClass("active");
  
  $("#hr-tab .data div").hide();
  $("#hr-tab .data div#"+$(this).attr("id")).fadeIn("slow");  
  
});


/*==========Q5 popup ================ */
 /*
$('[data-popup-target]').click(function () {
        $('html').addClass('overlay');
        var activePopup = $(this).attr('data-popup-target');
        $(activePopup).addClass('visible');
});
$(document).keyup(function (e) {
        if (e.keyCode == 27 && $('html').hasClass('overlay')) {
            clearPopup_box();
        }
});

$('.popup-exit').click(function () {clearPopup_box(); });
$('.popup-overlay').click(function () { clearPopup_box();});

function clearPopup_box() {
  $('.popup.visible').addClass('transitioning').removeClass('visible');
  $('html').removeClass('overlay');
  setTimeout(function () {
    $('.popup').removeClass('transitioning');
    }, 200);
  }
  
 */
/*Q5A -- POPUP-SIDEBAR-- */

$('.popup-sidebar-link').click(function () {
        $('html').addClass('overlay');
        $('.popup-sidebar-data').animate({width:"400px"});
});

$(document).keyup(function (e) {
  if (e.keyCode == 27 && $('html').hasClass('overlay')) {             clear_popup_sidebar() ;
        }
});
$('.popup-exit').click(function () { clear_popup_sidebar() ;});
$('.popup-overlay').click(function () { clear_popup_sidebar();});

function clear_popup_sidebar() {
  //$('.popup-sidebar-data').addClass('hide');
  $('.popup-sidebar-data').animate({width:"0px"});
  $('html').removeClass('overlay');
}
  

/*Q. 11 youtube bar */
$({property: 0}).animate({property: 105}, {
    duration: 4000,
    step: function() {
        var _percent = Math.round(this.property);
        $('#progress').css('width',  _percent+"%");
        if(_percent == 105) {
            $("#progress").addClass("done");
        }
    },
    complete: function() {
       // alert('complete');
    }
});

/*Q13 Majic line */
/*
 var $el, leftPos, newWidth,
        $mainNav = $("#example-one");
    
    $mainNav.append("<li id='magic-line'></li>");
    var $magicLine = $("#magic-line");
    
    $magicLine
        .width($(".current_page_item").width())
        .css("left", $(".current_page_item a").position().left)
        .data("origLeft", $magicLine.position().left)
        .data("origWidth", $magicLine.width());
        
    $("#example-one li a").hover(function() {
        $el = $(this);
        leftPos = $el.position().left;
        newWidth = $el.parent().width();
        $magicLine.stop().animate({
            left: leftPos,
            width: newWidth
        });
    }, function() {
        $magicLine.stop().animate({
            left: $magicLine.data("origLeft"),
            width: $magicLine.data("origWidth")
        });    
    });
*/
/*Q14 Colupsable List*/
$("#CollapseList .item").click(function(){

  var x = $(this).find(".details").hasClass("hide");
  $("#CollapseList .details").addClass("hide"); //hide all
  
  if(x){
//  $(this).find(".details").slideDown( 'slow')
  $(this).find(".details").removeClass("hide") //show this
  }
});


/* ============== End of code ============== */
})


 
/* ToothStrap JS Effect Here */
/* This file contsins common JS */
$(document).ready(function() {
 
/* ============== Start of code ============== */

/**************** usefull functions here **************/
/* 
ele: element to add classm 
cls:which calls to be added
how: up-go up
cur: pass this variable for refer
Example: onclick="toggleClass('.has-sub','opened','up',this)"
*/

window.addClass = function(ele,cls,how,cur){
  console.log('>>> adding calss '+cls+' to element <'+cur+'>on<'+how+'>');
  var x;
  if(how == 'up'){ x=$(cur).closest(ele);}
  else{  x = $(ele) }
  console.log('Effeted Element :')
  console.log(x);
  x.addClass(cls);  
 };
window.removeClass = function(ele,cls,how,cur){
  console.log('>>> removing calss '+cls+' to element '+ele+'on'+how);
  var x;
  if(how == 'up'){ x=$(cur).closest(ele); }
  else{ x = $(ele) }   
  x.removeClass(cls);
 };

window.toggleClass = function(ele,cls,how,cur){
  console.log('>>> toggleing calss '+cls+' to element '+ele+'on'+how);
  var x;
  if(how == 'up'){ x=$(cur).closest(ele); }
  else{  x = $(ele) }
  
  console.log('Effeted Element :')
  console.log(x);
  if( x.hasClass(cls)) {
    x.removeClass(cls);
  }
  else{
    x.addClass(cls);
  }
 };
 
/* serializeFrom: Extract the value of a from  */
window.serializeFrom  = function(ele){
  var a = $(ele).serializeArray();
  var m = {}
  a.forEach(function(entry) {
    if(m.hasOwnProperty(entry.name)){
       m[entry.name]=m[entry.name]+','+entry.value
    }
    else{
       m[entry.name]=entry.value
    }
  });
  return m;
}
/* mergeObj: Merge two Object */
window.mergeObj  = function (obj1,obj2){
    var obj3 = {};
    for (var attrname in obj1) { obj3[attrname] = obj1[attrname]; }
    for (var attrname in obj2) { obj3[attrname] = obj2[attrname]; }
    return obj3;
}

/******** end usefull functions here **************/

/************  table Resize  ************************/
window.tableResize = function(ele){
console.log('tableResize called for '+ele);
// Change the selector if needed
if (ele){
  var $table = $(ele)
}
else{
var $table = $('.table.scroll')
}
var $bodyCells = $table.find('tbody tr:first').children(), colWidth;

// Adjust the width of thead cells when window resizes
    // Get the tbody columns width array
    colWidth = $bodyCells.map(function() {
        return $(this).width();
    }).get();
    
    // Set the width of thead columns
    $table.find('thead tr').children().each(function(i, v) {
        $(v).width(colWidth[i]);
    });    
    
    //Just do a liner distribution
    $table.find('tr').children().each(function(i, v) {
      $(v).width($('.table.scroll').width()/$bodyCells.length -2);
    }); 
}
/************  table Resize End Here ************************/


/*== Q2 sliding tabs ========================= */
//$("#div-nav-bar .data>div).hide();
$(".menu a").click(function(){
  var uid=$(this).attr('targetid')
  tab = $(this).closest('.tab') 

  tab.find('.menu >a').removeClass('active')
  $(this).addClass('active')
  tab.find('.data > div').removeClass('active')
  tab.find('.data > #'+uid).addClass('active')

});

/*******************  fly out **************/
$(".onflyout").toggle('click', function(){
var a= $(this).data('flyout');
$("#flyout."+a.cls).css("top",a.top);
$("#flyout."+a.cls).css("left",a.left);
}); 

/* ============== End of code ============== */


/**********************Start Overlay-Popup ******************/
 window.showPopup = function(idname){
        $('html').addClass('overlay');
        $(idname).addClass('visible');
        $(idname).addClass('animated');
        if($(idname).hasClass('RightSlide')){
        $(idname).removeClass('lightSpeedOut').addClass('lightSpeedIn');
        }
        if($(idname).hasClass('fromTop')){
        $(idname).removeClass('fadeOutUp').addClass('fadeInDown');
        }
        else{
          $(idname).removeClass('flipOutY').addClass('flipInY');
        }
        
}

$(document).keyup(function (e) {
        if (e.keyCode == 27 && $('html').hasClass('overlay')) {
            clearPopup_box();
        }
});

$('.popup-exit').click(function () {clearPopup_box(); });
$('.popup-overlay').click(function () { clearPopup_box();});

function clearPopup_box() {
  if($('.popup.visible').hasClass('RightSlide')){
  $('.popup').removeClass('lightSpeedIn').addClass('lightSpeedOut');
  }
  else if($('.popup.visible').hasClass('fromTop')){
  $('.popup').removeClass('fadeInDown').addClass('fadeOutUp');
  }
  else{
  $('.popup').removeClass('flipInY').addClass('flipOutY'); 
  }
  setTimeout(function(){
    $('.popup.visible').removeClass('visible');
    $('html').removeClass('overlay');
    },1000);
}
  
/**********************Start Overlay-Popup ******************/


/*****************  Start full screen ***********************/
window.toggleFullScreen  = function(elem) {
    if ((document.fullScreenElement && document.fullScreenElement !== null) || (document.msfullscreenElement && document.msfullscreenElement !== null) || (!document.mozFullScreen && !document.webkitIsFullScreen)) {
        if (elem.requestFullScreen) {
            elem.requestFullScreen();
        } else if (elem.mozRequestFullScreen) {
            elem.mozRequestFullScreen();
        } else if (elem.webkitRequestFullScreen) {
            elem.webkitRequestFullScreen(Element.ALLOW_KEYBOARD_INPUT);
        } else if (elem.msRequestFullscreen) {
            elem.msRequestFullscreen();
        }
       $( "body" ).addClass( "fullscreen" )
    } else {
        if (document.cancelFullScreen) {
            document.cancelFullScreen();
        } else if (document.mozCancelFullScreen) {
            document.mozCancelFullScreen();
        } else if (document.webkitCancelFullScreen) {
            document.webkitCancelFullScreen();
        } else if (document.msExitFullscreen) {
            document.msExitFullscreen();
        }
         $( "body" ).removeClass( "fullscreen" )
    }
}
/************** End of fll screen ******************************/

/***************************  Mouse Move *********************/

window.addClassOnMouseMoveZone = function(){  
  var mie = (navigator.appName == "Microsoft Internet Explorer") ? true : false;
  if (!mie) {
       document.captureEvents(Event.MOUSEMOVE);
       document.captureEvents(Event.MOUSEDOWN);
  }
  document.onmousemove = function (e) {mousePos(e);};
  document.onmousedown = function (e) {mouseClicked();};
  var mouseClick;
  var keyClicked;
  var mouseX = 0;
  var mouseY = 0;

  function mousePos (e) {
      if (!mie) {
          mouseX = e.pageX; 
          mouseY = e.pageY;
      }
      else {
          mouseX = event.clientX + document.body.scrollLeft;
          mouseY = event.clientY + document.body.scrollTop;
      }
      // Write your action here..
      if (mouseX <15){$('#menu').addClass('show') } 
      if (mouseX >100){$('#menu').removeClass('show') } 
  }
  function mouseClicked()
  {
    console.log(' mouse click is not impelmenbted yet !')
  }
}
//addClassOnMouseMoveZone (); <<<<<<<<< donot enable this 
/*************************** End of  Mouse Move *********************/
/****************** Menu *******************/
window.toggleMenu  = function(elem){
 if($(".menu").hasClass("hide-sidebar"))
 { //show it.. 
 $(".menu").removeClass("hide-sidebar");
 $(".menu .nav span").fadeIn("slow", function(){
   $(".menu .logo").fadeIn("slow");
   });
 }
 else{
 //hide it
 $(".menu .logo").fadeOut("slow",function(){
    $(".menu .nav span").hide();
 });
 $(".menu").addClass("hide-sidebar");
 }
}

/********************Action Hide and Show on Hover and Click ***************/
/* This will add / remove class on hover or click */
 $('.toggle_open_class_on_hover_click').bind({
  mouseenter: function(e) {
  // Hover event handler
  $(this).addClass("open")
  },
  mouseleave: function(e) {
   $(this).removeClass("open")
  },
  click: function(e) {
  if($(this).hasClass("open")){
  $(this).removeClass("open");
  }
  else{
  $(this).addClass("open")
  }
  },
  blur: function(e) {
  $(this).removeClass("open")
  }
 });
/********************** End of this action *********************************/


/***************** Change the Body color ***********************************/
window.autoColor= (function(){
	var hexacode = ['#2B60DE', '#6960EC', '#38ACEC', '#ED7839', '#7DFDFE','#FF7D7D','#347C2C','#BCE954','#AF7817','#493D26','#6F4E37','#6F4E37','#800517'],
	el = document.getElementById('autocolor').style,
	counter = -1,
	hexalen = hexacode.length;
	function auto(){
		el.backgroundColor = hexacode[counter = ++counter % hexalen];
	}
	setInterval(auto, 10000);
});
// shoud call this fynction autoColor();
/***************** End Change the Body color ********************************/
 
/* End of document ready*/ 
/* End of document ready*/ 
})

/******************  Generated Ajax Call Back ***************************
* Example : AjaxCommand(MODEL_NAME,[action],{param},function success(a){})
* AjaxCommand('code','getall',{},function(a){alert(a.msg);})
* AjaxCommand('code','get',{'id':1},function(a){alert(a.msg);})
* AjaxCommand('code','create',{'id':1},function(a){alert(a.msg);})
* AjaxCommand('code','update',{'id':1},function(a){alert(a.msg);})
**************************************************************************/
function AjaxCommand(model,action,param,cb_success,cb_error){
  var url =''
  var type='post'
  /* TODO: We can support many more */
  if (action=="getall"){ url = '/api/'+model+'/',type='get' }
  else if (action=="get"){ url = '/api/'+model+'/'+param.id+'/',type='get' }
  else if(action=="create"){ url = '/api/'+model+'/' }
  else if(action=="update"){ url = '/api/'+model+'/'+param.id+'/' }
  else if (action=="delete"){ url = '/api/'+model+'/'+param.id+'/' }
  else{ url = '/api/cleancode/invalid/' }  
  
  /*Ajax call is here */
  $.ajax({ 
    url: url,
    type: type,
    data: param,
    contentType: 'application/x-www-form-urlencoded; charset=utf-8',  
    processData: true,
    success: function( data, textStatus, jQxhr ){
      console.log(data)
      if (cb_success != undefined){
      cb_success(data)
      }
    },
    error: function( jqXhr, textStatus, errorThrown ){
      console.log( errorThrown ); 
      if (cb_success != undefined){
        cb_error(data)
      }
    } 
  });
}
/******************  Generated Ajax Call Back ****************************/

/****************** Tree Menu Js ************************/
/* It will do action(add/remove/toggle) a class(class/id) on all sibling of ele(id/class) based on a cond(condition -like hasclass cond)

ele- element whose sibling to be effected
cls - class to be added /removed
cond - if that id has this cls
action - either add/remove/toggle
//TODO : Amke it Generalized. Action in Bulk. 
*/

function actionClassOnSiblingButNotThis(ele,cls,cond,action){
 var sib= ele.parentNode.childNodes
 for( i =0;i<sib.length;i++)
 {
   if( sib[i] != ele && $(sib[i]).hasClass(cond)){
     if(action=='toggle'){$(sib[i]).toggleClass(cls)}
     if(action=='add'){$(sib[i]).addClass(cls)}
     if(action=='remove'){$(sib[i]).removeClass(cls)} 
   }
 }
}

function recur(ll,level){
  var h='<ul>'
  ll.forEach(function(e) {
    var has_child = (e.hasOwnProperty('child') && e.child.length != 0)
    if (has_child){
      h+='<li class="has_child"  style="margin-left:'+level*18+'px">'
      h+='<i class="jstree-icon jstree-ocl"></i>'
      h+='<a onclick="actionClassOnSiblingButNotThis(this.parentNode,\'expanded\',\'has_child\',\'remove\');toggleClass(\'li\',\'expanded\',\'up\',this); " ><i class="fa fa-folder-open-o"></i> '+e.name+'</a>'
      h+= recur(e.child,1)
      h+='</li>'
    }
    else{
      h+='<li style="margin-left:'+level*18+'px">'
      h+='<i class="jstree-icon jstree-ocl"></i>'
      h+='<a> <i class="fa fa-file-o"></i>'+e.name+'</a>'
      h+='</li>'
    }    
  });
  h += '</ul>'
  return h;
}

var a=[
  { 'name':'dd1' },
  {'name':'dd2'},
  {'name':'dd3','child':
    [
        { 'name':'dd31' },
        {'name':'dd32'},
        {'name':'dd33','child':
          [
            { 'name':'dd331'}
          ]
        },
        {'name':'dd33','child':
          [
            { 'name':'dd331'}
          ]
        },
        {'name':'dd33','child':
          [
            { 'name':'dd331'}
          ]
        },
        {'name':'dd33','child':
          [
            { 'name':'dd331'}
          ]
        },
        {'name':'dd33','child':
          [
            { 'name':'dd331'},
            {'name':'dd33','child':
              [
                { 'name':'dd331'},
                {'name':'dd33','child':
                  [
                    { 'name':'dd331'},
                    {'name':'dd33','child':
                              [
                                { 'name':'dd331'}
                              ]
                    }
                  ]
                }
              ]
            }
          ]
        }
    ]
  }
  ]



var html = recur(a,0)
$(document).ready(function() {
$("#test").html(html)

});
/******************  End of Tree Menu Js *****************/

/************************** Auto Hide Popup ***********************/
function autohideMsgPopUp(html,sec) {
  if (sec == undefined){ sec = 2;}
  $(".autohideMsgPopUp").html(html);
  $(".autohideMsgPopUp").addClass('active')
  setTimeout(function(){  $(".autohideMsgPopUp").removeClass('active'); }, sec*1000);
}
//shoub be Moved to common lib
function autohide(id,sec) {
  if (sec == undefined){ sec = 1;}
  $(id).addClass('active')
  setTimeout(function(){  $(id).removeClass('active'); }, sec*1000);
}
/**********************************************************************/



/******************  Bubble Games *****************/

function bubbles() {  
  // Settings
  var min_bubble_count = 20, // Minimum number of bubbles
      max_bubble_count = 60, // Maximum number of bubbles
      min_bubble_size = 3, // Smallest possible bubble diameter (px)
      max_bubble_size = 12; // Maximum bubble blur amount (px)
  var clr=['red','green','blue','yellow','black']
  
  // Calculate a random number of bubbles based on our min/max
  var bubbleCount =  min_bubble_count + Math.floor(Math.random() * (max_bubble_count + 1));
  
  var $bubbles = $('.bubbles'); 
  // Create the bubbles
  for (var i = 0; i < bubbleCount; i++) {
    $bubbles.append('<div class="bubble-container"><div class="bubble"></div></div>');
  }  
  // Now randomise the various bubble elements
  $bubbles.find('.bubble-container').each(function(){    
    
    var pos_rand = Math.floor(Math.random() * 101); // Randomise the bubble positions (0 - 100%)   
    var size_rand = min_bubble_size + Math.floor(Math.random() * (max_bubble_size + 1));   // Randomise their size 
    var delay_rand = Math.floor(Math.random() * 16);    // Randomise the time they start rising (0-15s)
    var speed_rand = 3 + Math.floor(Math.random() * 9);   // Randomise their speed (3-8s)    
    var bdr_clr = clr[Math.floor(Math.random() * clr.length)];   // Randomise their speed (3-8s)   
    var blur_rand = 0//Math.floor(Math.random() * 3);  // Random blur 
    
    
    // Cache the this selector
    var $this = $(this);    
    // Apply the new styles
    $this.css({
      'left' : pos_rand + '%',      
      '-webkit-animation-duration' : speed_rand + 's',
      '-moz-animation-duration' : speed_rand + 's',
      '-ms-animation-duration' : speed_rand + 's',
      'animation-duration' : speed_rand + 's',      
      '-webkit-animation-delay' : delay_rand + 's',
      '-moz-animation-delay' : delay_rand + 's',
      '-ms-animation-delay' : delay_rand + 's',
      'animation-delay' : delay_rand + 's',      
      '-webkit-filter' : 'blur(' + blur_rand  + 'px)',
      '-moz-filter' : 'blur(' + blur_rand  + 'px)',
      '-ms-filter' : 'blur(' + blur_rand  + 'px)',
      'filter' : 'blur(' + blur_rand  + 'px)'
      
    });    
    $this.children('.bubble').css({
      'width' : size_rand + 'px',
      'height' : size_rand + 'px',
      'border-color': bdr_clr
    });
    
  });
}
// In case users value their laptop battery life
// Allow them to turn the bubbles off
$('.bubble-toggle').click(function(){
  if($bubbles.is(':empty')) {
    bubbles();
    $bubbles.show();
    $(this).text('Bubbles Off');
  } else {
    $bubbles.fadeOut(function(){
      $(this).empty();
    });
    $(this).text('Bubbles On');
  } 
  
  return false;
});

function startBubbleGame(){
  var $bubbles = $('.bubbles'); 
  $bubbles.html(''); //clean all
  $bubbles.addClass('active')
  bubbles();
  setTimeout(function(){  $(".bubbles").removeClass('active'); }, 5000); // play for 30 sec.
}

/******************  Bubble Games End *****************/

/***************  Start Content tanble Div Editor *************
dc_editor: dc editor:
1. Double click to edit
2. Make carser where it should be..
Example:
<div id="dc_editor" contenteditable="false">Some editable text. Double click to edit</div>
***************************************************************/
function getMouseEventCaretRange(evt) {
    var range, x = evt.clientX, y = evt.clientY;
    
        // Try the simple IE way first
        if (document.body.createTextRange) {
            range = document.body.createTextRange();
            range.moveToPoint(x, y);
        }
    
    else if (typeof document.createRange != "undefined") {
        // Try Mozilla's rangeOffset and rangeParent properties, which are exactly what we want
        
        if (typeof evt.rangeParent != "undefined") {
            range = document.createRange();
            range.setStart(evt.rangeParent, evt.rangeOffset);
            range.collapse(true);
        }
    
        // Try the standards-based way next
        else if (document.caretPositionFromPoint) {
            var pos = document.caretPositionFromPoint(x, y);
            range = document.createRange();
            range.setStart(pos.offsetNode, pos.offset);
            range.collapse(true);
        }
    
        // Next, the WebKit way
        else if (document.caretRangeFromPoint) {
            range = document.caretRangeFromPoint(x, y);
        }
    }
    
    return range;
}

function selectRange(range) {
    if (range) {
        if (typeof range.select != "undefined") {
            range.select();
        } else if (typeof window.getSelection != "undefined") {
            var sel = window.getSelection();
            sel.removeAllRanges();
            sel.addRange(range);
        }
    }
}

//document.getElementById("dc_editor").ondblclick = function(evt) 
$('.dc_editor').on('dblclick' ,function (e){
    evt = evt || window.event;
    this.contentEditable = true;
    this.focus();
    var caretRange = getMouseEventCaretRange(evt);    
    // Set a timer to allow the selection to happen and the dust settle first
    window.setTimeout(function() {
        selectRange(caretRange);
    }, 10);
    return false;
});

/***************  End of Double click Editor *********************/

/********** Dynamic Allocate Elements **********************
Example:
RegisterEvent('click','div',function(){alert('hello');})
DeRegisterEvent('click','div')
RegisterEvent('dblclick','div',function(){alert('hello'); this.contentEditable = true;})
***********************************************************/
function RegisterEvent(ev,ele,clb){
  $(ele).on(ev, clb );
}
function DeRegisterEvent(ev,ele){
  $(ele).off(ev);
}
/***************** Dynamic Allocate Elements ************/

/**********  Serialize Editable data ************/
