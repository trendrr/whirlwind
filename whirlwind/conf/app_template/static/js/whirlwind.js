var Whirlwind = {};

//test for the console..
window.log = function f(){ log.history = log.history || []; log.history.push(arguments); if(this.console) { var args = arguments, newarr; args.callee = args.callee.caller; newarr = [].slice.call(args); if (typeof console.log === 'object') log.apply.call(console.log, console, newarr); else console.log.apply(console, newarr);}};
(function(a){function b(){}for(var c="assert,count,debug,dir,dirxml,error,exception,group,groupCollapsed,groupEnd,info,log,markTimeline,profile,profileEnd,time,timeEnd,trace,warn".split(","),d;!!(d=c.pop());){a[d]=a[d]||b;}})
(function(){try{console.log();return window.console;}catch(a){return (window.console={});}}());

/**
 * assumes the template has named variable in the form 
 * 
 * will unescape {} symbols, as firefox mistakenly fucks things up sometimes.
 * 
 * {varName} and has a corresponding value in teh options 
 */
Whirlwind.evalTemplate = function(htmlTemplate, options) {
	var syntax = /(\{(\w+)\})/g; //matches symbols like '{id}'
	
	if (!options) {
		return htmlTemplate;
	}
	
	if (!Whirlwind.isString(htmlTemplate)) {
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


Whirlwind.isFunction = function(obj) {
	//console.log("testing is function %o", obj);
	if (!obj) {
		return false;
	}
	return $.isFunction(obj);
};

Whirlwind.isString= function(obj) {
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


Whirlwind.isNumber = function(obj) {
	return typeof(obj) == 'number';
};

Whirlwind.isTrue = function(obj) {
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

Whirlwind.isArray = function(obj) {
	if (!obj) {
		return false;
	}
	return $.isArray(obj); 
};

/**
 * Parses an iso date.
 * 
 * works with most (all?) iso format variations
 * 2011-04-25T20:59:59.999-07:00
 * 2011-04-25T20:59:59+07:00
 * 2011-04-25T20:59:59Z
 * 
 */
Whirlwind.parseISODate = function(string) {
//	http://webcloud.se/log/JavaScript-and-ISO-8601/
	//Fixed the incorrect escaping from the original blog post.
    var regexp = "([0-9]{4})(\\-([0-9]{2})(\\-([0-9]{2})" +
	    "(T([0-9]{2}):([0-9]{2})(\\:([0-9]{2})(\\.([0-9]+))?)?" +
	    "(Z|(([\\-\\+])([0-9]{2})\\:?([0-9]{2})))?)?)?)?";
	var d = string.match(new RegExp(regexp));
	if (d == null || d.length == 0) {
		return null;
	}
	var offset = 0;
	var date = new Date(d[1], 0, 1);
	
	if (d[3]) { date.setMonth(d[3] - 1); }
	if (d[5]) { date.setDate(d[5]); }
	if (d[7]) { date.setHours(d[7]); }
	if (d[8]) { date.setMinutes(d[8]); }
	if (d[10]) { date.setSeconds(d[10]); }
	
	if (d[12]) { date.setMilliseconds(Number("0." + d[12]) * 1000); }
	
	if (d[14]) {
	    offset = (Number(d[16]) * 60) + Number(d[17]);
	    console.log(offset);
	    offset *= ((d[15] == '-') ? 1 : -1);
	}
	
	offset -= date.getTimezoneOffset();
	time = (Number(date) + (offset * 60 * 1000));
	return new Date(Number(time));
}


/**
 * Will convert passed in element to a date (when possible)
 * 
 * this requires the date.js to work.
 * will successfully parse iso dates of all styles. 
 * 
 */
Whirlwind.toDate = function(date) {
	if (!date) {
		return null;
	} 
	if (date instanceof Date) {
		return date;
	}
	
	//ISO date from above
	var d = Whirlwind.parseISODate(date);
	if (d) {
		return d;
	}
	return new Date(date *1000);
};


/**
 * Serializes the passed in element into an object.
 * uses all input elements below the passed in element.
 * 
 * 
 */
Whirlwind.serialize = function(element) {
	var params = {};
	$(element).find(':input').each(function(i) {
		if (!($(this).data('iptrMsgDisplayed')) &&
			this.name && !this.disabled &&
				(this.checked || /select|textarea/i.test(this.nodeName) ||
					/text|hidden|password/i.test(this.type))) {
			if (params[this.name]) {
				if (!Whirlwind.isArray(params[this.name])) {
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
Whirlwind.value = function(elem, value) {
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
Whirlwind.trim = function(str, trim) {
	if (!str) {
		return str;
	}
	if (!trim) {
		return jQuery.trim(str);
	}
	var tmp = str;
	while(Whirlwind.stringStartsWith(tmp, trim)) {
		tmp = tmp.slice(trim.length);
	}
	while(Whirlwind.stringEndsWith(tmp, trim)) {
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
Whirlwind.href = function(options) {
	if (Whirlwind.isString(options)) {
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
 
Whirlwind.isVisible = function(element) {
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
	
	var measure = Whirlwind.measure(elem);
	
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
Whirlwind.formatNumber = function(number) {
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