/*
/*JEOPVIDEO : Video Player setup and related functions
 */
(function(n,$,undefined){
	"use strict"

	var trace = function() {},	// define trace if not loaded (set in init)
		visApi = null,	// set visApi to null if not loaded (set in init)
		vid_wrapper = '<div class="videoWrapper"/>',
		playerID = 'vidPlayer_',
		playerCount = 0,
		vidHosts = {
			'youtube'	: {
				check	: /^(?:https?:?)?(?:\/\/)?(?:www|m)?\.?(?:youtube\.com|youtu.be)\/(?:[\w\-]+\?v=|embed\/|v\/)?([\w\-]+)(\S+)?$/i,
				checkID : 1,	// the capture index for the video ID
				URL		: 'https://www.youtube.com/embed/',
				params	: {
					autoplay	: 'autoplay',
					controls	: 'controls',
					related		: 'rel',
					loop		: 'loop',
					api			: 'enablejsapi',
					referer		: 'origin'
				}
			},
			'vimeo' : {
				check	: /https?:\/\/(?:www\.|player\.)?vimeo.com\/(?:channels\/(?:\w+\/)?|groups\/([^\/]*)\/videos\/|album\/(\d+)\/video\/|video\/|)(\d+)(?:$|\/|\?)/i,
				checkID	: 3,	// the capture index for the video ID
				URL		: 'https://player.vimeo.com/video/',
				params	: {
					autoplay	: 'autoplay',
					loop		: 'loop',
					api			: 'api'
				}
			}
		},
		params = {
			autoplay 	: 0,
			loop		: 0,
			api			: 1,
			related		: 0,
			controls	: 1,
		},
		AutoPauseEvent	= 'pageVisible',
		ModalPlayerDiv = null,
		timerInterval = 1000; // time in milliseconds to update analytics during video playback


	function init(){
		// use the trace module if it exists, else use the old trace function, fail safe to a blank function
		trace = window.site.utilities && window.site.utilities.trace ? window.site.utilities.trace.push : (window.trace || function(){});
		visApi = n.utilities && n.utilities.visApi ? n.utilities.visApi : null;	// cache visApi reference if present

		detectModal();
		detectEmbededVideos();
		listeners();
	}

	/**
	 * Check if the player's installed and if not load it, the css and the empty div needed for it
	 * @return {[type]} [description]
	 */
	 function detectModal(){

		//check for modal video player div
		if($('#ext_video1').size() == 0){
			$('body').append('<div id="ext_video1"/>');
			trace('added the modal div');
		} else {
			trace('the modal div is already present');
		}

		ModalPlayerDiv = $('#ext_video1');
	}

	function detectEmbededVideos(){
		var iframes = $('iframe:not(.videoEmbed)'),
			videos = {};

		for(var len=iframes.length, i=0; i<len; i++) {
			var iframe = $(iframes[i]),
				videoEmbed = modifyVideoEmbed(iframe);

			if(videoEmbed) {
				iframe
					.attr('src',videoEmbed)
					.addClass('videoEmbed')
					.css({
						'position' : 'absolute',
						'left'	: 0,
						'top'	: 0,
						'width'	: '100%',
						'height': '100%'
					})
					.wrap(vid_wrapper);
			}
		}
	}

	/*
	 Attach all the event listeners
	 */
	function listeners(){
		
		$(document).on('click', 'a.video', function(e){
			if($(this).attr('href').indexOf('youtu') > -1) {
				e.preventDefault();
				e.stopPropagation();
				
				trace('loading the video' + $(this));

				var vidlink = ((typeof this.url) != 'undefined') ? this.url : $(this).attr('href');

				trace('the video link is '+ vidlink);

				var vimg = $(this).find('img').attr('src');
				var vidtitle = $(this).parent().find('h3:not(".galleryonly")').text();
				if(vidtitle.length < 2){
					vidtitle = $(this).parent().find('h3').text();
				}
				trace('The image grabbed is :' + vimg);

				var jeopv ={
					'url' : vidlink,
					'emsrc' : $(this).data('embedsrc'),
					'title' : vidtitle,
					'image' : vimg
				};
				trace(jeopv);

				prepModal(jeopv);
				setupVideo(jeopv);
			}
		});

		$(document).on('click', '#btn_close_modal',function(){
			ModalPlayerDiv.empty();
			$('body').css('overflow','auto');
		});
	}

	function modifyVideoEmbed(iframe){
		var url = iframe.attr('src'),
			embedUrl = url,
			vidHost = null;

		// loop through vidHosts to identify URL
		$.each(vidHosts, function(k,v){
			if(url.match(v.check)) {
				if(debug) {
					trace('check vidHost: '+k);
				}

				var vidCode = v.check.exec(url);
				iframe.data('videoId', vidCode);
				embedUrl = v.URL+vidCode[v.checkID];

				vidHost = k;
				return false;
			}
		});

		// if vidHost is supported, append parameters to embed URL
		if(vidHost) {
			if(debug) {
				trace(vidHost+' URL detected.');
			}
			if(!iframe.attr('id')) {

			}

			var i = 0;
			$.each(params, function(k,v){
				var delim = i === 0 ? '?' : '&';
				if(vidHosts[vidHost].params[k]) {
					if(debug) trace('adding '+k+ ' param');
					embedUrl += delim + vidHosts[vidHost].params[k] + '=' + encodeURIComponent(v);
				}
				i++;
			});

			vidHostApi(vidHost, iframe);

			return embedUrl;
		} else {
			return false;
		}
	}

	function vidHostApi(vidHost, player){
		switch (vidHost) {
			case 'youtube':

				// ensure Youtube iFrame API is loaded
				if(typeof window.YT === 'undefined') {
					trace('Adding YouTube API');
					//load the IFrame Player API code asynchronously
					var tag = document.createElement('script'),
						firstScriptTag = document.getElementsByTagName('script')[0];

					tag.src = "https://www.youtube.com/iframe_api";
					firstScriptTag.parentNode.insertBefore(tag, firstScriptTag);

					window.onYouTubeIframeAPIReady = function() {
						trace('YouTube API loaded');
						YTListen(player);
					};
				}
				else {
					if(debug) {
						trace('YouTube API already loaded');
					}
					try {
						YTListen(player);
					} catch(e){
						trace('YouTube API not ready');
						window.onYouTubeIframeAPIReady = function() {
							trace('YouTube API loaded');
							YTListen(player);
						};
					}
				}
				break;

			default: 

				break;
		}
	}

	function YTListen(player) {
		trace(player);
		var YTID = player.attr('id'),
			info = {
				'title' : '',
				'url' : player.attr('src'),
				'emsrc' : 'youtube',
				'current_time' : 0,
				'duration' : 0,
				'percentage' : 0,
				'quarter' : false,
				'half' : false,
				'third' : false
			},
			timer = null;

		if(!YTID){
			playerCount++;
			YTID = playerID + playerCount;
			player.attr('id', YTID);
		}

		
		var tubePlayer = new YT.Player(YTID, {
			events	: {
				'onStateChange': onPlayerStateChange
			}
		});

		if(visApi !== null){
			$(window).on(AutoPauseEvent+'.vidModal', function(e){
				if(e.detail.isVisible){
					trace('play video');
					tubePlayer.playVideo();
				}
				else {
					trace('pause video');
					tubePlayer.pauseVideo();
				}
			});
			
		} else {
			if(console && console.warn) console.warn('-- WARNING the visApi module is not recognized. Videos will NOT auto pause --');
		}

		function onPlayerStateChange(event) {
			var state = event.data;
			updateInfo();

			switch (state) {
				case YT.PlayerState.PLAYING:
					gtmStart(info);

					// set interval to check percentage of playback viewed
					timer = setInterval(updateInfo,timerInterval); 

					break;

				case YT.PlayerState.PAUSED:
					gtmStop(info);
					clearInterval(timer);
					break;

				case YT.PlayerState.ENDED:
					gtmComplete(info);
					clearInterval(timer);
					break;

				case YT.PlayerState.BUFFERING:

					break;

				case YT.PlayerState.CUED:

					break;

				default:

					break;
			}
		}

		function updateInfo(){
			info.title = tubePlayer.getVideoData().title;
			info.current_time  = tubePlayer.getCurrentTime();
			info.duration = tubePlayer.getDuration();
			info.percentage = info.current_time / info.duration;

			// fire at a quarter
			if (!info.quarter && info.percentage > .25) {
				info.quarter = true;
				gtmCheck(info, "25%");
			}
			// fire at half
			if (!info.half && info.percentage > .50) {
				info.half = true;
				gtmCheck(info, "50%");
			}
			// fire at 3/4
			if (!info.third && info.percentage > .75) {
				info.third = true;
				gtmCheck(info, "75%");
			}
		}
	}

	/*
	   Setup the modal html which includes fb and twitter sharing
	 */
	function prepModal(jeopv){
		var msg = 'Check out this Jeopardy! video |  '+jeopv.title,  //The space forces the title to the next line
		share_url = (jeopv.url != '#' || jeopv.url != null) ? jeopv.url : 'http://www.jeopardy.com';
		// var share_url = 'http://www.jeopardy.com';

		var layout = $('<div id="modal_overlay"> <div class="vid_wrapper"> <button id="btn_close_modal"></button> <div id="jplayer1"><div id="myElement">Loading the player...</div></div>  <div class="vid_info"> <div class="share"><a target="_new" href="https://www.facebook.com/sharer/sharer.php?s=100&p[url]='+share_url+'" class="share_facebook"></a><a href="https://twitter.com/intent/tweet?url='+share_url+'&text='+escape(msg)+'" target="_new" class="share_twitter"></a></div> <p id="vidtitle">Title goes here</p> </div>  </div>  </div>');
		ModalPlayerDiv.html(layout);
		$("body").css('overflow','hidden');
		layout.find("#vidtitle").text(jeopv.title);
		
		trace('Video URL is:  ' + jeopv.url );

	}

	/*
	   Check for embed or video url (link) and choose to use JWplayer or an iframe
	 */
	function setupVideo(info){

		var thesource = info.url,
			modal_width = $('.vid_wrapper').width(),
			iframe_width = modal_width * .9,


			iframe = $('<iframe/>', {
				"width" : iframe_width,
				"height" : 360,
				"scrolling" : 'no',
				"frameborder" : 0,
				"src" : thesource,
				"allowfullscreen" : true,
				"mozallowfullscreen" : true,
				"webkitallowfullscreen" : true,
				"allowtransparency" : true
			});

		//thelayout = '<iframe autoplay="false" source='+thesource+' width=70% height="auto" ></iframe>';
		//get the embed source.
		$("#myElement").hide();
		//insert it into an iFrame and add it to the dom
		$('#jplayer1').append(iframe);
		
		detectEmbededVideos();
	}

	function gtmStart(info){
		if(dataLayer){

			var verbage = (Math.round(info.current_time) == 0 || info.current_time =='undefined') ? "video_start" : "video_continue";

			dataLayer.push({
				"video_action" : verbage,
				"video_title" : info.title,
				"event" : "video",
				"video_url" : info.url,
				"watch_time" : info.current_time
			});
		}

		trace("The video Tracking fired"+ info);
	}


	function gtmComplete(info){

		if(dataLayer){
			dataLayer.push({
				"video_action" : "video_complete",
				"video_title" : info.title,
				"event" : "video",
				"video_url" : info.url,
				"watch_time" : info.current_time
			});
		}

		trace("The video Complete "+ info);
	}

	function gtmStop(info){
		if(dataLayer){

			if( (info.current_time  + 1) <  info.duration){ // don't send after video complete

				dataLayer.push({
					"video_action" : "video_stop",
					"video_title" : info.title,
					"event" : "video",
					"video_url" : info.url,
					"watch_time" : info.current_time
				});

			}

		}
		trace("The video stopped"+ info);
	}


	function gtmCheck(info, perc_check){

		if(dataLayer){
			dataLayer.push({
				"video_action" : "video_check",
				"video_title" : info.title,
				"event" : "video",
				"video_url" : info.url,
				"watch_percent_reached" : "watched "+perc_check+ " of the video"
			});
		}

		trace("The video Complete "+ info);
	}

	// Public API
	n.detectEmbededVideos = detectEmbededVideos;
	n.modifyVideoEmbed = modifyVideoEmbed;
	
	// run on DOM ready
	$(function(){
		init();
	});

})(window.JEOPVIDEO=window.JEOPVIDEO || {},jQuery);