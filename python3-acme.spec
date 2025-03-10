#
# Conditional build:
%bcond_without	doc	# Sphinx documentation
%bcond_without	tests	# unit tests

%define		module  acme
Summary:	Python library for the ACME protocol
Summary(pl.UTF-8):	Biblioteka Pythona do protokołu ACME
Name:		python3-%{module}
Version:	1.32.0
Release:	2
License:	Apache v2.0
Group:		Libraries/Python
#Source0Download: https://pypi.org/simple/acme/
Source0:	https://files.pythonhosted.org/packages/source/a/acme/%{module}-%{version}.tar.gz
# Source0-md5:	ff30c912210078136dca039370aab100
URL:		https://pypi.org/project/acme/
BuildRequires:	python3-devel >= 1:3.7
BuildRequires:	python3-setuptools >= 1:41.6
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
%if %{with doc} || %{with tests}
BuildRequires:	python3-cryptography >= 2.5
BuildRequires:	python3-josepy >= 1.13
BuildRequires:	python3-pyOpenSSL >= 17.5
BuildRequires:	python3-pyrfc3339
BuildRequires:	python3-pytz >= 2019.3
BuildRequires:	python3-requests >= 2.20
BuildRequires:	python3-requests-toolbelt >= 0.3
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
