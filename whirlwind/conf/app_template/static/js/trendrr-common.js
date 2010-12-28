var Trendrr = {};

//test for the console..
if(!(window['console'])){ 
	if (window.console) {
		console = window.console;
	} else {
		console = {};
		console.log = function() {};
	}
}

/**
 * assumes the template has named variable in the form 
 * 
 * will unescape {} symbols, as firefox mistakenly fucks things up sometimes.
 * 
 * {varName} and has a corresponding value in teh options 
 */
Trendrr.evalTemplate = function(htmlTemplate, options) {
	var syntax = /(\{(\w+)\})/g; //matches symbols like '{id}'
	
	if (!options) {
		return htmlTemplate;
	}
	
	if (!Trendrr.isString(htmlTemplate)) {
		return htmlTemplate;
	}
	htmlTemplate = htmlTemplate.replace('%7B', '{').replace('%7D', '}');
	htmlTemplate = htmlTemplate.replace('%7b', '{').replace('%7d', '}');
	var html = htmlTemplate.replace(syntax, function(match,group1) {
		var tmp = match.replace('{','');
		tmp = tmp.replace('}','');
		if (typeof options[tmp] != 'undefined' && options[tmp] != null) {
			return options[tmp];
		}
		return match;
	});
	return html;
};


Trendrr.isFunction = function(obj) {
	//console.log("testing is function %o", obj);
	if (!obj) {
		return false;
	}
	return $.isFunction(obj);
};

Trendrr.isString= function(obj) {
	if (!obj) {
		return false;
	}
	if (obj instanceof String) {
		return true;
	}
	if (typeof(obj) == 'string') {
		return true;
	}
	return false;
};


Trendrr.isNumber = function(obj) {
	return typeof(obj) == 'number';
};



Trendrr.isTrue = function(obj) {
	if (!obj) {
		return false;
	}
	if (obj == 'true') {
		return true;
	}
	if (obj == true) {
		return true;
	}
	//TODO;check if this is checkbox
	
	return false;
}


Trendrr.isArray = function(obj) {
	if (!obj) {
		return false;
	}
	return $.isArray(obj); 
};

/**
 * Will convert passed in element to a date (when possible)
 * 
 * this requires the date.js to work.
 * will successfully parse iso dates of all styles. 
 * 
 */
Trendrr.toDate = function(date) {
	if (!date) {
		return null;
	} 
	if (date instanceof Date) {
		return date;
	}
	if (Trendrr.isFunction(date.match) && date.match(/[^0-9]/)) {
//		"2010-04-02T18:29:11.976Z"
		
		//remove millisecond field if exists.
		date = date.replace(/\.\d\d\d/, '');

		//formated date..
		if (Trendrr.stringEndsWith(date,'-00:00') || Trendrr.stringEndsWith(date,'+00:00')) {
			//we need to fix a date.js bug where +00:00 timezone 
			//defaults to local time.
			var dt = date.replace(/[\-\+]{1}00\:00/, "+01:00");
			console.log(dt);
			var d = Date.parse(dt);
			if (d) {
				return d.addHours(1);
			}
		}
		
		var d = Date.parse(date);
		if (d) {
			if (Trendrr.stringEndsWith(date, 'Z')) {
				//convert to local time.. 
				d.addMinutes(-new Date().getTimezoneOffset());
			}	
			
			return d;
		}
		if (!d) {
			//twitter date..
			d = Date.parseExact(date, 'E, dd NNN yyyy HH:mm:ss Z');
			if (d) {
				return d;
			}	
		}
		
	} else {
		return new Date(date *1000);
	}
};


/**
 * Serializes the passed in element into an object.
 * uses all input elements below the passed in element.
 * 
 * 
 */
Trendrr.serialize = function(element) {
	var params = {};
	$(element).find(':input').each(function(i) {
		if (!($(this).data('iptrMsgDisplayed')) &&
			this.name && !this.disabled &&
				(this.checked || /select|textarea/i.test(this.nodeName) ||
					/text|hidden|password/i.test(this.type))) {
			if (params[this.name]) {
				if (!Trendrr.isArray(params[this.name])) {
					var tmp = params[this.name];
					params[this.name] = [];
					params[this.name].push(tmp);
				}
				params[this.name].push($(this).val());
			} else {
				params[this.name] = $(this).val();
			}			
		}

	});
	return params;
};


/**
 * gets the value from an input element,
 * or sets the value if passed in
 * returns the value 
 */
Trendrr.value = function(elem, value) {
	if ($(elem).size() == 0)
		return;
	var dom = $(elem).get(0)
	if (typeof value != 'undefined') {
		dom.value = value;
		return value;
	} else {
		if($(elem).attr('type') == 'checkbox') {
			if (dom.checked)
				return true;
			return false;
		} else if ($(elem).attr('type') == 'radio') {
			return $(elem).val();
		}
		return dom.value;
	}
};

/**
 * trims off whitespace from front and end of string, 
 * if second param is specified will trim that off instead of whitespace.
 * 
 * ex: 
 * Trendrr.trim(' string '); => 'string'
 * Trendrr.trim('trendrr', 'r'); => 'trend'
 */
Trendrr.trim = function(str, trim) {
	if (!str) {
		return str;
	}
	if (!trim) {
		return jQuery.trim(str);
	}
	var tmp = str;
	while(Trendrr.stringStartsWith(tmp, trim)) {
		tmp = tmp.slice(trim.length);
	}
	while(Trendrr.stringEndsWith(tmp, trim)) {
		tmp = tmp.slice(0, tmp.length-trim.length);
	}
	return tmp;
};

/**
 * 
 * Will take a string or dict as params.
 * Trendrr.href(urlString) will change the page to the passed in url.
 * 
 * options
 * url => url to work from (default to window location)
 * params => will replace any params in the query string 
 * forward => (default true)if true will not return, but rather forward browser to the newly generated url.
 *  			if false will return the updated url
 * clearParams = (default false) if true will clear all url params before the params are applied
 */
Trendrr.href = function(options) {
	if (Trendrr.isString(options)) {
		options = {url:options};
	}
	var opts = $.extend({
		url : window.location.href,
		forward : true,
		clearParams : false,
		params : {}
	}, options);

	var u = opts.url;
	
	//strip local link
	u = u.split('#')[0];
	if (opts.clearParams) {
		u = u.split('?')[0];
	}
	
	
	if (u.indexOf('?') == -1) {
		u += '?';
	}
	$.each(opts.params, function(i, val) {
		var regex = new RegExp('\\&*' + i + '=[^\\&]*');
		u = u.replace(regex, '');
		u += '&' + i + '=' + this;
	});
	console.log(opts);
	if (opts.forward) {
		window.location.href = u;
	} else {
		return u;
	}
};


/**
 * tests wether the element is currently visible
 * to be visible the element must not have display:none, and
 * must be with the current scrollpane.,
 */
 
Trendrr.isVisible = function(element) {
	if (!element) {
		return false;
	}
	var elem = $(element);

	if (elem.size() == 0) {
		return false;
	}

	if (!elem.is(':visible')) {
		return false;
	}

	if (elem.hasClass('ui-offscreen')) {
		return false;
	}
	if (elem.closest('.ui-offscreen').size() > 0) {
		return false;
	}
	
	var measure = Trendrr.measure(elem);
	
	if ($(document).scrollTop() > (measure.top + measure.height)) {
		return false;
	}
	if ((measure.left + measure.width) < 1) {
		return false;
	}
	return true;
};

/**
 * formats numbers 
 * like 
 * 1.5M
 * 1,000
 * 10,000
 * 1.2K
 * 
 * 
 */
Trendrr.formatNumber = function(number) {
	var str = '';
	var unit = '';
	
	if (number < 10000) {
		str = number + ''; //TODO: add comma
	} else if (number < 1000000) {
		var val = number / 1000;
		str = val.toPrecision(4) + "K";
		unit = "K";
	} else if (number < 1000000000) {
		var val = number / 1000000;
		str = val.toPrecision(4) + "M";
		unit = "M";
	} else {
		//billions
		var val = number / 1000000000;
		str = val.toPrecision(4) + "B";
		unit = "B";
	}
	
	str = str.replace(/\.0+[A-Za-z]+/, '');
	str = str.replace(/(\.[1-9]*)0+[A-Za-z]+/, '$1');
	
	return str + unit;
	
};