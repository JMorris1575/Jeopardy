// JCG document ready at end of file.
/* OBJECT AND PROTOTYPE DEFENITIONS */

document.writeln("<script type='text/javascript' src='/Assets/jeopardy/easyxdm/easyXDM.js'></script>");
document.writeln("<script type='text/javascript' src='/Assets/jeopardy/easyxdm/exdm_helper.js'></script>");

// Global addition of dialog module
document.writeln("<script type='text/javascript' src='/Assets/jeopardy/js/dialog.js'></script>");

document.writeln("<script type='text/javascript' src='/Assets/jeopardy/js/validate.min.js'></script>");
document.writeln("<script type='text/javascript' src='/Assets/jeopardy/js/2.0/jeopvideo.js'></script>");

var link = document.createElement( "link" );
link.href = "/Assets/jeopardy/css/dialog.css";
link.type = "text/css";
link.rel = "stylesheet";
link.media = "all";
document.getElementsByTagName( "head" )[0].appendChild( link );

$(function(){
	var year = new Date().getFullYear();
	$('#footer .copyYear').text(year);

   	if (self.location !== top.location && top.location.hostname != "wcms.sonypictures.com") {
   		$('body').empty();
   		$('body').html('Cross frame scripting detected and disallowed.');
   	}
})

//Resize management, update root element size for rem size
var resizeManager = {

	tabThreshold : 1280,
	mobileThreshold : 767,
	tabWidth : 1280,
	mobileWidth : 640,
	initRootSize : 10,
	domRoot : null,
	menuBaseFontSize : 12,
	navItems:null,
	navContainer:null,

	init : function()
	{
		resizeManager.domRoot = $('html');
		resizeManager.navItems = $(".nav_item");
		resizeManager.navContainer = $("#nav .container");
	},

	handelResize : function()
	{

		var newWidth = window.innerWidth;
		var multiplier = 1;
		var newRootSize = 10;

		trace("WORKING ON RESIZE " + resizeManager.targetWidth);

		if (newWidth <= resizeManager.mobileThreshold)
		{
			trace("GO MOBILE");
			multiplier = newWidth / resizeManager.mobileWidth;
		}
		else if (newWidth < resizeManager.tabThreshold  )
		{
			trace("GO TAB");
			multiplier = newWidth / resizeManager.tabWidth;
		}

		newRootSize = resizeManager.initRootSize * multiplier;
		newRootSize = newRootSize + "px";

		$(resizeManager.domRoot).css('font-size', newRootSize);
		$(resizeManager.navItems).css('font-size', resizeManager.menuBaseFontSize * (resizeManager.navContainer.width() / 990));

	},

	handleSubResize : function(element, fullWidth, baseFontSize){
		var perc = $(element).width() / fullWidth;

		if ($(element).width() == 0){
			perc = 1;
		}

		var newRootSize = baseFontSize * perc;

		$(element).css('font-size', newRootSize + "px");
	}

};


////////////////////////////////////////////////////////////////////////////////////////////
//
//  User session management - signed in status
//	on each page load, creates the global userStatus object that can be accessed
//	on each page load userStatus object checks for cookie and handles time till expiration
//
//	a global var userStatus is created and can be check at any point.
//	currently init is not in the document ready function to speed responce, but this can be updated if problems arrise
//
//	Note:  the sign-in page /signin now has tabbed flowthrough for username and password.
//	Also, there is a js script in the signin widget that binds the enter key to clicking the signin button
//
//	Usefull function/methods
//	isUserLoggedIn() - returns boolean
//	setAsSignedIn(id, username, toek) - after sign in to set values
//	getUserID - returns ID or false if not signed in
//	getUserName - returns user name or false if not signed in
//
//	**** isUserLoggedInPII should be ignored, it is just a stub in case thing change
//
////////////////////////////////////////////////////////////////////////////////////////////
function UserStatus()
{
	this.signedIn = null;
	this.userID = null;
	this.userName = null;
	this.serverToken = null;
	this.cookieName = 'jeopuserstatus';
	this.cookieDataDelin = '|';
	this.cookieExpiration = 0.083;  //2 hours
	this.loginType = null;
}


UserStatus.prototype.init = function()
{
	this.checkCookieData();
};

UserStatus.prototype.isUserLoggedIn = function()
{
	var self = this;
	if (self.signedIn == null) {
		return self.checkCookieData(function(d) {
			return self.signedIn ? self.loginType : false;
		});
	}
	else {
		return self.signedIn ? self.loginType : false;
	}


};

/*
Return the user id
retuns false is not set
*/
UserStatus.prototype.getUserID = function()
{
	var self = this;
	if (self.signedIn == null) {
		return self.checkCookieData(function(d) {
			return self.userID;
		});
	}
	else {
		return self.userID;
	}
};

/*
Return the user name
retuns false is not set
*/
UserStatus.prototype.getUserName = function()
{
	var self = this;
	if (self.signedIn == null) {
		return self.checkCookieData(function(d) {
			return self.userName;
		});
	}
	else {
		return self.userName;
	}
};


/*
Return the session token
retuns false is not set
*/
UserStatus.prototype.getUserToken = function()
{
	var self = this;
	if (self.signedIn == null) {
		self.checkCookieData(function(d) {
			return self.serverToken != null ? self.serverToken : false;
		});
	}
	else {
		return self.serverToken;
	}
};

/*
Check for locally stored cookie and updates data if found
*/
UserStatus.prototype.checkCookieData = function(cb)
{

	//check if a cookie is present
	var cookie = this.readCookie(this.cookieName);
	var dataTemp;

	if(cookie != null)
	{
		trace("login cookie found " + cookie);
		var splitData = cookie.split(this.cookieDataDelin);
		this.userID = splitData[0];
		this.userName = splitData[1].toString().replace(/<[^>]*>/g, "");
		this.serverToken = splitData[2];
		this.loginType = splitData[3];

		if(splitData.length < 4){ //not a valid cookie
			this.signedIn = false;
		}

		trace("Here's the cookie info");
		trace(splitData);
		if (this.userID != null && this.userID != false && this.userID !== '')
		{
			this.signedIn = true;
		}
		else
		{
			trace('The value is empty');
			this.signedIn = false;
		}

	}else{

		trace('There is not a cookie present');
		this.signedIn = false;
	}

	if(this.signedIn == false) {
		backendUserCheck(function(d){
			if(cb) {
				cb(d);
			}
		});
	} else {
		if(cb) {
			cb(this.signedIn);
		}
	}


};

/*
Sets a cookie with log in info
*/
UserStatus.prototype.setCookieData = function(userID, userName, token, loginType)
{
	var cookieData = "";
	cookieData += userID + this.cookieDataDelin;
	cookieData += userName + this.cookieDataDelin;
	cookieData += token + this.cookieDataDelin;
	cookieData += loginType;

	this.createCookie(this.cookieName, cookieData, this.cookieExpiration);
};

/*
Use signed in set the data we need
Mostly just calling update status
*/
UserStatus.prototype.userSignedIn = function(userID, userName, token, loginType)
{
	trace('userSignIn');
	trace('userID->'+userID);
	trace('userName->'+userName);
	trace('token->'+token);
	trace('loginType->'+loginType);
	
	//get id and username
	//drop cookie with fresh timeing
	token = typeof token !== 'undefined' ? token : 0;
	loginType = typeof loginType !== 'undefined' && typeof loginType !== 'boolean' ? loginType : 'hard';
	
	this.userID = userID;
	this.userName = userName;
	this.serverToken = token;
	this.loginType = loginType;

	this.setCookieData(userID, userName, token, loginType);
	updateHeaderForLogInStatus(true);
};

UserStatus.prototype.userSignedOut = function()
{
	trace('userSignOut');
	this.userID = null;
	this.userName = null;
	this.serverToken = null;
	this.loginType = null;
	this.signedIn = false;
	this.eraseCookie(this.cookieName);

	updateHeaderForLogInStatus(false);

};


UserStatus.prototype.createCookie = function(name,value,days)
{

	if(typeof days != 'undefined' && days != -1){
		var date = new Date(),
			time = date.getTime(),
			addTime = days*24*60*60*1000,
			dateCode = time+addTime;
		date.setTime(dateCode);
		var expires = "; expires="+date.toUTCString();
	 }else{
	 	// var expires = "; expires=Thu, 01 Jan 1970 00:00:01 GMT";
	 	//forcing the cookie to delete
	 	document.cookie = name+'=;expires=Thu, 01 Jan 1970 00:00:01 GMT;path=/';
	 	trace("deleted the cookie");

	 	return
	 }

	 trace('expires->'+expires);

	document.cookie = name+"="+value+expires+";path=/";
};

UserStatus.prototype.readCookie = function(name)
{
    var nameEQ = name + "=";
    var ca = document.cookie.split(';');
    for(var i=0;i < ca.length;i++) {
        var c = ca[i];
        while (c.charAt(0)==' ') c = c.substring(1,c.length);
        if (c.indexOf(nameEQ) == 0) return c.substring(nameEQ.length,c.length);
    }
    return null;
};

UserStatus.prototype.eraseCookie = function(name)
{
	this.createCookie(name,"","-1");
	trace('eraseCookie');

};



/*
VARIABLES
*/
var isAndroid = (/android/gi).test(navigator.appVersion) || window.location.hash == "#isAndroid",
	isIDevice = (/iphone|ipad/gi).test(navigator.appVersion) || window.location.hash == "#isIDevice",
	isTouchPad = (/hp-tablet/gi).test(navigator.appVersion) || window.location.hash == "#isTouchPad",
	isMobile = (/android|iphone|ipad|hp-tablet/gi).test(navigator.appVersion) || window.location.hash == "#isMobile";


$.urlParam = function(name){
    var results = new RegExp('[\?&]' + name + '=([^&#]*)').exec(window.location.href);
    if (results==null){
       return null;
    }
    else{
       return results[1] || 0;
    }
};


if (!Array.isArray) {
  Array.isArray = function(arg) {
    return Object.prototype.toString.call(arg) === '[object Array]';
  };
}

var userStatus = new UserStatus();

$(function(){
	userStatus.init();  // move to document ready if prefered
});

var debug = true;

function trace(str){
	if (typeof console == "undefined") {
   		 this.console = {log: function() {}, dir: function(){}};
	}else if (window.console && debug && location.hostname != "www.jeopardy.com"){
		console.log(str);
	}
}

function getDateFormat(dateStr){
	var month = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'];

	//trace('getDateFormat');
	//trace('the input date is:'+ dateStr);

	dateStr = trimWhiteSpace(dateStr);

	//trace('the cleaned input date is : '+dateStr);


	if (dateStr.indexOf(" ") > -1){
		dateStr = dateStr.split(" ")[0];
	}

	var dateNum = dateStr.split('-');

	//console.dir("the date array is: "+dateNum);


	//trace('dateStr->'+dateStr);

	var date = new Date(dateNum[0],(dateNum[1] -1),dateNum[2],07, 00, 01, 00);
	/* I added the 7 hour (1 sec)  deal because of the GMT offset */

	var yesterday = new Date();
	yesterday.setDate(yesterday.getDate() - 1);
	//trace('yesterday date ->'+yesterday);

    yesterday = (yesterday.getMonth() + 1) + "-" + yesterday.getDate() + "-" + yesterday.getFullYear();
    //trace('yesterday col:->'+yesterday);

    //trace('transformed input date : '+date);

    var dateCheckStr = (date.getUTCMonth()+1) + "-" + date.getDate() + "-" + date.getFullYear();

    //trace('dateCheckStr->'+dateCheckStr);
   // trace('month[date.getMonth()] + " " + date.getUTCDate() + ", " + date.getFullYear()->'+(month[date.getMonth()] + " " + date.getUTCDate() + ", " + date.getFullYear()));

    if (yesterday == dateCheckStr){
    	return "Yesterday";
    } else {
		return month[date.getMonth()] + " " + date.getUTCDate() + ", " + date.getFullYear();
	}
}

/**
 * js version to strip tags(text inside of brackets) taken from Percussion and put them in an array
 * @param  {[type]} data [the object containing the tags pulled from precussion]
 * @return {[type]}      an array of the tags
 */
function pullTags(data){
	results = [];
	data.replace(/\[(.+?)\]/g, function($0, $1) { results.push($1); });
	trace('the data is: ' + words);
	trace(results.length);
	return results;
}

function getRelatedNewsArticles(){
	var s_url = '/php/getnewsresults.php?tag=',
	 	tag = 'ALEX TREBEK',
	 	results,
	 	u='';

 	u += String(s_url);
 	u += String(tag);

	raSearch = $.ajax({
					url: u
				}).done(function(data){
					trace(data);
					relatedarticles = $(data).find("#results").text();
				});
}


/**
* Error message handeling
* parse back end api responces and pull error text to display OR
* Trigger specific text responces based on error code
*/
var errorDecoder = {

	//catch error codes and return text based on error code value
	//is specific text is not specified, format the server responce
	interpretError:function(dataObject)
	{
		errorString = '';

		//if already a string just return it
		if (typeof dataObject === 'string')
		{
			errorString = dataObject;
			return errorString;
		}


		//if an array - decode into a string and return
		if (typeof dataObject === 'array')
		{
			for (var i = 0; i < dataObject.length; i++)
			{
				errorString += dataObject[i];
				errorString += '<br>';
			}
			return errorString;
		}


		//if an object EXPECTED CASE
		var errorCode = dataObject['errors']['code'];
		trace("error code is " + errorCode);

		switch(errorCode)
		{
			case 12:
				errorString = 'Sorry, the username and password combination entered does not match our records.';
				break;

			case 22:
				//invalid username or password
				if (dataObject['errors']['message']['password'] !== undefined){
					if(dataObject['errors']['message']['password'].indexOf('required') > -1) {
						errorString += "Please enter your password.\n";
					} else {
						errorString += 'Your password must contain at least one number and one letter.\n';
					}
				}
				if (dataObject['errors']['message']['username'] !== undefined){
					if(dataObject['errors']['message']['username'].indexOf('required') > -1){
						errorString += "Please enter your username or email.\n";
					} else {
						errorString += 'Your username must be at least 4 alphanumeric characters.\n';
					}
				}
				if (dataObject['errors']['message']['dob'] !== undefined){

					errorString += 'You must enter your date of birth as month and year.\n';
				}
				if (dataObject['errors']['message']['email'] !== undefined){

					errorString += 'Please enter a valid email address.\n';
				}
				if (dataObject['errors']['message']['zip'] !== undefined){

					errorString += 'Please enter a valid ZIP code.\n';
				}
				break;

			default:
				errorString = errorDecoder.createErrorString(dataObject);
		}

		return errorString;
	},

	//pull individual error messages and add a <br> between them
	createErrorString:function(dataObject)
	{
		var errorObject = dataObject['errors'];
		var errorMessageGroup = errorObject['message'];
		var returnErrorString = '';

		if (typeof errorMessageGroup === 'string')
		{
			returnErrorString = errorMessageGroup;
		}
		else
		{
			for(var key in errorMessageGroup) {
				trace("ERROR MESSAGE KEY: " + key + "   ERROR MESSAGE: " + errorMessageGroup[key][0]);
				if(typeof errorMessageGroup[key] === 'string')
				{
					trace("error message is string");
	    			returnErrorString += errorMessageGroup[key];
	    			returnErrorString += '<br>';
				}
				else if (typeof errorMessageGroup[key] === 'array')
				{
					trace("error message is array");
					for (var i = 0; i < errorMessageGroup[key].length; i++)
					{
		    			returnErrorString += errorMessageGroup[key][i];
		    			returnErrorString += '<br>';
					}
				}
				else
				{
					trace("error message is OBJ - or not string or array");
					for(var subkey in errorMessageGroup[key])
					{
		    			returnErrorString += errorMessageGroup[key][subkey];
		    			returnErrorString += '<br>';
					}
				}
    		}
		}

		return  returnErrorString;

	}

};


/**
 * Reads the image selected by the user and stores the data to be displayed
 * @param  {Event}    e        The 'change' event on the file field
 * @param  {Function} success  The function that will handle displaying and storing the image data
 * @param  {Function} error    A function to handle errors
 * @param  {Number}   maxSize  The maximum size in bytes for the image
 * @return {none}
 */
function uploadImage(e,success,error,maxSize){
	var reader = new FileReader();
    reader.onload = function(e){
    	if (e.total > maxSize){ //if the uploaded file exceeds the maximum file size
    		error("Image exceeds maximum file size.");
    		return;
    	}

        var img = new Image();
        img.onload = function(){
            success(this,e.target.result);
        }

        img.src = e.target.result;
    }

    reader.readAsDataURL(e.target.files[0]);
}

/**  start vid galleries***/

/** end vid galleries */


function trimWhiteSpace(x) {
	if (x == null){
		return '';
	}
    return x.replace(/^\s+|\s+$/gm,'');
}

function getSocialHtml(socialNetwork, post, containingPage, item_number) {
	var days = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"];
	var months = ["", "Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];

	function getThreeLetterMonth(n){
		return months[Number(n)];
	}

	function getThreeLetterDayOfWeek(day, month, year){
		if (day.length > 2){
			day = day.substr(0,2);
		}

		if (month.length > 2){
			month = month.substr(0,2);
		}

		if (year.length > 4){
			year = year.substr(0,4);
		}

		var d = new Date(year, month, day, 0, 0, 0, 0);
		//trace(d);
		//trace(d.getDay());
		return days[d.getDay()];
	}

	function formatTwitterDate(str){
		str = str || "";

		if (str == ""){
			return "";
		}

		str = trimWhiteSpace(str); //twitter already has the correct format so we just need to remove whitespace

		return str;
	}

	function formatFacebookDate(str){
		//trace("str=>"+str);
		str = str || "";

		//trace("str=>"+str);

		if (str == ""){
			return "";
		}

		//trace("str=>"+str);

		str = trimWhiteSpace(str);

		//trace("str=>"+str);

		var a = str.split(":");
		//trace(a);
		var b = a[0].split("-");
		//trace(b);

		if (b[2].length > 2){
			b[2] = b[2].substring(0,2);
		}

		if (b[1].length > 2){
			b[1] = b[1].substring(0,2);
		}

		if (b[0].length > 4){
			b[0] = b[0].substring(0,4);
		}

		return getThreeLetterDayOfWeek(b[2], b[1], b[0]) + " " + getThreeLetterMonth(b[1]) + " " + b[2];
	}

	function formatYoutubeDate(str){
		str = str || "";

		if (str == ""){
			return "";
		}

		str = trimWhiteSpace(str);

		return str;
	}

	function formatInstagramDate(str){
		str = str || "";

		if (str == ""){
			return "";
		}

		str = trimWhiteSpace(str);
		str = Number(str * 1000);

		var d = new Date(str);

		str = days[d.getDay()] + " " + months[d.getMonth() + 1] + " " + d.getDate();

		return str;
	}

    var html = "",
    	link="#",
    	picture="",
    	time="",
    	message="",
    	networkDisplayName="",
    	maxMessageLength=165;

    if (socialNetwork == "facebook"){
    	if (post.picture == undefined){
    		trace("error, facebook post not found");
    		return "";
    	}

    	if (Array.isArray(post.picture)){
    		picture = post.picture[0].source;
    	} else {
    		picture = post.picture;
    	}
    	message = post.post.message;
    	time = formatFacebookDate(post.post.created_time);
    	networkDisplayName = "Facebook";
    	link = post.post.link;
	} else if (socialNetwork == "twitter"){
		picture = "none";

		if (post.entities == undefined){
			trace("error, twitter post not found");
			return "";
		}

		if (post.entities.media){
			if (post.entities.media.type == "photo"){
				picture = post.entities.media.media_url;
			}
		}
    	message = post.text;
    	time = formatTwitterDate(post.created_at);
    	networkDisplayName = "Twitter";

    	if (post.html) {
    		link = post.html.url;
    	} else if (post.entities.url){
    		link = post.entities.url.urls[0].url;
    	} else if (post.entities.urls) {
    		if (post.entities.urls.length == 0) {
    			if (post.extended_entities){
    				link = post.extended_entities.media[0].expanded_url;
    			} else {
    				link = "#";
    			}
    		} else {
	    		link = post.entities.urls[0].url;
	    	}
    	} else {
    		trace("error");
    		trace(post.entities);
    	}
	} else if (socialNetwork == "instagram"){
		if (post.created_time == undefined){
			trace("error, instagram post not found");
			return "";
		}
    	picture = post.images.standard_resolution.url;
    	message = post.caption.text;
    	time = formatInstagramDate(post.created_time);
    	networkDisplayName = "Instagram";
    	link = post.link;

    	if (picture.indexOf("s612x612") > -1){
    		picture = picture.split("s612x612").join("s640x640");
    	}

	} else if (socialNetwork == "youtube"){
		if (post.thumbnails == undefined){
			trace("error, youtube post not found.");
			return "";
		}
    	picture = post.thumbnails.high.url;
    	message = post.title;
    	time = getDateFormat(post.published_at);
    	networkDisplayName = "Youtube";
    	link = "https://www.youtube.com/watch?v=" + post.id;
	}

	if (message.length > maxMessageLength){
		message = message.substring(0,maxMessageLength) + "...";
	}

	html += '<li class="social_item '+socialNetwork + ((picture != "none" && picture != "") ? "" : " no_image")+'">';
	html += '    <div class="social_image">';
	if (picture !== "none"){
	    html += '        <a href="'+link+'" target=\"_blank\" class="' + containingPage + '-overview-social-'+socialNetwork+'-'+item_number+'"><img class="socialPostImage" src="'+picture+'" alt="'+networkDisplayName+'"></a>';
	}
    html += '        <div class="social_icon"></div>';
    html += '    </div>';
    html += '    <div class="social_text">';
    html += '        <div class="social_source">';
    html += '            <a href="'+link+'" target=\"_blank\" class="'+containingPage+'-overview-social-'+socialNetwork+'-'+item_number+'">' + networkDisplayName + '</a>';
    html += '        </div>';
    html += '        <div class="social_date">';
    html += '            ' + time;
    html += '        </div>';
    html += '        <div class="social_content">';
    html += '            <div class="social_content_sub">';
    html += '            	<a href="'+link+'" target=\"_blank\" class="'+containingPage+'-overview-social-'+socialNetwork+'-'+item_number+'">' + message + '</a>';
    html += '            </div>';
    html += '        </div>';
    html += '    </div>';
    html += '</li>';

    return html;
}

function fetchSocialItem(socialNetwork, container, page, containingPage){
	var XAUTH_TOKEN = "abcde",
		containingPage = containingPage || "";

	// xdm Ajax call to API
	xAjax({
        url: "/1.0/social/"+socialNetwork+"?label=" + page,
        method: "GET",
        headers: {
           "x-auth-token": XAUTH_TOKEN
        },

        success: function(_result){
			trace("\n\nSUCCESS " + socialNetwork + JSON.stringify(_result) );

            if (_result.status != "ok") {
                trace('Error ' + socialNetwork + ': ' + _result.status);
                return;
            }

            if (_result.data.items.length == 0){
                trace('no results');
                return;
            }


			var html = "";

			for (var i=0, len=_result.data.items.length; i<len; i++) {
				html += getSocialHtml(socialNetwork, _result.data.items[i], containingPage, i);
			}

            $(container).append(html);
        },

        error: function(_result){
        	trace("ERROR " + JSON.stringify(_result) );
        }
    });
}

function backendLogout(response){
	trace("backendLogout was called");
	// trace('Not logged in or an issue with the API. so I\'m killing the cookie, and resetting the name in the upper left. The check returned ---: ');
	// console.dir(response);
	// $("#btn_my_jeopardy").text("MY PROFILE");

	// userStatus.userSignedOut();
	// // userStatus.eraseCookie();  go oldschool below
	// document.cookie = 'jeopuserstatus=; expires=Thu, 01 Jan 1970 00:00:01 GMT;';
	// updateHeaderForLogInStatus(false);
	// userStatus.signedIn = false;

	try{
		//logout of the api server, just a quick fix
		xAjax({
			url: "/1.0/users/logout",
			method: "GET",
			headers: {
			"x-auth-token": "abcde"
			},
			success: function(){
				trace("Logged out of BE succesfully");
				userStatus.userSignedOut();
			},
			error: function(){
				trace("Couldn't logout of BE succesfully")
			}
		});

	}catch(e){
		trace("The endpoint returned something weird - msg: " +e );
	}
}

function backendUserCheck(cb){

	xAjax({
            url: "/1.0/users/check",
            method: "GET",
            headers: {
               "x-auth-token": "abcde"
            },

            success: function(response){

				if(response.errors.message == "Not logged in."){
					trace("Not Logged in ");
					userStatus.userSignedOut();


					if(cb) {
						cb(false);
					}
					//return false;

				}else{
					trace('!--------------------Logged in! The check returned:');
					console.dir(response);


					trace('testcookieid: '+userStatus.readCookie('jeopuserstatus'));
					if(userStatus.readCookie('jeopuserstatus') == null){ // if the cookie was deleted then populate the status on the page
						userStatus.userSignedIn(response.data.id,response.data.username,response.data.session_id,response.data.login_type);
						trace("cookie readded");
					}

					if(cb) {
						cb(true);
					}
					//return response;

				}

            },

            error: function(response){
            	trace('Error with the API : will log out ');
					console.dir(response);
					userStatus.userSignedOut();

					if(cb) {
						cb(false);
					}
					//return false;

            }
        });
}


function animateNavMobile(nav){
	var height = 0,
		heightPerElement = $(".nav_item").outerHeight(),
		visibleItems = $(".nav_item a:visible").length;

	if ($(nav).hasClass("open")){
		height = visibleItems * heightPerElement;
	}

	$(nav).css({
		"height":height + "px"
	});
}
/*
/ DOCUMENT READY
*/
$(document).ready(function(){
	var html = "";
	html += '<div id="portrait_message">This site is best viewed in a landscape orientation.  Please rotate your device.</div>';

	if ($("#portrait_message").length == 0){
		$("body").prepend(html);
	}

	var initScale = 0.5,
		isTablet = (/ipad|hp-tablet/gi).test(navigator.appVersion);

	if(isTablet){
		initScale = 1;
	}

	trace('initScale->'+initScale);
	trace('$("meta[name=viewport]").length->'+$("meta[name=viewport]").length);

	if ($("meta[name=viewport]").length == 0){
		$("head").append('<meta name="viewport" content="width=device-width, initial-scale='+initScale+'" /> ');
	} else {
		$("meta[name=viewport]").attr('content', 'width=device-width, initial-scale=' + initScale);
	}

	trace('userStatus.isUserLoggedIn()->'+userStatus.isUserLoggedIn());
	updateHeaderForLogInStatus(userStatus.isUserLoggedIn());

	$(".story").click(function(e){
		var url = $(this).children("a").attr('href');
		window.location.href = url;
	});

	$(".story").hover(
		function(){
			var url = $(this).children("a").attr('href');
			window.status = firstPartOfURL() + "/" + url;
		},
		function(){
			window.status = "";
		}
	);

	var	newsIcons = ["", "alex", "contestants", "pop", "show", "crew", "press", "ask"],
		newsIconsMatrix = {"alextrebek" : "alex", "contestants" :"contestants", "popculure" : "pop", "theshow" : "show", "cluecrew" : "crew", "press" : "press", "weask" : "ask"};

	$(".ribbon").each(function(i){
		var rawcat = trimWhiteSpace($(this).text()),
			newcat = rawcat.replace(/ /g,'').toLowerCase();

		$(this).addClass(newsIconsMatrix[newcat]);
	});

	$(".contestant_name,.contestant_streak_name").each(function(e){
		$(this).text($(this).text().split(" null").join(""));
	});

	$("#icon_mobile_menu").click(function(e){
		e.preventDefault();
		e.stopPropagation();
		var nav = $("#nav");

		$(nav).toggleClass("open");

		animateNavMobile(nav);
	});

	if (userStatus.isUserLoggedIn()){ //display username in header

		u_name = userStatus.getUserName();

		if(u_name == false){
			backendLogout();
			u_name = "MY PROFILE";
		}
		$("#btn_my_jeopardy").text(u_name);
	}

	var touchEvent = ('ontouchstart' in document.documentElement);

	if (touchEvent){
		$("body").addClass("touch-device");
	}

	/*===================================
	These click events allow for the entire nav item to be clickable without having the change the page structure significantly.
	===================================*/
	$(".nav_item .sub_menu a").click(function(e){
		return true;
	});

	$(".nav_item .sub_menu").click(function(e){
		e.stopPropagation();
	});

	$(".nav_item").click(function(e){
		var subMenu = $(this).children(".sub_menu");

		if ($(this).children("a:first-child").attr('href').indexOf("http") == -1){
			e.preventDefault();
			e.stopPropagation();
		} else {
			return true;
		}

		if (isMobile) {
			if (!subMenu.is(':visible') && subMenu.length > 0) {
				$(".sub_menu").hide().removeClass("mobileOpen"); //hide other menus
				subMenu.show().addClass("mobileOpen"); //show this menu

				animateNavMobile($("#nav"));

				$(".nav_item.active").removeClass('active');
				$(this).addClass('active');

				return;
			}
		}

		//if the nav is already open and they click on the item again it will go to that link so those pages are still accessible
		window.location.href = firstPartOfURL() + $(this).children("a:first-child").attr('href');
	});

	// disabling the last three items on the menu per bug #2176. Update the shared global header when this is removed

	$(".nav_item.tempdisabled").unbind('click');

	$(".date_format").each(function(e){
		$(this).text(getDateFormat($(this).text()));
	});

	$("#share_icons li:first-child").click(function(e){
		e.preventDefault();
		e.stopPropagation();

		$("#share_icons").toggleClass("open");
	});

	$("#search_field").attr('data-initial-value', $("#search_field").val());

	$("#search_field").click(function(e){
		if ($(this).val() == $("#search_field").attr('data-initial-value')) {
			$(this).val('');
		}
	});

	$("#search_form").submit(function(e){
		e.preventDefault();
		e.stopPropagation();
		return false;
	});

	$("#search_field").keypress(function(e){
		var keycode = (e.keyCode ? e.keyCode : e.which);
		trace('search field key:' + keycode);
        if (keycode == '13') {
        	e.preventDefault();
			e.stopPropagation();

        	var txt = $("#search_field").val();

			if (txt == $("#search_field").attr('data-initial-value') || txt == "") {
				return;
			}

			submitSearch(txt);
        }
	});

	$("#search_field").change(function(){
		$("#search_form #q").val($(this).val());
	});

	$("#search_icon").click(function(e){
		e.preventDefault();
		e.stopPropagation();

		var txt = $("#search_field").val();

		if (isMobile){
			$("#search_form").attr({
				'action':firstPartOfURL() + "/search",
				'method':'GET'
			});

			$("#search_field").css({
				'display':'block',
				'position':'absolute',
				'z-index':999,
				'right':'0'
			});

			$("#search_field").focus().val('');


		} else {
			if (txt == $("#search_field").attr('data-initial-value')) {
				return;
			}

			submitSearch(txt);
		}
	});

	//add Log Out listener
	$('#header_logout_btn').click(function(e){
		e.preventDefault();
		e.stopPropagation();
		backendLogout();
		window.setTimeout(function(){window.location.reload(true);},600);

		// window.location = '/signin';
	});


	//add listeners
	resizeManager.init();
	$( window ).resize(resizeManager.handelResize);
	resizeManager.handelResize();

	//fill in username on page when needed
	var userName = userStatus.getUserName();
	trace("checking user name - is:"+userName);
	if (userName)
	{	trace("updateing user name");
		$('.autofill_username').html(userName);
	}else{
		trace("bs cookie - signing out name ")
		userStatus.signedIn = false;
	}

	$("#share_icons .sprite, .clue_facebook, .clue_twitter, #news_article_social a, .share a, #jbuzz_article_social a, #j6 .share_facebook, .congrats_share_links .share_facebook").click(function(e){
		e.preventDefault();
		e.stopPropagation();

		var url="",
			facebookBase="https://www.facebook.com/sharer/sharer.php?u=",
			twitterBase="https://twitter.com/intent/tweet?text=";


			// pull custom share info from meta tag ... how to code at midnight....

			var social_element = document.querySelector('meta[property="og:title"]');
			var s_content = (social_element != null ) ? social_element && social_element.getAttribute("content") : "";

			var custom_text = (s_content.length > 2 ) ? s_content : "";


		if ($(this).hasClass("share_facebook")){
			url = facebookBase + encodeURIComponent(window.location.href);
		} else if ($(this).hasClass("share_twitter")){
			if(custom_text.length > 5 ){

				url = twitterBase + encodeURIComponent(custom_text) + " " + encodeURIComponent(window.location.href);
			}else{
				url = twitterBase + encodeURIComponent(document.title) + " " + encodeURIComponent(window.location.href);
			}

		} else if ($(this).hasClass("share_google")){
			url = "https://plus.google.com/share?url=" + encodeURIComponent(window.location.href);
		} else if ($(this).hasClass("share_pagelink")){
			//url = "";
			return;
		} else if ($(this).hasClass("share_email")){
			url= "mailto:?&subject="+encodeURIComponent(document.title)+"&body=" + encodeURIComponent(window.location.href);
		} else if ($(this).hasClass("clue_facebook")){
			//updated this to point to the inifinte-jeopardy share
			// url = facebookBase + encodeURIComponent(window.location.href + "#clue");
			url = facebookBase + encodeURIComponent(window.location.href + "/infinite-jeopardy");
		} else if ($(this).hasClass("clue_twitter")){
			url = twitterBase + encodeURIComponent("Every Final Jeopardy! clue from the past 30+ years. Exactly as it originally aired. On a random loop. ") + " " + encodeURIComponent(window.location.href)+"/infinite-jeopardy";
		}

		window.open(url, "share");
	});

	$(".jeopardyWYouMayAlsoLikeGlobal a, .jeopardyWContestantsHomeHeader a").each(function(i){
		if ($(this).attr('href').indexOf("youtube.com") > -1 || $(this).attr('href').indexOf("youtu.be") > -1){
			$(this).addClass('video');
			//add the title that will be populated in the pop_up
			var vid_title = $(this).parent().siblings('h2').text();
			$(this).append("<h3 class='video_title'>"+vid_title+"</h3>");

		}
	});

	if (!("placeholder" in document.createElement("input"))) { //fallback for placeholder attribute on older browsers
		$("input[placeholder], textarea[placeholder]").each(function() {
			var val = $(this).attr("placeholder");
				if ( this.value == "" ) {
				this.value = val;
			}$(this).focus(function() {
				if ( this.value == val ) {
					this.value = "";
				}
			}).blur(function() {
				if ( $.trim(this.value) == "" ) {
					this.value = val;
				}
			})
		});
		// Clear default placeholder values on form submit
		$('form').submit(function() {
			$(this).find("input[placeholder], textarea[placeholder]").each(function() {
				if ( this.value == $(this).attr("placeholder") ) {
					this.value = "";
				}
			});
		});
	}
});

function submitSearch(q){
	if (q == ""){
		return;
	}

	var searchURL = firstPartOfURL() + "/search?q=" + encodeURIComponent(q);

	trace('firstPartOfURL()->'+firstPartOfURL());
	trace('q->'+q);
	trace('searchURL->'+searchURL);

	window.location.href=searchURL;
}

function firstPartOfURL(){
	var str;

	if (window.location.href.indexOf("www.jeopardy.com") > -1) {
		str = location.protocol + "//www.jeopardy.com";
	} else {
		var siteStr = "/Jeopardy";
		var index = window.location.href.indexOf(siteStr);

		//str = [location.protocol, '//', location.host, location.pathname].join('');
		str = [location.protocol, '//', location.host].join('');

		if (index > -1){
			str = str.substring(0, index + siteStr.length);
		}
	}

	if (str.substring(str.length-1, str.length) == "/") { //remove trailing slashes
		str = str.substring(0, str.length-1);
	}

	//trace(str);

	return str;
}

function rotateContentSet(selector){
	if ($(selector).length == 0) { //don't set up an unnecessary interval
		return;
	}

	$(selector+":not(:eq(0))").hide(); //hide all but the initial element

	setInterval(function(){
		var a = selector.split(" ");

		$(selector).each(function(i){
			if ($(this).is(":visible")) {
				$(this).fadeOut("slow");

				var len = $(this).siblings(a[1]).length;
				var index = $(this).index();

				if (index + 1 > len) {
					$(this).siblings(a[1] + ":eq(0)").fadeIn("slow");
				} else {
					$(this).siblings(a[1] + ":eq("+(index)+")").fadeIn("slow");
				}

				return false;
			}
		});
	}, 5000);
}

function updateHeaderForLogInStatus(isUserLoggedIn){

	if (isUserLoggedIn)
	{
		trace("user signed in");
		//$('#header_logout_btn').show();
		//$('#btn_sign_in').hide();
		$('#btn_my_jeopardy').text(userStatus.userName);
		$('.show_on_logged_in').show();
		$('.hide_on_logged_in').hide();

	}
	else
	{
		trace("user signed out");
		//$('#header_logout_btn').hide();
		//$('#btn_sign_in').show();
		$('.show_on_logged_in').hide();
		$('.hide_on_logged_in').show();

	}

}

function validateEmail(email) {
	var re = /^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
	return re.test(email);
}