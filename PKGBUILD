# Maintainer: <saswata>

pkgname=kayos-assistant
_licensedir="/usr/share/kayos/licenses/"
_policydir="usr/share/polkit-1/actions/"
pkgver=1.0
pkgrel=1
pkgdesc="Assistant application for KayOS"
arch=('x86_64')
url="https://github.com/test9846161946519816/$pkgname"
license=('GPL3')
depends=('w3m' 'python-numpy' 'python-psutil' 'chaotic-mirrorlist' 'chaotic-keyring')
makedepends=('git')
options=(!strip !emptydirs)
conflicts=('kayos-assistant')
source=("$pkgname-$pkgver::git+$url")
sha256sums=('SKIP')

package() {
	install -dm755 ${pkgdir}${_licensedir}${pkgname}
	install -m644  ${srcdir}/${pkgname}-${pkgver}/LICENSE ${pkgdir}${_licensedir}${pkgname}
	
	install -dm755 ${pkgdir}${_policydir}
	install -m644  ${srcdir}/${pkgname}-${pkgver}/usr/share/polkit-1/actions/org.kayos.assistant.policy ${pkgdir}${_policydir}

	cp -r "$srcdir/$pkgname-$pkgver/usr" "$pkgdir"
}
