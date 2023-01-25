#
# Conditional build:
%bcond_without	doc	# Sphinx documentation
%bcond_without	tests	# unit tests

%define		cryptography_ver	2.5.0
%define		josepy_ver		1.13.0
%define		pyopenssl_ver		17.3.0
%define		requests_ver		2.20.0
%define		requests_toolbelt_ver	0.3.0
%define		six_ver			1.9.0

%define		module  acme
Summary:	Python library for the ACME protocol
Summary(pl.UTF-8):	Biblioteka Pythona do protokołu ACME
Name:		python3-%{module}
Version:	1.27.0
Release:	1
License:	Apache v2.0
Group:		Libraries/Python
#Source0Download: https://pypi.org/simple/acme/
Source0:	https://files.pythonhosted.org/packages/source/a/acme/%{module}-%{version}.tar.gz
# Source0-md5:	3d950fd6465f8e85800a62eb7e76be19
URL:		https://pypi.org/project/acme/
BuildRequires:	python3-devel >= 1:3.7
BuildRequires:	python3-setuptools >= 1:41.6
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
%if %{with doc} || %{with tests}
BuildRequires:	python3-cryptography >= %{cryptography_ver}
BuildRequires:	python3-josepy >= %{josepy_ver}
BuildRequires:	python3-pyOpenSSL >= %{pyopenssl_ver}
BuildRequires:	python3-pyrfc3339
BuildRequires:	python3-pytz >= 2019.3
BuildRequires:	python3-requests >= %{requests_ver}
BuildRequires:	python3-requests-toolbelt >= %{requests_toolbelt_ver}
%endif
%if %{with tests}
BuildRequires:	python3-pytest
%endif
%if %{with doc}
BuildRequires:	python3-sphinx_rtd_theme
BuildRequires:	sphinx-pdg-3 >= 1.0
%endif
Requires:	python3-cryptography >= %{cryptography_ver}
Requires:	python3-pyOpenSSL >= %{pyopenssl_ver}
Requires:	python3-pyasn1
Requires:	python3-pyrfc3339
Requires:	python3-pytz
Requires:	python3-requests >= %{requests_ver}
Requires:	python3-requests-toolbelt >= %{requests_toolbelt_ver}
Requires:	python3-six >= %{six_ver}
Suggests:	python3-acme-doc
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Python library for use of the Automatic Certificate Management
Environment protocol as defined by the IETF. It's used by the Let's
Encrypt project.

%description -l pl.UTF-8
Biblioteka Pythona do korzystania z protokołu Automatic Certificate
Management Environment (środowiska automatycznego zarządzania
certyfikatami) zdefiniowanego przez IETF. Jest używana przez projekt
Let's Encrypt.

%package doc
Summary:	Documentation for python-acme library
Summary(pl.UTF-8):	Dokumentacja do biblioteki python-acme
Group:		Documentation

%description doc
Documentation for the ACME Python library.

%description doc -l pl.UTF-8
Dokumentacja do biblioteki Pythona ACME.

%prep
%setup -q -n %{module}-%{version}

%build
%py3_build

%if %{with tests}
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
PYTHONPATH=$(pwd) \
%{__python3} -m pytest tests
%endif

%if %{with doc}
%{__make} -C docs html \
	SPHINXBUILD=sphinx-build-3
%endif

%install
rm -rf $RPM_BUILD_ROOT

%py3_install

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README.rst
%{py3_sitescriptdir}/%{module}
%{py3_sitescriptdir}/%{module}-%{version}-py*.egg-info

%if %{with doc}
%files doc
%defattr(644,root,root,755)
%doc docs/_build/html/{_modules,_static,api,man,*.html,*.js}
%endif