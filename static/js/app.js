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
})(window)
