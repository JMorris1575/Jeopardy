////////////////////////////////////////////////////////////////////////////
//
//     ______                _  __ ____  __  ___     __  __________    ____  __________ 
//    / ____/___ ________  _| |/ // __ \/  |/  /    / / / / ____/ /   / __ \/ ____/ __ \
//   / __/ / __ `/ ___/ / / /   // / / / /|_/ /    / /_/ / __/ / /   / /_/ / __/ / /_/ /
//  / /___/ /_/ (__  ) /_/ /   |/ /_/ / /  / /    / __  / /___/ /___/ ____/ /___/ _, _/ 
// /_____/\__,_/____/\__, /_/|_/_____/_/  /_/    /_/ /_/_____/_____/_/   /_____/_/ |_|  
//                  /____/                                                              
//     ________  ___   ______________________  _   _______
//    / ____/ / / / | / / ____/_  __/  _/ __ \/ | / / ___/
//   / /_  / / / /  |/ / /     / /  / // / / /  |/ /\__ \ 
//  / __/ / /_/ / /|  / /___  / / _/ // /_/ / /|  /___/ / 
// /_/    \____/_/ |_/\____/ /_/ /___/\____/_/ |_//____/  
//
//
//  TERMS
//	Terms so we all talk about it the same way:
//	API server - is the server being called via ajax
//	Client server - the server from which the main page is loaded
//
//  WHAT IT DOES
//	EasyXDM opens a new browser window, loaded from the "API" server.
//	Then it uses cross window communication to make the ajax call from a window that is 
//	loaded from the api server getting around cross domain issues 
//
//  PERCUSSION
//	In percussion - this should exist on each page as part of default includes
//	Right now this exists as global vars and functions.  This can be updated to
//	ties them to an object, or prototype if the group thinks it would make life easier.
//	
//	HOW TO USE
//	1.  Set up an object the same way you would for a normal ajax call
/*
    $.ajax({
    	type: "POST",
    	url: "URL",
    	data: DATATOSEND,
    	success: SUCCESSFUNCTION,
    	error:ERRORFUNCTION,
    	dataType: "json"
    });	
*/
//  would become
/*
    var object = {
        type: "POST",
        url: "URL",
        data: DATATOSEND,
        success: SUCCESSFUNCTION,
        error:ERRORFUNCTION,
        dataType: "json"
    });
//
//  2. Then send that object to the global function xAjax();
/*
    xAjax(object);
*/
//  2-ALT. You could use with a object literal, just like ajax
/*
    xAjax({
        type: "POST",
        url: "URL",
        data: DATATOSEND,
        success: SUCCESSFUNCTION,
        error:ERRORFUNCTION,
        dataType: "json"
    }); 
*/
//  3. Pour youself a Pepsi
//  
//
//  INCLUDES AND NEEDED SCRIPTS
//  The intention is for this to exist in a global header, but if that changes here is the needed code
//  <script type="text/javascript" src="/Assets/Jeopardy/easyxdm/easyXDM.js">
//  </script> <script type="text/javascript" src="/Assets/Jeopardy-/easyxdm/exdmTestFunctions.js">
//  </script> <script type="text/javascript"> easyXDM.DomHelper.requiresJSON("/Assets/Jeopardy/easyxdm/json2.js"); </script>
//
//
//  NOTES
//  The domain of the url to call is set in this file (in case it changes) so only include the url starting at "/api"
//  Right now we just directly pass the JSON back, if we want to implement some global error handeling or messagin, this would be the place.
//
//  *Thanks to Brian Hsiao for setting this up
//  **Like how the comments are longer then the script?                                                                                                                                                                        
//////////////////////////////////////////////////////////////////////////////////

// this is only bootstrapping code
var REMOTE = (function(){
    var remote = location.href;


/**
 * Comment this out and uncomment the switch below once the stage and Prod APIs have been created 
 */
    // switch (location.host) {
    //     case "provider.easyxdm.net":
    //         location.href = remote.replace("provider", "consumer");
    //         break;
    //     case "devtvg.com":
    //     	//trace("ON DEV");
    //         remote = 'https://api.dev.jeopardy.com/siteui/' ;
    //         break;

    //     case "consumer.easyxdm.net":
    //         remote = remote.replace("consumer", "provider");
    //         break;
    //     case "xdm1":
    //         remote = remote.replace("xdm1", "xdm2");
    //         break;
    //     case "briantestserver"://update location to use this
    //     	remote = 'http://ec2-54-191-27-27.us-west-2.compute.amazonaws.com/';
    //     break;

    //     case "wcms.sonypictures.com":
    //         remote = 'https://api.dev.jeopardy.com/siteui/';
    //     break;
    //     default:
    //     	//trace("ON DEFAULT");
    //         remote = 'https://api.jeopardy.com/siteui/';
    // }

/*********** End of Old boostrap *******************************/

/*********************************
 * This switch should be implemented once the stage and production API endpoints have been created
 ********************************/

    switch(location.host){

        /* Production */
        case "www.jeopardy.com" :
            remote = 'https://api.jeopardy.com/siteui/';
        break;

        /* Development */
        case "jeopardy.dev.tvg.la" :
            remote = 'https://api.dev.jeopardy.com/siteui/' ;
        break;

        /* Development instance 2 */
        case "wcms.sonypictures.com" :
            remote = 'https://api.stage.jeopardy.com/siteui/';
        break;

        /* Staging */
        case "stage2.jeopardy.com" :
            remote = 'https://api.stage.jeopardy.com/siteui/';
        break;

        /* Production */
        case "www2.jeopardy.com" :
            remote = 'https://api.jeopardy.com/siteui/';
        break;

        case "wcms.sonypictures.com" :
            remote = 'https://api.stage.jeopardy.com/siteui/';
        break;

        /* Testing XDM functionality */
        case "provider.easyxdm.net":
            location.href = remote.replace("provider", "consumer");
        break;

        case "jeopardy.dev" :
            remote = 'https://api.stage.jeopardy.com/siteui/';
        break;

        /* Default takes care of Percussion preveiw and live site  */
        default:
            remote: 'https://api.jeopardy.com/siteui/';
            // uncomment this once the Prod server is ready
            // remote: 'https://api.jeopardy.com/siteui/';

    }


    return remote.substring(0, remote.lastIndexOf("/"));
}());

// this is really what you are after
var xhr = new easyXDM.Rpc({
    local: "easyxdm/name.html",
    swf: REMOTE + "/easyxdm/easyxdm.swf",
    remote: REMOTE + "/easyxdm/cors/",
    remoteHelper: REMOTE + "/easyxdm/name.html"
}, {
    remote: {
        request: {}
    }
});


function xAjax(ajaxObj){
    xhr.request(
        {
            url: ajaxObj['url'],
            method: ajaxObj['method'],
            headers: ajaxObj['headers'],
            data: ajaxObj['data'],
            contentType: "text/xml; charset=\"utf-8\""
        }, 
        function(rpcdata){  //success
            var json = easyXDM.getJSONObject().parse(rpcdata.data);
            
            //add in error checks (server returned errors)
            /*
            if server responds with error
            {
                ajaxObj['error'](rpcdata);
            }
            else known error returned by server
            {
                ajaxObj['success'](rpcdata);
            }
            else
            {
               ajaxObj['success'](rpcdata); 
            }
            */

            ajaxObj['success'](json); 
        },
        function(rpcdata){
            if (ajaxObj['error'] != null)
            {
                //var json = easyXDM.getJSONObject().parse(rpcdata.data); 

                ajaxObj['error']({'error':rpcdata});  
            }
        }
    );

}



/** This is for the J6 game API endpoint  */

var jurl = location.href;
    isJ6 = (jurl.indexOf("j6") > -1 || jurl.indexOf("dashboard") > -1 ) ?  true : false ;

    if(isJ6){

        REMOTEJ = REMOTE.replace("api", "j6-api");
        console.log("using the j6 endpoint ")


        var jxhr = new easyXDM.Rpc({
            local: "easyxdm/name.html",
            swf: REMOTEJ + "/easyxdm/easyxdm.swf",
            remote: REMOTEJ + "/easyxdm/cors/",
            remoteHelper: REMOTEJ + "/easyxdm/name.html"
        }, {
            remote: {
                request: {}
            }
        });
    }


function j6Ajax(ajaxObj){

    // point to the j6 API server
    console.log('running the j6Ajax call');

    jxhr.request(
        {
            url: ajaxObj['url'],
            method: ajaxObj['method'],
            headers: {
             "x-auth-token": "abcde"
            },
            data: ajaxObj['data'],
            contentType: "text/xml; charset=\"utf-8\""
        }, 
        function(rpcdata){  //success
            var json = easyXDM.getJSONObject().parse(rpcdata.data);
            
            //add in error checks (server returned errors)
            /*
            if server responds with error
            {
                ajaxObj['error'](rpcdata);
            }
            else known error returned by server
            {
                ajaxObj['success'](rpcdata);
            }
            else
            {
               ajaxObj['success'](rpcdata); 
            }
            */

            ajaxObj['success'](json); 
        },
        function(rpcdata){
            if (ajaxObj['error'] != null)
            {
                //var json = easyXDM.getJSONObject().parse(rpcdata.data); 

                ajaxObj['error']({'error':rpcdata});  
            }
        }
    );

}