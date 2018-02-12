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
    var distroSpec = ''
    if (distro) {
      distroSpec = '/' + distro
      if (release) {
        distroSpec += '/' + release
      }
    }

    var url
    switch (target || 'index') {
      case 'index':
        url = distroSpec ? '/index' + distroSpec + '/' : '/'
        break
      case 'nuvola':
        url = '/nuvola' + distroSpec + '/'
        break
      default:
        url = '/app/' + target + distroSpec + '/'
        break
    }
    window.location.href = url
  }

  checkHash()

  var PLATFORM_X64 = ['x86_64', 'x86-64']
  var USER_AGENT_X64 = [
    'x86_64', 'x86-64', 'Win64', 'x64;', 'amd64', 'AMD64', 'WOW64', 'x64_64'
  ]

  var isPlatformAmd64 = function () {
    var ua = navigator.userAgent
    var oscpu = window.navigator.oscpu || ''
    var platform = window.navigator.platform || ''
    for (var i = 0; i < PLATFORM_X64.length; i++) {
      var test = PLATFORM_X64[i]
      if (platform.indexOf(test) !== -1 || oscpu.indexOf(test) !== -1) {
        return true
      }
    }
    for (i = 0; i < USER_AGENT_X64.length; i++) {
      if (ua.indexOf(USER_AGENT_X64[i]) !== -1) {
        return true
      }
    }
    return false
  }
  var notAmd64 = !isPlatformAmd64()
  var elms = window.document.querySelectorAll('.not-amd64')
  for (var i = 0; i < elms.length; i++) {
    elms[i].style.display = notAmd64 ? 'block' : 'none'
  }

  var setupGalleries = function (galleries) {
    if (galleries) {
      for (var i = 0; i < galleries.length; i++) {
        var gallery = galleries[i]
        var images = gallery.querySelectorAll('img')
        if (images) {
          for (var j = 0; j < images.length; j++) {
            attachGallery(i, images, j)
          }
        }
      }
    }
  }

  var attachGallery = function (galleryNumber, images, imageNumber) {
    var image = images[imageNumber]
    var link = image.parentNode
    link.title = link.title || image.title || image.alt
    link.onclick = function (event) {
      showGalleryImage(event, galleryNumber, images, imageNumber)
      return false
    }
  }

  var mktext = document.createTextNode.bind(document)
  var mkelm = function (name, attributes, children) {
    var elm = document.createElement(name)
    attributes = attributes || {}
    for (var key in attributes) {
      elm.setAttribute(key, attributes[key])
    }
    children = children || []
    for (var i = 0; i < children.length; i++) {
      var child = children[i]
      elm.appendChild((typeof child === 'string') ? mktext(child) : child)
    }
    return elm
  }

  var showGalleryImage = function (event, galleryNumber, images, imageNumber) {
    var image = images[imageNumber]
    var galleryLightbox = document.getElementById('gallery-lightbox')
    if (galleryLightbox) {
      if (galleryLightbox.getAttribute('data-gallery-number') !== '' + galleryNumber) {
        galleryLightbox.parentNode.removeChild(galleryLightbox)
        galleryLightbox = null
      }
    }
    if (!galleryLightbox) {
      var img = mkelm('img', {alt: ' ', 'class': 'lightbox-img'})
      var position = mkelm('span', {'class': 'lightbox-position'})
      var prev = mkelm('span', {'class': 'lightbox-prev'}, ['<'])
      prev.onclick = galleryGoPrev(images)
      var next = mkelm('span', {'class': 'lightbox-next'}, ['>'])
      next.onclick = galleryGoNext(images)
      var caption = mkelm('p', {'class': 'lightbox-caption'})
      var close = mkelm('span', {'class': 'lightbox-close'}, ['×'])
      var toolbar = mkelm('div', {'class': 'lightbox-toolbar'}, [prev, position, next, close])
      var content = mkelm('div', {'class': 'lightbox-content'}, [img])

      close.onclick = removeGalleryLightbox
      galleryLightbox = mkelm(
          'div', {id: 'gallery-lightbox', 'data-gallery-number': galleryNumber}, [toolbar, content, caption])
      document.body.appendChild(galleryLightbox)
    } else {
      img = galleryLightbox.querySelector('.lightbox-img')
      caption = galleryLightbox.querySelector('.lightbox-caption')
      position = galleryLightbox.querySelector('.lightbox-position')
    }

    img.src = image.parentNode.href
    img.alt = image.alt
    img.title = image.title || image.alt
    caption.textContent = image.alt || image.title
    position.textContent = 'Image ' + (imageNumber + 1) + '/' + images.length
    galleryLightbox.setAttribute('data-gallery-image', imageNumber)
  }

  var removeGalleryLightbox = function () {
    var galleryLightbox = document.getElementById('gallery-lightbox')
    if (galleryLightbox) {
      galleryLightbox.parentNode.removeChild(galleryLightbox)
    }
  }

  var galleryGoPrev = function (images) {
    return function (event) { galleryGo(event, images, -1) }
  }
  var galleryGoNext = function (images) {
    return function (event) { galleryGo(event, images, 1) }
  }

  var galleryGo = function (event, images, step) {
    var gallery = document.getElementById('gallery-lightbox')
    var galleryNumber = gallery.getAttribute('data-gallery-number') * 1
    var imageNumber = gallery.getAttribute('data-gallery-image') * 1 + step
    while (imageNumber < 0) {
      imageNumber += images.length
    }
    while (imageNumber >= images.length) {
      imageNumber -= images.length
    }
    showGalleryImage(event, galleryNumber, images, imageNumber)
  }

  setupGalleries(document.querySelectorAll('.gallery'))
})(window)
