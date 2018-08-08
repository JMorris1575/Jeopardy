// check for YT videos embedded in the article copy and load the iframe YT script

if (typeof trace !== 'function'){
	trace = function(){}
}

var NV =  NV || {}; //news videos

NV = {

	checkForEmbeds : function(){
		var embVideos = $('iframe');
		if(embVideos.length > 0){
			//trace('we have '+embVideos.length+' youtube videos.');

			$(embVideos).each(function(i){

				//check for main img or article embed
				v_parent = $(this).parent().parent().attr('id');
				window.v_parent = v_parent;
				//get url
				var source = $(this).attr('src');
				var url = NV.getYTID(source);
				var v_id = 'vid_'+i;

				//add new iframe to page.  Clean this up later
				if(url != null) {
					if(v_parent == 'news_article_img' ){
						//trace('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ there\'s a main article');
						$(this).parent().append('<div id="'+v_id+'"/>').addClass('video-tracking');

					}else{
						//trace('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ it\'s in the body');
						$(this).empty().after('<div id="'+v_id+'"/>').addClass('video-tracking');
					}

					$(this).remove();

					NV.renderJWPlayer(v_id, url);
				}
			})

		}else {
			//trace("no youtube videos")
		}

	},

	getYTID : function(url){
		 var regExp = /^.*(youtu.be\/|v\/|u\/\w\/|embed\/|watch\?v=)([^#\&\?]*).*/;
	    var match = url.match(regExp);
	    if (match&&match[2].length==11){
	        return match[2];
	    }else{
	        //trace("There isn't a YT video here");
	        return null;
	    }
	},


	renderJWPlayer : function(id, url){

		var v_size = {"width": 560, "height" : 315};
		if(window.v_parent == 'news_article_img' ){
			v_size.height = 360;
			v_size.width = 640;
		}

		var v_title = $("#news_article_header h3").text() + '-'+id+'(embedded)';

		var playerInstance = 'playerInstance_'+id;
		playerInstance = jwplayer(id);
		v_file = 'https://www.youtube.com/watch?v='+url;
		var info;
		info = {
			"title" : v_title,
			"url" : v_file,
			"current_time" : 0
		};

		var jvideo = playerInstance.setup({
		    file: v_file,
			width: v_size.width,
			height:v_size.height,
		    events: {
		    	onPlay: function(){GT.gtmStart(info)},
		    	onTime: function(event) {


					        info.percentage = jvideo.getPosition() / jvideo.getDuration();
					        info.current_time = (this.getPosition() != 'undefined') ? this.getPosition() : 0;


					        // fire at a quarter

					        if (!info.quarter && info.percentage > .25) {
					            info.quarter = true;
					            GT.gtmCheck(info, "25%");

					        }
					        // fire at half
					        if (!info.half && info.percentage > .50) {
					            info.half = true;

					            GT.gtmCheck(info, "50%");

					        }
					        // fire at 3/4
					        if (!info.third && info.percentage > .75) {
					            info.third = true;

					            GT.gtmCheck(info, "75%");

					        }

					    } ,
		    	onPause: function(){GT.gtmStop(info)},
		    	onComplete : function(){GT.gtmComplete(info);
			            		//trace("complete fired");
			            		}
		    }
		});
	},

	checkJWPlayer: function(cb){
		    var jwscript = '/Assets/jeopardy/js/vendor/jwplayer/jwplayer.js',
            jwkey =  "KRfs9Za5NjfmH2KZ2OBi4e07U2trg+B5vlMisg==",
            jwcss = '/Assets/jeopardy/css/video.css';


        if( typeof(jwplayer) !=  'function'){
            trace('jw not loaded');
            $.getScript(jwscript, function(){
                    trace('loaded player');
                    jwplayer['key'] = jwkey;
             });
            $.getScript(jwcss, function(){

            });
            $.getScript('/Assets/jeopardy/js/vendor/jwplayer/jwplayer.html5.js', function(){
            	NV.checkForEmbeds();
            });

        }else{
            //trace('jw loaded');
        }

	}


}


var GallerySlides = GallerySlides || { // Gallery Scroller
	articleWrap : $('#jbuzz_article'),
	articleBody : $('#jbuzz_article #jbuzz_article_txt'),
	addPips : true,
	addViewlist : true,
	viewText : ['view as list', 'view as slideshow'],
	slides : null,
	container : null,
	current : 0,
	total : 0,
	animTime : 500, // time in milliseconds for gallery slide animation

	init : function() {
		var self = this;
		self.articleBody.find('img').parent('p').addClass('img');

		self.articleBody.find('p.img').each(function(i,v){
			$(this).nextUntil('p.img, h2, div','p').wrapAll('<div class="caption"/>');
			$(this).prev('h2').andSelf().add($(this).next('.caption')).wrapAll('<div class="slide" id="slide_'+i+'"/>');
		});
		
		self.slides = self.articleBody.find('.slide');
		self.total = self.slides.length;
		self.slides.wrapAll('<div class="gallerywrap slideshow"><div class="slides"/></div>');
		self.container = self.articleBody.find('.slides');

		if(self.total > 1) {
			self.container.append('<div class="slidecontrol left"/><div class="slidecontrol right"/>');
			if(self.addViewlist) {
				$('<p class="view_toggle"><a class="slideshow" href="#">'+self.viewText[0]+'</a></p>').insertBefore(self.container);
			}
			$('<div class="slidecount"/>').insertAfter(self.container);
			if(self.addPips) {
				var pips = $('<ul class="pips"/>');
				pips.insertAfter(self.container);
				for(i=0; i<self.total; i++) {
					pips.append('<li id="pip_'+i+'"/>');
				}
			}
			self.slides.not(':first').css({'left':'100%'});
			self.listeners();
			self.gotoSlide(0);
		} else {
			self.container.parent('.gallerywrap').toggleClass('slideshow list');
		}
	},

	listeners : function(){
		var self = this;

		self.container.find('.slidecontrol').click(function(e){
			e.preventDefault();
			e.stopPropagation();
			if($(this).hasClass('left')) {
				self.gotoSlide('prev');
			} else {
				self.gotoSlide('next');
			}
		});

		if(self.addViewlist) {
			self.articleBody.find('.view_toggle a').click(function(e){
				e.preventDefault();
				e.stopPropagation();

				self.container.parent('.gallerywrap').toggleClass('slideshow list');

				var link = $(this);
				if(link.hasClass('slideshow')){
					link.text(self.viewText[1]).removeClass('slideshow').addClass('list');
				} else {
					link.text(self.viewText[0]).removeClass('list').addClass('slideshow');
				}
			});
		}

		if(self.addPips) {
			self.articleBody.find('.pips li').click(function(e){
				e.preventDefault();
				e.stopPropagation();

				var id = $(this).attr('id').replace('pip_', '');
				self.gotoSlide(id);
			})
		}
	},

	gotoSlide : function(id) {
		var self = this;
		if(id == 'prev') id = self.current -1;
		if(id == 'next') id = self.current +1;

		id = parseInt(id);

		var direction = id > self.current ? 0 : 1;

		if(id > self.total-1) id = 0;
		if(id < 0) id = self.total-1;

		if(self.addPips) {
			self.articleBody.find('.pips li').removeClass('active').filter('#pip_'+id).addClass('active');
		}

		var current = self.container.find('#slide_'+self.current);
		var next = self.container.find('#slide_'+id);

		if(id != self.current) {

			if(direction == 0) { // slide left
				next.css({'left':'100%'}).animate({'left':0}, self.animTime);
				current.animate({'left':'-100%'}, self.animTime, function(){
					current.removeClass('active');
					next.addClass('active');
				});
			} else {	// slide right
				next.css({'left':'-100%'}).animate({'left':0}, self.animTime);
				current.animate({'left':'100%'}, self.animTime, function(){
					current.removeClass('active');
					next.addClass('active');
				});
			}

			self.current = id;
		} else {
			current.addClass('active');
		}

		self.container.siblings('.slidecount').html('<span>'+(self.current+1)+'</span>/'+self.total);
	},

	isGallery : function() {
		return this.articleWrap.hasClass('picture') || this.articleWrap.hasClass('gif') || this.articleWrap.hasClass('infographic');
	},

}


$(document).ready(function(){
	//VIDEO_DISABLE NV.checkJWPlayer();
	GallerySlides.articleWrap = $('#jbuzz_article');
	GallerySlides.articleBody = $('#jbuzz_article #jbuzz_article_txt');
	if(GallerySlides.isGallery()) {
		GallerySlides.init();
	}

	var checkdate = $('.date');

	checkdate.each(function(){
		var raw = $(this).text().trim();

		var newdate = getDateFormat(raw);

		if( typeof newdate != 'undefined'){
			$(this).text(newdate);
		}
 	})



	// Quick fix to update main & related article icons on stage 10
	var	newsIcons = ["", "alex", "contestants", "pop", "show", "crew", "press", "ask"],
		newsIconsMatrix = {"alextrebek" : "alex", "contestants" :"contestants", "popculure" : "pop", "theshow" : "show", "cluecrew" : "crew", "press" : "press", "weask" : "ask"};


	mainArticleCat = $('#news_article_header').find('h2').text();
	category = mainArticleCat.replace(/ /g,'').toLowerCase();
	$("#news_article_img").addClass(newsIconsMatrix[category]);


	var relatedArticles = $("aside article h4");
	relatedArticles.each(function(){
		item_cat = $(this).text();
		item_class = item_cat.replace(/ /g,'').toLowerCase();
		$(this).siblings('div.storyicon').addClass('news_icon '+ newsIconsMatrix[item_class]);
	});

	//Jbuzz landing latest stories
	var stories = $('.story');

	stories.each(function(){
		rawcat = $(this).find('h3').text();
		newcat = rawcat.replace(/ /g,'').toLowerCase();
		$(this).addClass(newsIconsMatrix[newcat]);
	});

	var container = $("#news_article_right .container"),
		images = $(".story_img_wrap img");

	function sizeImageCrop(){
		var fullWidth = 225,
			fullHeight = 259,
			fullContainerWidth = 246;

		var perc = $(container).width() / fullContainerWidth;

		if (perc > 1) {
			perc = 1;
		}

		if ($("body").width() > 767){
			$(images).css({
				'clip':'rect(0px, '+(fullWidth * perc)+'px, '+(fullHeight * perc)+'px, 0px)'
			});
		} else {
			$(images).css({
				'clip':'auto'
			});
		}
	}

	sizeImageCrop();

	$(window).resize(sizeImageCrop);




});