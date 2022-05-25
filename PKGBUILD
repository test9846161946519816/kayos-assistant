# Maintainer: <saswata>

pkgname=kayos-assistant
pkgver=1.0
pkgrel=1
pkgdesc="Assistant application for KayOS"
arch=('x86_64')
url="https://github.com/test9846161946519816/$pkgname"
depends=('w3m' 'python-numpy' 'python-psutil' 'chaotic-mirrorlist' 'chaotic-keyring')
makedepends=('git')
conflicts=('kayos-assistant')
source=("$pkgname-$pkgver.tar.gz::git+$url")
sha256sums=('SKIP')

package() {
	cd "$srcdir"
	cp -r "$pkgname-$pkgver/usr" "$pkgdir"
}
