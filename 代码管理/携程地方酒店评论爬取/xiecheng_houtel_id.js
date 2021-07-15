function gencb(n) {
        var r = function() {
            for (var e = "qwertyuiopasdfg$hjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM", t = "", n = 0; n < 10; n++)
                t += e.charAt(~~(Math.random() * e.length));
            return encodeURIComponent(t)
        }();
        return window[r] = function(e) {
            delete window[r];
            var t = e()
              , e = "?";
            n.realUrl && 0 < n.realUrl.indexOf("?") && (e = "&"),
            n.realUrl += e + "testab=" + encodeURIComponent(t)
        }
        ,
        r
}