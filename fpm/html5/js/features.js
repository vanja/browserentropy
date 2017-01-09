var smartCopy = function(sourceObj, excludedProps) {
  var setVal = function(val) {
    if (val == false)
      return 0;
    else if (val == true)
      return 1;
    else if (val == 'probably')
      return 2;
    else if (val == 'maybe')
      return 3;
    else
      return 4;
  }

  // could also use following polyfill:
  // https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Object/keys#Polyfill
  if (!Object.keys) {
    Object.keys = function(obj) {
      var keys = [];
      for (var i in obj) {
        if (obj.hasOwnProperty(i)) {
          keys.push(i);
        }
      }
      return keys;
    };
  }

  var keys = Object.keys(sourceObj).sort();
  var newObj = Object();
  for (var k in keys) {
    if (String(keys[k]).substring(0, 1) == '_' || $.inArray(keys[k], excludedProps) > -1)
      continue;
    var attr = sourceObj[keys[k]];
    if (typeof attr === "object" && typeof attr.valueOf() === "boolean") {
      newObj[keys[k]] = setVal(attr.valueOf());
      for (var l in attr) {
        newObj[keys[k] + '__' + l] = setVal(attr[l]);
      }
    } else if (typeof attr === "object" && typeof attr.valueOf() === "object") {
      for (var l in attr) {
        newObj[keys[k] + '__' + l] = setVal(attr[l]);
      }
    } else {
      newObj[keys[k]] = setVal(attr.valueOf());
    }
  }
  return newObj;
}

function detectFeatures() {
  return smartCopy(Modernizr, ['atobbtoa', 'cookies', 'canvaswinding', 'display-runin',
    'flash', 'forcetouch', 'matchmedia', 'webgl', 'webglextensions', 'webpanimation',
    'webpalpha', 'webplossless', 'webp-lossless', 'xhrresponsetypearraybuffer',
    'xhrresponsetypeblob', 'xhrresponsetypedocument', 'xhrresponsetypejson',
    'xhrresponsetypetext', 'xhrresponsetype']);
};
