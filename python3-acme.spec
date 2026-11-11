#
# Conditional build:
%bcond_without	doc	# Sphinx documentation
%bcond_without	tests	# unit tests

%define		module  acme
Summary:	Python library for the ACME protocol
Summary(pl.UTF-8):	Biblioteka Pythona do protokołu ACME
Name:		python3-%{module}
Version:	5.10.0
Release:	1
License:	Apache v2.0
Group:		Libraries/Python
#Source0Download: https://pypi.org/simple/acme/
Source0:	https://files.pythonhosted.org/packages/source/a/acme/%{module}-%{version}.tar.gz
# Source0-md5:	2d6b62c55214edf6dd3f7be030a1e1b6
URL:		https://pypi.org/project/acme/
BuildRequires:	python3-build
BuildRequires:	python3-installer
BuildRequires:	python3-modules >= 1:3.10
BuildRequires:	python3-setuptools >= 1:61
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 2.044
%if %{with doc} || %{with tests}
BuildRequires:	python3-cryptography >= 47.0.0
BuildRequires:	python3-josepy >= 2.0.0
BuildRequires:	python3-pyOpenSSL >= 25.0
BuildRequires:	python3-pyrfc3339
BuildRequires:	python3-requests >= 2.25.1
%endif
%if %{with tests}
BuildRequires:	python3-pytest
%endif
%if %{with doc}
BuildRequires:	python3-sphinx_rtd_theme
BuildRequires:	sphinx-pdg-3 >= 1.0
%endif
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
%py3_build_pyproject

%if %{with tests}
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
PYTHONPATH=$(pwd)/src \
%{__python3} -m pytest src/acme
%endif

%if %{with doc}
%{__python3} -m zipfile -e build-3/*.whl build-3-doc
PYTHONPATH=$(pwd)/build-3-doc \
%{__make} -C docs html \
	SPHINXBUILD=sphinx-build-3
%endif

%install
rm -rf $RPM_BUILD_ROOT

%py3_install_pyproject

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README.rst
%{py3_sitescriptdir}/%{module}
%{py3_sitescriptdir}/%{module}-%{version}.dist-info

%if %{with doc}
%files doc
%defattr(644,root,root,755)
%doc docs/_build/html/{_modules,_static,api,man,*.html,*.js}
%endif
