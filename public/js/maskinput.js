/**
 * MODO DE USAR EM: https://igorescobar.github.io/jQuery-Mask-Plugin/docs.html
 * 
 * jquery.mask.js
 * @version: v1.14.11
 * @author: Igor Escobar
 *
 * Created by Igor Escobar on 2012-03-10. Please report any bug at http://blog.igorescobar.com
 *
 * Copyright (c) 2012 Igor Escobar http://blog.igorescobar.com
 *
 * The MIT License (http://www.opensource.org/licenses/mit-license.php)
 *
 * Permission is hereby granted, free of charge, to any person
 * obtaining a copy of this software and associated documentation
 * files (the "Software"), to deal in the Software without
 * restriction, including without limitation the rights to use,
 * copy, modify, merge, publish, distribute, sublicense, and/or sell
 * copies of the Software, and to permit persons to whom the
 * Software is furnished to do so, subject to the following
 * conditions:
 *
 * The above copyright notice and this permission notice shall be
 * included in all copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
 * EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
 * OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
 * NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
 * HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
 * WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
 * FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
 * OTHER DEALINGS IN THE SOFTWARE.
 */

/* jshint laxbreak: true */
/* jshint maxcomplexity:17 */
/* global define */

'use strict';

// UMD (Universal Module Definition) patterns for JavaScript modules that work everywhere.
// https://github.com/umdjs/umd/blob/master/jqueryPluginCommonjs.js

(function(e,x,C){"function"===typeof define&&define.amd?define(["jquery"],e):"object"===typeof exports?module.exports=e(require("jquery")):e(x||C)})(function(e){var x=function(a,g,h){var b={invalid:[],getCaret:function(){try{var c=0,f=a.get(0),d=document.selection,m=f.selectionStart;if(d&&-1===navigator.appVersion.indexOf("MSIE 10")){var k=d.createRange();k.moveStart("character",-b.val().length);c=k.text.length}else if(m||"0"===m)c=m;return c}catch(p){}},setCaret:function(c){try{if(a.is(":focus")){var f=
a.get(0);if(f.setSelectionRange)f.setSelectionRange(c,c);else{var d=f.createTextRange();d.collapse(!0);d.moveEnd("character",c);d.moveStart("character",c);d.select()}}}catch(m){}},events:function(){a.on("keydown.mask",function(c){a.data("mask-keycode",c.keyCode||c.which);a.data("mask-previus-value",a.val());a.data("mask-previus-caret-pos",b.getCaret());b.maskDigitPosMapOld=b.maskDigitPosMap}).on(e.jMaskGlobals.useInput?"input.mask":"keyup.mask",b.behaviour).on("paste.mask drop.mask",function(){setTimeout(function(){a.keydown().keyup()},
100)}).on("change.mask",function(){a.data("changed",!0)}).on("blur.mask",function(){t===b.val()||a.data("changed")||a.trigger("change");a.data("changed",!1)}).on("blur.mask",function(){t=b.val()}).on("focus.mask",function(c){!0===h.selectOnFocus&&e(c.target).select()}).on("focusout.mask",function(){h.clearIfNotMatch&&!G.test(b.val())&&b.val("")})},getRegexMask:function(){for(var c=[],f,d,m,k,p=0;p<g.length;p++)(f=n.translation[g.charAt(p)])?(d=f.pattern.toString().replace(/.{1}$|^.{1}/g,""),m=f.optional,
(f=f.recursive)?(c.push(g.charAt(p)),k={digit:g.charAt(p),pattern:d}):c.push(m||f?d+"?":d)):c.push(g.charAt(p).replace(/[-\/\\^$*+?.()|[\]{}]/g,"\\$&"));c=c.join("");k&&(c=c.replace(new RegExp("("+k.digit+"(.*"+k.digit+")?)"),"($1)?").replace(new RegExp(k.digit,"g"),k.pattern));return new RegExp(c)},destroyEvents:function(){a.off("input keydown keyup paste drop blur focusout ".split(" ").join(".mask "))},val:function(c){var f=a.is("input")?"val":"text";if(0<arguments.length){if(a[f]()!==c)a[f](c);
f=a}else f=a[f]();return f},calculateCaretPosition:function(){var c=a.data("mask-previus-value")||"",f=b.getMasked(),d=b.getCaret();if(c!==f){var m=a.data("mask-previus-caret-pos")||0;f=f.length;var k=c.length,p=c=0,q=0,r=0,l;for(l=d;l<f&&b.maskDigitPosMap[l];l++)p++;for(l=d-1;0<=l&&b.maskDigitPosMap[l];l--)c++;for(l=d-1;0<=l;l--)b.maskDigitPosMap[l]&&q++;for(l=m-1;0<=l;l--)b.maskDigitPosMapOld[l]&&r++;d>k?d=f:m>=d&&m!==k?b.maskDigitPosMapOld[d]||(m=d,d=d-(r-q)-c,b.maskDigitPosMap[d]&&(d=m)):d>m&&
(d=d+(q-r)+p)}return d},behaviour:function(c){c=c||window.event;b.invalid=[];var f=a.data("mask-keycode");if(-1===e.inArray(f,n.byPassKeys)){f=b.getMasked();var d=b.getCaret();setTimeout(function(){b.setCaret(b.calculateCaretPosition())},10);b.val(f);b.setCaret(d);return b.callbacks(c)}},getMasked:function(c,f){var d=[],m=void 0===f?b.val():f+"",k=0,p=g.length,q=0,r=m.length,l=1,y="push",z=-1,D=0,E=[];if(h.reverse){y="unshift";l=-1;var A=0;k=p-1;q=r-1;var H=function(){return-1<k&&-1<q}}else A=p-1,
H=function(){return k<p&&q<r};for(var F;H();){var B=g.charAt(k),w=m.charAt(q),u=n.translation[B];if(u)w.match(u.pattern)?(d[y](w),u.recursive&&(-1===z?z=k:k===A&&(k=z-l),A===z&&(k-=l)),k+=l):w===F?(D--,F=void 0):u.optional?(k+=l,q-=l):u.fallback?(d[y](u.fallback),k+=l,q-=l):b.invalid.push({p:q,v:w,e:u.pattern}),q+=l;else{if(!c)d[y](B);w===B?(E.push(q),q+=l):(F=B,E.push(q+D),D++);k+=l}}m=g.charAt(A);p!==r+1||n.translation[m]||d.push(m);d=d.join("");b.mapMaskdigitPositions(d,E,r);return d},mapMaskdigitPositions:function(c,
f,d){c=h.reverse?c.length-d:0;b.maskDigitPosMap={};for(d=0;d<f.length;d++)b.maskDigitPosMap[f[d]+c]=1},callbacks:function(c){var f=b.val(),d=f!==t,m=[f,c,a,h],k=function(p,q,r){"function"===typeof h[p]&&q&&h[p].apply(this,r)};k("onChange",!0===d,m);k("onKeyPress",!0===d,m);k("onComplete",f.length===g.length,m);k("onInvalid",0<b.invalid.length,[f,c,a,b.invalid,h])}};a=e(a);var n=this,t=b.val(),G;g="function"===typeof g?g(b.val(),void 0,a,h):g;n.mask=g;n.options=h;n.remove=function(){var c=b.getCaret();
b.destroyEvents();b.val(n.getCleanVal());b.setCaret(c);return a};n.getCleanVal=function(){return b.getMasked(!0)};n.getMaskedVal=function(c){return b.getMasked(!1,c)};n.init=function(c){c=c||!1;h=h||{};n.clearIfNotMatch=e.jMaskGlobals.clearIfNotMatch;n.byPassKeys=e.jMaskGlobals.byPassKeys;n.translation=e.extend({},e.jMaskGlobals.translation,h.translation);n=e.extend(!0,{},n,h);G=b.getRegexMask();if(c)b.events(),b.val(b.getMasked());else{h.placeholder&&a.attr("placeholder",h.placeholder);a.data("mask")&&
a.attr("autocomplete","off");c=0;for(var f=!0;c<g.length;c++){var d=n.translation[g.charAt(c)];if(d&&d.recursive){f=!1;break}}f&&a.attr("maxlength",g.length);b.destroyEvents();b.events();c=b.getCaret();b.val(b.getMasked());b.setCaret(c)}};n.init(!a.is("input"))};e.maskWatchers={};var C=function(){var a=e(this),g={},h=a.attr("data-mask");a.attr("data-mask-reverse")&&(g.reverse=!0);a.attr("data-mask-clearifnotmatch")&&(g.clearIfNotMatch=!0);"true"===a.attr("data-mask-selectonfocus")&&(g.selectOnFocus=
!0);if(I(a,h,g))return a.data("mask",new x(this,h,g))},I=function(a,g,h){h=h||{};var b=e(a).data("mask"),n=JSON.stringify;a=e(a).val()||e(a).text();try{return"function"===typeof g&&(g=g(a)),"object"!==typeof b||n(b.options)!==n(h)||b.mask!==g}catch(t){}},v=function(a){var g=document.createElement("div");a="on"+a;var h=a in g;h||(g.setAttribute(a,"return;"),h="function"===typeof g[a]);return h};e.fn.mask=function(a,g){g=g||{};var h=this.selector,b=e.jMaskGlobals,n=b.watchInterval;b=g.watchInputs||
b.watchInputs;var t=function(){if(I(this,a,g))return e(this).data("mask",new x(this,a,g))};e(this).each(t);h&&""!==h&&b&&(clearInterval(e.maskWatchers[h]),e.maskWatchers[h]=setInterval(function(){e(document).find(h).each(t)},n));return this};e.fn.masked=function(a){return this.data("mask").getMaskedVal(a)};e.fn.unmask=function(){clearInterval(e.maskWatchers[this.selector]);delete e.maskWatchers[this.selector];return this.each(function(){var a=e(this).data("mask");a&&a.remove().removeData("mask")})};
e.fn.cleanVal=function(){return this.data("mask").getCleanVal()};e.applyDataMask=function(a){a=a||e.jMaskGlobals.maskElements;(a instanceof e?a:e(a)).filter(e.jMaskGlobals.dataMaskAttr).each(C)};v={maskElements:"input,td,span,div",dataMaskAttr:"*[data-mask]",dataMask:!0,watchInterval:300,watchInputs:!0,useInput:!/Chrome\/[2-4][0-9]|SamsungBrowser/.test(window.navigator.userAgent)&&v("input"),watchDataMask:!1,byPassKeys:[9,16,17,18,36,37,38,39,40,91],translation:{0:{pattern:/\d/},9:{pattern:/\d/,optional:!0},
"#":{pattern:/\d/,recursive:!0},A:{pattern:/[a-zA-Z0-9]/},S:{pattern:/[a-zA-Z]/}}};e.jMaskGlobals=e.jMaskGlobals||{};v=e.jMaskGlobals=e.extend(!0,{},v,e.jMaskGlobals);v.dataMask&&e.applyDataMask();setInterval(function(){e.jMaskGlobals.watchDataMask&&e.applyDataMask()},v.watchInterval)},window.jQuery,window.Zepto);