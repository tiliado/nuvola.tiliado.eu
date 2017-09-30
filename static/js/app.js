(function (window) {

  var parseHash = function (hash) {
    var parts = (hash || '').split('!')
    var result = {}
    result.app = parts[1] || null
    result.distro = parts[2] || null
    result.release = parts[3] || null
    return result
  }

  var checkHash = function () {
    var hash = parseHash(window.location.hash)
    var target = hash.app
    if (!target) {
      return
    }
    var distro = hash.distro
    var release = hash.release
    var distro_spec = ''
    if (distro) {
      distro_spec = '/' + distro
      if (release) {
        distro_spec += '/' + release
      }
    }

    var url;
    switch (target || 'index') {
      case 'index':
        url = distro_spec ? '/index' + distro_spec + '/' : '/'
        break
      case 'nuvola':
        url = '/nuvola' + distro_spec + '/'
        break
      default:
        url = '/app/' + target + distro_spec + '/'
        break
    }
    window.location.href = url
  }

  checkHash()
  var PLATFORM_X64 = ['x86_64', 'x86-64'];
  var USER_AGENT_X64 = [
    'x86_64', 'x86-64', 'Win64', 'x64;', 'amd64', 'AMD64', 'WOW64', 'x64_64'
  ]

  var isPlatformAmd64 = function () {
    var ua = navigator.userAgent;
    var oscpu = window.navigator.oscpu || "";
    var platform = window.navigator.platform || "";
    for (var i = 0; i < PLATFORM_X64.length; i++) {
      var test = PLATFORM_X64[i];
      if (platform.indexOf(test) !== -1 || oscpu.indexOf(test) !== -1) {
        return true;
      }
    }
    for (i = 0; i < USER_AGENT_X64.length; i++) {
      if (ua.indexOf(USER_AGENT_X64[i]) !== -1) {
        return true;
      }
    }
    return false;
  }
  var notAmd64 = !isPlatformAmd64();
  var elms = window.document.querySelectorAll('.not-amd64')
  for (var i = 0; i < elms.length; i++) {
    elms[i].style.display = notAmd64 ? "block" : "none"
  }
})(window)
