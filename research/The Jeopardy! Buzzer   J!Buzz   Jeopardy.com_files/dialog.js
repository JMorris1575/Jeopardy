/**
 * @module dialog
 *
 * @description
 * <p>Creates stylable modal dialog boxes to replace the default browser dialog boxes.</p>
 *
 * @example
 * // trigger an alert dialog
 * dialog.alert('Alert!');
 *
 * // trigger a prompt dialog
 * dialog.prompt('what\'s your name?',function(data){
 *   // do something with user's response
 * });
 *
 * // trigger a confirm dialog
 * dialog.confirm({
 *   msg : 'Do you want to Proceed?',
 *   confirm : 'yes',
 *   cancel : 'no'
 * },function(){
 *   // do confirmed action
 * },function(){
 *   // do canceled action
 * });
 *
 * @tutorial  dialog
 */
(/** @lends module:dialog */ function(n,undefined) {
	"use strict";

	var mask = $('<div id="dialog_mask"/>'),
		container = $('<div class="dialog"/>'),
		input = $('<input type="text" name="prompt"/>'),
		confirmBtn = $('<button class="confirm"/>'),
		cancelBtn = $('<button class="cancel"/>'),
		closeBtn = $('<button class="close" id="btn_close_modal"/>'),
		defaults = {
			cancel : "cancel",
			confirm : "ok",
			close : "close",
			fadeSpeed : "slow",
			plainText : true
		};

	/**
	 * Create an 'alert' type modal dialog
	 * @arg  {(Object|String)}    settings  Customized text to display in this dialog. You can supply just the text of the dialog in a string or supply an object to customize the button text and/or fade speed as well.
	 * @param  {string} settings.msg Message to display in the dialog.
	 * @param  {string} [settings.cancel = 'cancel'] Text to display on the cancel button
	 * @param  {string} [settings.confirm = 'ok'] Text to display on the confirm button
	 * @param  {(string|number)} [settings.fadeSpeed = 'slow'] Speed to fade in/out the dialog
	 * @param {bool} [settings.plainText = true] (replaces '\n\n' with paragraph break. replaces '\n' with line break)
	 * @arg  {Function}  [onTrue]    Callback to fire when the user clicks the confirm button.
	 */
	function alert(settings,onTrue){
		dialog('alert',settings,onTrue);
	}

	/**
	 * Create a standard modal dialog with a close button
	 * @arg  {(Object|String)}    settings  Customized text/markup to display in this dialog. You can supply just the text/markup of the dialog in a string or supply an object to customize the button text and/or fade speed as well.
	 * @param  {string} settings.msg Message to display in the dialog. (replaces '\n\n' with paragraph break. replaces '\n' with line break)
	 * @param  {string} [settings.cancel = 'cancel'] Text to display on the cancel button
	 * @param  {string} [settings.confirm = 'ok'] Text to display on the confirm button
	 * @param  {(string|number)} [settings.fadeSpeed = 'slow'] Speed to fade in/out the dialog
	 * @param {bool} [settings.plainText = true] (replaces '\n\n' with paragraph break. replaces '\n' with line break)
	 * @arg  {Function}  [onTrue]    Callback to fire when the user clicks the confirm button.
	 */
	function modal(settings,onTrue){
		dialog('modal',settings,onTrue);
	}

	/**
	 * Create a 'prompt' type modal dialog
	 * @arg  {(Object|String)}    settings  Customized text to display in this dialog. You can supply just the text of the dialog in a string or supply an object to customize the button text and/or fade speed as well.
	 * @param  {string} settings.msg Message to display in the dialog. (replaces '\n\n' with paragraph break. replaces '\n' with line break)
	 * @param  {string} [settings.cancel = 'cancel'] Text to display on the cancel button
	 * @param  {string} [settings.confirm = 'ok'] Text to display on the confirm button
	 * @param  {(string|number)} [settings.fadeSpeed = 'slow'] Speed to fade in/out the dialog
	 * @param {bool} [settings.plainText = true] (replaces '\n\n' with paragraph break. replaces '\n' with line break)
	 * @arg  {Function}  [onTrue]    Callback to fire when the user clicks the confirm button. Prompt dialog passes the value of the input field to this callback.
	 */
	function prompt(settings,onTrue){
		dialog('prompt',settings,onTrue);
	}

	/**
	 * Create a 'confirm' type modal dialog
	 * @arg  {(Object|String)}    settings  Customized text to display in this dialog. You can supply just the text of the dialog in a string or supply an object to customize the button text and/or fade speed as well.
	 * @param  {string} settings.msg Message to display in the dialog. (replaces '\n\n' with paragraph break. replaces '\n' with line break)
	 * @param  {string} [settings.cancel = 'cancel'] Text to display on the cancel button
	 * @param  {string} [settings.confirm = 'ok'] Text to display on the confirm button
	 * @param  {(string|number)} [settings.fadeSpeed = 'slow'] Speed to fade in/out the dialog
	 * @param {bool} [settings.plainText = true] (replaces '\n\n' with paragraph break. replaces '\n' with line break)
	 * @arg  {Function}  [onTrue]    Callback to fire when the user clicks the confirm button.
	 * @arg  {Function}  [onFalse]   Callback to fire when the user clicks the cancel button.
	 */
	function confirm(settings,onTrue,onFalse){
		dialog('confirm',settings,onTrue,onFalse);
	}

	/**
	 * Creates stylable modal dialog boxes to replace the default browser dialog boxes
	 * @arg  {string}    type      Specify the type of dialog you'd like to display. ('alert'|'prompt'|'confirm')
	 * @arg  {(Object|String)}    settings  Customized text to display in this dialog. You can supply just the text of the dialog in a string or supply an object to customize the button text and/or fade speed as well.
	 * @param  {string} settings.msg Message to display in the dialog. (replaces '\n\n' with paragraph break. replaces '\n' with line break)
	 * @param  {string} [settings.cancel = 'cancel'] Text to display on the cancel button
	 * @param  {string} [settings.confirm = 'ok'] Text to display on the confirm button
	 * @param  {(string|number)} [settings.fadeSpeed = 'slow'] Speed to fade in/out the dialog
	 * @param  {bool} [settings.plainText = true] (replaces '\n\n' with paragraph break. replaces '\n' with line break)
	 * @arg  {Function}  [onTrue]    Callback to fire when the user clicks the confirm button. Prompt dialog passes the value of the input field to this callback.
	 * @arg  {Function}  [onFalse]   Callback to fire when the user clicks the cancel button. (only applies to confirm dialog)
	 *
	 * @private
	 */
	 function dialog(type,settings,onTrue,onFalse) {
		var txt		= settings.msg,
			cncl	= settings.cancel		|| defaults.cancel,
			ok		= settings.confirm		|| defaults.confirm,
			close	= settings.close		|| defaults.close,
			spd		= settings.fadeSpeed	|| defaults.fadeSpeed,
			pt		= settings.plainText	|| defaults.plainText;

		clearDialog();
			
		if(typeof settings == 'string') {
			txt = settings;
			settings = defaults;
			settings.msg = txt;
		}
		if(pt && typeof txt == 'string') {
			settings.msg = '<p>'+txt.replace(/\n\n/gi, '</p><p>').replace(/\n/gi, '<br/>')+'</p>';
		} 
		confirmBtn.text(ok);
		cancelBtn.text(cncl);
		closeBtn.text(close);

		switch (type.toLowerCase()) {
			case "confirm":
				container.addClass('confirm').append(settings.msg,cancelBtn,confirmBtn);
			break;

			case "prompt":
				container.addClass('prompt').append(settings.msg,input,confirmBtn);
			break;

			case "alert":
				container.addClass('alert').append(settings.msg,confirmBtn);
			break;

			default: // "modal"
				container.addClass('modal').append(settings.msg,closeBtn);
		}

		mask.append(container);
		mask.appendTo('body').hide().fadeIn(spd);

		confirmBtn.off('click').on('click', function(){
			clearDialog(spd,onTrue,input.val());
		});

		cancelBtn.off('click').on('click', function(){
			clearDialog(spd,onFalse);
		});

		closeBtn.off('click').on('click', function(){
			clearDialog(spd,onTrue);
		});
	}

	/**
	 * close and empty the dialog contents
	 * @arg  {(string|number)}    spd       Speed to fade in/out the dialogs
	 * @arg  {Function}  [callback]  callback to fire when dialog has closed
	 * @arg  {Object}    [data]      data to pass to callback
	 * 
	 */
	function clearDialog(spd,callback,data) {
		spd		=  spd || settings.fadeSpeed || defaults.fadeSpeed;
		mask.fadeOut(spd,function(){
			mask.remove();
			input.val('');
			container.removeClass('alert prompt confirm modal').children('*').remove();

			if(typeof callback == 'function') callback(data);
		});
	}

	/**
	 * Set the default settings for all dialogs
	 * @arg  {Object}  set  
	 * @param {string} [set.cancel = "cancel"] cancel button text
	 * @param {string} [set.confirm = "ok"] confirm button text
	 * @param {(string|int)} [set.fadeSpeed = "slow"] fade in/out speed for modal
	 * @param {bool} [set.plainText = true] is the message input type plain text that should have line breaks converted to markup?
	 */
	function settings(set) {
		Object.keys(set).forEach(function(i){
			defaults[i] = set[i];
		});
	}

	// Public API
	n.ui = n.ui || {};
	n.ui.dialog = {
		alert : alert,
		prompt : prompt,
		confirm : confirm,
		modal : modal,
		settings : settings,
		clearDialog : clearDialog
	};

})(window.site=window.site || {});