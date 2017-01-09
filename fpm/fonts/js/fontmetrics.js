var CODEPOINTS = [0x20B9, 0x2581, 0x20BA, 0xA73D, 0xFFFD, 0x20B8, 0x05C6, 0x1E9E, 0x097F, 0xF003, 0x1CDA, 0x17DD, 0x23AE, 0x0D02, 0x0B82, 0x115A, 0x2425, 0x302E, 0xA830, 0x2B06, 0x21E4, 0x20BD, 0x2C7B, 0x20B0, 0xFBEE, 0xF810, 0xFFFF, 0x007F, 0x10A0, 0x1D790, 0x0700, 0x1950, 0x3095, 0x532D, 0x061C, 0x20E3, 0xFFF9, 0x0218, 0x058F, 0x08E4, 0x09B3, 0x1C50, 0x2619];

// Aggregate numbers by rolling them into something like a linear
// congruential RNG, with the given number in place of the increment.
function addsum(x, y) {
	return (x * 69069 + y) % 0x100000000;
}

// String.fromCharCode doesn't support code points outside the BMP (it
// treats them as mod 0x10000). String.fromCodePoint isn't supported.
// https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/String/fromCharCode
// https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/String/fromCodePoint
function stringFromCodePoint(n) {
	if (n <= 0xffff) {
		return String.fromCharCode(n);
	} else {
		n -= 0x10000;
		return String.fromCharCode(0xd800 + (n >> 10), 0xdc00 + (n % 0x400));
	}
}

var STYLES = ["default", "sans-serif", "serif", "monospace", "cursive", "fantasy", "standard", "unifont"];
// SYSTEM_STYLES uses system-installed fonts.
var SYSTEM_STYLES = ["default", "sans-serif", "serif", "monospace", "cursive", "fantasy"];
var DIVS = {};
var SPANS = {};
for (var i = 0; i < STYLES.length; i++) {
	var style = STYLES[i];
	DIVS[style] = document.getElementById("div-" + style);
	SPANS[style] = document.getElementById("span-" + style);
}

var CHECKSUM_SYSTEM = 0;
var CHECKSUM_STANDARD = 0;
var CHECKSUM_UNIFONT = 0;

// Measure the initial size of the fontloadboxes, so we can detect when the
// downloaded fonts are here.
var DOWNLOADED_FONT_FAMILIES = ["unifont", "linuxlibertine"];
var DOWNLOADED_FONT_INITIAL_WIDTHS = {};

// Wait for the fontloadboxes to change size, meaning that the web font has
// finished downloading. This trick doesn't work for Tor Browser, because of its
// "first web font" rule; the box changes to a blank (but larger) glyph when
// fontFamily is set, because the web font completely shadows the "fontload"
// font that follows it, even before it it loaded.
function download_webfonts() {
	for (var i = 0; i < DOWNLOADED_FONT_FAMILIES.length; i++) {
		var family = DOWNLOADED_FONT_FAMILIES[i];
		var loadbox = document.getElementById("fontload-" + family);
		DOWNLOADED_FONT_INITIAL_WIDTHS[family] = loadbox.offsetWidth;
		loadbox.style.fontFamily = family + ", fontload";
	}
	await_webfonts();
}

function await_webfonts() {
	var done = true;
	for (var i = 0; i < DOWNLOADED_FONT_FAMILIES.length; i++) {
		var family = DOWNLOADED_FONT_FAMILIES[i];
		var loadbox = document.getElementById("fontload-" + family);
		if (loadbox.offsetWidth === DOWNLOADED_FONT_INITIAL_WIDTHS[family]) {
			// Not yet.
			done = false;
		} else {
			loadbox.parentNode.style.border = "2px #222 solid";
		}
	}
	if (!done) {
		setTimeout(await_webfonts, 50);
		return;
	}
	document.getElementById("fontsloading").style.display = "none";
  	do_test();
}

function do_test() {
	var checksum = 0;
	for (var i = 0; i < CODEPOINTS.length; i++) {
		var n = CODEPOINTS[i];
		var c = stringFromCodePoint(n);
		for (var j = 0; j < STYLES.length; j++) {
			var style = STYLES[j];
			SPANS[style].textContent = c;
		}
		for (var j = 0; j < SYSTEM_STYLES.length; j++) {
			var style = SYSTEM_STYLES[j];
			CHECKSUM_SYSTEM = addsum(CHECKSUM_SYSTEM, SPANS[style].offsetWidth);
			CHECKSUM_SYSTEM = addsum(CHECKSUM_SYSTEM, DIVS[style].offsetHeight);
		}
		CHECKSUM_STANDARD = addsum(CHECKSUM_STANDARD, SPANS["standard"].offsetWidth);
		CHECKSUM_STANDARD = addsum(CHECKSUM_STANDARD, DIVS["standard"].offsetHeight);
		if (0 <= n && n < 0xFFFE) {
			CHECKSUM_UNIFONT = addsum(CHECKSUM_UNIFONT, SPANS["unifont"].offsetWidth);
			CHECKSUM_UNIFONT = addsum(CHECKSUM_UNIFONT, DIVS["unifont"].offsetHeight);
		}
	}
	for (var j = 0; j < STYLES.length; j++) {
		var style = STYLES[j];
		SPANS[style].textContent = "";
	}

	document.getElementById("content").style.display = "none";
}

// Wait some time before we start, otherwise Safari and Chrome on OS X appear
// not to load the fonts quickly enough.
setTimeout(download_webfonts, 500);
