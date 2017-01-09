function fpjs2r_get(k) {
  function filterByKey(k) {return function(el) {return 'key' in el && el.key === k;}}
  try {return $.grep(fpjs2r, function(el) {return 'key' in el && el.key === k;})[0].value;} catch (e) {return '';}
}

var fpjs2r = Object();
function navfp() {
  var options = {
      excludeAdBlock: true,
      excludeUserAgent: true,
      excludeSessionStorage: true,
      excludeIndexedDB: true,
      excludeCanvas: true,
      excludeWebGL: true,
      excludeTouchSupport: true,
      excludeJsFonts: true,
      excludeFlashFonts: true
    };

  new Fingerprint2(options).get(function(result, components){
    fpjs2r = components;
  });

  var r = Object();
  r['platform'] = fpjs2r_get('navigator_platform');
  r['lang'] = fpjs2r_get('language');
  if (fpjs2r_get('has_lied_languages')) r['lang'] += '*';
  r['video'] = fpjs2r_get('resolution').toString().replace(',', 'x');
  r['video'] += 'x' + fpjs2r_get('color_depth');
  if (fpjs2r_get('has_lied_resolution')) r['video'] += '*';
  r['tz'] = fpjs2r_get('timezone_offset');
  r['dnt'] = fpjs2r_get('do_not_track');
  r['adblock'] = document.getElementById("ads") ? false : true;

  var plg = [];
  var rp = fpjs2r_get('regular_plugins');
  if (rp) plg = rp;
  var iep = fpjs2r_get('ie_plugins');
  if (iep) plg = $.grep(iep, function(o) {return o !== null;});
  r['plugins'] = plg.join('|||\r\n');

  var jf = fpjs2r_get('js_fonts');
  if (jf) r['fonts'] = jf + ' (via JavaScript)';
  var ff = fpjs2r_get('swf');
  if (ff) r['fonts'] = ff + ' (via Flash)';
  if (r['fonts']) r['fonts'] = r['fonts'].toString().replace(/,/g, ', ');

  r['cookies'] = Modernizr.cookies;
  r['flash'] = Modernizr.flash.blocked ? 'Blocked' : (Modernizr.flash ? 'True' : 'False');

  return r;
}