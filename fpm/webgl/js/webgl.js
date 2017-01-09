function webglDetect() {
    // return supported, enabled, contex list
    if (!!window.WebGLRenderingContext) {
        var canvas = document.createElement("canvas");
        var names = ["webgl", "experimental-webgl", "moz-webgl"];
        supported = [];
        for(var i in names) {
            try {
                var gl = canvas.getContext(names[i]);
                if (gl && typeof gl.getParameter == "function") {
                    supported.push(names[i]);
                }
            } catch(e) {}
        }
        if (supported.length >= 1)
            return [true, true, supported];

        return [true, false, []];
    }
    return [false, false, []];
}

function runWebgl() {
    var wgld = webglDetect();
    var supported = wgld[0];
    var enabled = wgld[1];
    var ctxs = wgld[2];

    var webglres = {};
    webglres["supported"] = supported;
    webglres["enabled"] = enabled;

    if (supported && enabled && ctxs.length >= 1) {
        webglres["ctx_names"] = ctxs.join(', ');
        var ctx_name = ctxs[0];
        if (ctx_name) {
            var gl = document.createElement("canvas").getContext(ctx_name);
            webglres["ver"] = gl.getParameter(gl.VERSION);
            webglres["shader_ver"] = gl.getParameter(gl.SHADING_LANGUAGE_VERSION);
            webglres["vendor"] = gl.getParameter(gl.VENDOR);
            webglres["renderer"] = gl.getParameter(gl.RENDERER);

            // extensions
            var ext = gl.getSupportedExtensions();
            if (ext) {
                webglres["extensions"] = ext.join(', ');
            }

            var dbgrnd = gl.getExtension('WEBGL_debug_renderer_info');
            if (dbgrnd != null)
            {
                webglres["vendor_real"] = gl.getParameter(dbgrnd.UNMASKED_VENDOR_WEBGL);
                webglres["renderer_real"] = gl.getParameter(dbgrnd.UNMASKED_RENDERER_WEBGL);
            }

            // max anisotropy:
            var max, e = gl.getExtension("EXT_texture_filter_anisotropic")
                || gl.getExtension("WEBKIT_EXT_texture_filter_anisotropic")
                || gl.getExtension("MOZ_EXT_texture_filter_anisotropic");
            if (e) {
                max = gl.getParameter(e.MAX_TEXTURE_MAX_ANISOTROPY_EXT);
                if (max === 0) max = 2;
                webglres["max_anisotropy"] = max;
            }
        }
    }
    return webglres;
}
