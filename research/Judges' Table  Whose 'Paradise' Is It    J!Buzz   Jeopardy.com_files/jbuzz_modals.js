var jbuzzModals = {

	selector : $('.jbuzz_modules .jbuzz_module a'),
	jbuzz_types : ['picture','gif','video'],

	modal_layout : $('<div id="modal_overlay"><div class="jbuzz_wrapper"><button id="btn_close_modal"></button><div class="jbuzz_info"></div><div class="jbuzz_content"></div><a href="#" class="readmore">Read Full Article</a></div></div>'),
	modal_category : $('<div class="jbuzz_article_category"></div>'),
	modal_share : $('<ul id="jbuzz_modal_social"><li id="jbuzz_modal_fb"><a id="news_modal_fb_link" class="news-jbuzz-detail-share-facebook sprite share_facebook" href="#">Facebook</a></li><li id="jbuzz_modal_tw"><a id="news_modal_tw_link" class="news-jbuzz-detail-share-twitter sprite share_twitter" href="#">Twitter</a></li><li id="jbuzz_modal_em"><a id="news_modal_em_link" class="news-jbuzz-detail-share-email sprite share_email" href="#">Email</a></li></ul>'),

	module : null,
	article_data : {},

	init : function() {
		var self = this;

		if($('#jbuzz_modal').size() == 0) {
			$('body').append('<div id="jbuzz_modal"/>');
			trace('added the JBuzzModal div');
		}

		$(document).on('click', '.jbuzz_modules .jbuzz_module a', function(e) {

			self.module = $(this);
			var elem = $(this);
			var isMobile = $(window).width() < 780;
			var isType = false;
			$.each(self.jbuzz_types, function(i,v) {
				if(elem.hasClass(v)) {
					isType = true;
					self.article_data.type = v;
				}
			});

			trace('JBuzzModal isType: '+isType);
			if(isType && !isMobile) {
				e.preventDefault();
				e.stopPropagation();
				self.article_data.url = elem.attr('href');
				self.getArticleData(self.article_data.url);
			}
		});

		$(document).on('click', '#jbuzz_modal #btn_close_modal',function(){
            $("#jbuzz_modal").empty();
			$("body").css('overflow','auto');
			self.module = null;
        });
	},

	getArticleData : function(url) {
		var self = this;

		if(typeof url != 'undefined' && url != 'undefined') {

			$.ajax({
				url:url,
				type:'GET',
				success: function(data) {
					var article_data = $(data);
					self.parseData(article_data);
				},
				error: function(data) {
					trace(data);
					self.failOver();
				}
			});

		}
		else {
			self.failOver();
		}
	},

	parseData : function(data) {
		var self = this;
		trace(data);

		self.article_data.category = data.find('#jbuzz_article_category').html();
		self.article_data.title = data.find('#jbuzz_article_txt h1').text();
		self.article_data.content = data.find('#jbuzz_article_txt').html();
		self.article_data.tags = $('<ul class="jbuzz_article_tags">').html(data.find('#jbuzz_article_tags').html());
		self.article_data.meta = data.find('meta[property="og:title"]').attr('content');

		self.buildModal();
	},

	buildModal : function() {
		var self = this;
		
		var data = self.article_data;

		var layout = self.modal_layout.clone();
		var category = self.modal_category.clone();
		var share = self.modal_share.clone();
		var info = layout.find('.jbuzz_info');
		var content = layout.find('.jbuzz_content');
		
		if(data != null) {
			layout.find('a.readmore').attr('href',self.article_data.url);

			category.html(data.category);
			content.html(data.content);
			content.append(data.tags);

			info.append(category);
			info.append(share);

			$('#jbuzz_modal').empty().append(layout);

			$('body').css('overflow','hidden');

			if(data.type == 'picture' || data.type == 'gif' || data.type == 'infographic') {
				ModalGallerySlides.init();
			}
			if(data.type == 'video') {
				self.videoAdjust();
			}
			self.shareButtons();
		}
	},

	videoAdjust : function() {
		var self = this;
		var articleWrap = $('#jbuzz_modal');
		var articleBody = $('#jbuzz_modal .jbuzz_content');
		
		articleBody.find('iframe:first').parent('p').prependTo(articleBody);
		JEOPVIDEO.detectEmbededVideos();

		self.cleanModal();
	},

	shareButtons : function() {
		var self = this;
		$("#jbuzz_modal_social a").click(function(e){
			e.preventDefault();
			e.stopPropagation();

			var url = '',
				link = window.location.protocol+'//'+window.location.hostname+self.article_data.url,
				facebookBase="https://www.facebook.com/sharer/sharer.php?u=",
				twitterBase="https://twitter.com/intent/tweet?text=";


				// pull custom share info from meta tag ... how to code at midnight....

				var social_element = self.article_data.meta;
				var custom_text = social_element || self.article_data.title;


			if ($(this).hasClass("share_facebook")){
				url = facebookBase + encodeURIComponent(link);
			} else if ($(this).hasClass("share_twitter")){
				url = twitterBase + encodeURIComponent(custom_text) + " " + encodeURIComponent(link);
			} else if ($(this).hasClass("share_google")){
				url = "https://plus.google.com/share?url=" + encodeURIComponent(link);
			} else if ($(this).hasClass("share_pagelink")){
				//url = "";
				return;
			} else if ($(this).hasClass("share_email")){
				url= "mailto:?&subject="+encodeURIComponent(self.article_data.title)+"&body=" + encodeURIComponent(link);
			}

			window.open(url, "share");
		});
	},

	cleanModal : function() {
		var self = this;
		$("#jbuzz_modal .rxbodyfield > *").not('.rxbodyfield > p:first').remove();
	},

	failOver : function() {
		trace('JBuzzModal FailOver');
		var self = this;
		var url = self.module.attr('href');
		$("#jbuzz_modal").empty();
		$("body").css('overflow','auto');
		if(typeof url != 'undefined' && url != 'undefined') {
			self.module = null;
			window.location = url;
		}
	},

}

$(function(){
	jbuzzModals.init();
});

$.fn.ignore = function(sel){
  return this.clone().find(sel||">*").remove().end();
};

var ModalGallerySlides = ModalGallerySlides || { // Gallery Scroller
	articleWrap : $('#jbuzz_modal'),
	articleBody : $('#jbuzz_modal .jbuzz_content'),
	addPips : true,
	addViewlist : false,
	viewText : ['view as list', 'view as slideshow'],
	slides : null,
	container : null,
	current : 0,
	total : 0,
	animTime : 500, // time in milliseconds for gallery slide animation

	init : function() {
		var self = this;
		trace('init JBuzz gallery');
		self.articleWrap = $('#jbuzz_modal');
		self.articleBody = $('#jbuzz_modal .jbuzz_content');

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

		$('#jbuzz_modal .jbuzz_content .gallerywrap').prependTo(self.articleBody);
		jbuzzModals.cleanModal();
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