# Maintainer: Alexander Seiler <seileralex@gmail.com>

pkgname=kodi-addon-checker
pkgver=0.0.15
pkgrel=1
pkgdesc="Check kodi addons or whole kodi repositories for errors and best practices."
arch=('any')
url="https://pypi.org/project/${pkgname}"
license=('GPL3')
depends=('python' 'python-pillow' 'python-polib' 'python-requests' 'python-radon' 'python-urllib3' 'python-xmlschema')
makedepends=('python-setuptools')
source=("https://files.pythonhosted.org/packages/source/${pkgname::1}/${pkgname}/${pkgname}-${pkgver}.tar.gz")
sha256sums=('a73b80b901592de077aa3b88b8090b5066c2c46ebdc13e3fd7bb5a61af54b1a5')

prepare() {
	cd "$pkgname-$pkgver"
}

build() {
	cd "$pkgname-$pkgver"
	python setup.py build
}

check() {
	cd "$pkgname-$pkgver"
	python setup.py test
}

package() {
	cd "$pkgname-$pkgver"
	python setup.py install --root="$pkgdir/" --optimize=1 --skip-build
}
