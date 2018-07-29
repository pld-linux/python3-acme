#
# Conditional build:
%bcond_without	doc	# don't build doc
%bcond_with	tests	# do not perform "make test"
%bcond_without	python2 # CPython 2.x module
%bcond_without	python3 # CPython 3.x module

%define		cryptography_ver	0.8
%define		josepy_ver		1.0.0
%define		pyopenssl_ver		0.13
%define		requests_ver		2.4.1
%define		requests_toolbelt_ver	0.3.0
%define		six_ver			1.9.0

%define		module  acme
Summary:	Python library for the ACME protocol
Name:		python-%{module}
Version:	0.26.0
Release:	3
License:	Apache v2.0
Group:		Libraries/Python
Source0:	https://pypi.python.org/packages/source/a/%{module}/%{module}-%{version}.tar.gz
# Source0-md5:	a0f09ed7009d71b11c160e232d6f7aac
URL:		https://pypi.python.org/pypi/acme
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.713
%if %{with python2}
BuildRequires:	python-cryptography >= %{cryptography_ver}
BuildRequires:	python-devel
BuildRequires:	python-pyOpenSSL >= %{pyopenssl_ver}
BuildRequires:	python-pyrfc3339
BuildRequires:	python-requests >= %{requests_ver}
BuildRequires:	sphinx-pdg
%if %{with tests}
BuildRequires:	python-josepy >= %{josepy_ver}
BuildRequires:	python-mock
BuildRequires:	python-nose
BuildRequires:	python-requests-toolbelt >= %{requests_toolbelt_ver}
BuildRequires:	python-tox
%endif
%endif
%if %{with python3}
BuildRequires:	python3-cryptography >= %{cryptography_ver}
BuildRequires:	python3-devel
BuildRequires:	python3-pyOpenSSL >= %{pyopenssl_ver}
BuildRequires:	python3-pyrfc3339
BuildRequires:	python3-requests >= %{requests_ver}
%if %{with tests}
BuildRequires:	python3-josepy >= %{josepy_ver}
BuildRequires:	python3-mock
BuildRequires:	python3-nose
BuildRequires:	python3-requests-toolbelt >= %{requests_toolbelt_ver}
BuildRequires:	python3-tox
%endif
%endif
Requires:	python-cryptography >= %{cryptography_ver}
Requires:	python-pyOpenSSL >= %{pyopenssl_ver}
Requires:	python-pyasn1
Requires:	python-pyrfc3339
Requires:	python-pytz
Requires:	python-requests >= %{requests_ver}
Requires:	python-requests-toolbelt >= %{requests_toolbelt_ver}
Requires:	python-six >= %{six_ver}
Suggests:	python-acme-doc
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Python 2 library for use of the Automatic Certificate Management
Environment protocol as defined by the IETF. It's used by the Let's
Encrypt project.

%package -n python3-acme
Summary:	Python library for the ACME protocol
Group:		Libraries/Python
Requires:	python3-cryptography >= %{cryptography_ver}
Requires:	python3-josepy >= %{josepy_ver}
Requires:	python3-pyOpenSSL >= %{pyopenssl_ver}
Requires:	python3-pyasn1
Requires:	python3-pyrfc3339
Requires:	python3-pytz
Requires:	python3-requests >= %{requests_ver}
Requires:	python3-requests-toolbelt >= %{requests_toolbelt_ver}
Requires:	python3-six >= %{six_ver}
Suggests:	python-acme-doc

%description -n python3-acme
Python 3 library for use of the Automatic Certificate Management
Environment protocol as defined by the IETF. It's used by the Let's
Encrypt project.

%package doc
Summary:	Documentation for python-acme libraries
Group:		Documentation

%description doc
Documentation for the ACME python libraries

%prep
%setup -q -n %{module}-%{version}

%build
%if %{with python2}
%py_build %{?with_tests:test}
%endif

%if %{with python3}
%py3_build %{?with_tests:test}
%endif

%if %{with doc}
%{__make} -C docs html

# Clean up stuff we don't need for docs
rm -rf docs/_build/html/{.buildinfo,_sources}
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%py_install
%endif

%if %{with python3}
%py3_install
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%files
%defattr(644,root,root,755)
%doc README.rst LICENSE.txt
%{py_sitescriptdir}/%{module}
%{py_sitescriptdir}/%{module}-%{version}*.egg-info
%endif

%if %{with python3}
%files -n python3-acme
%defattr(644,root,root,755)
%doc README.rst LICENSE.txt
%{py3_sitescriptdir}/%{module}
%{py3_sitescriptdir}/%{module}-%{version}*.egg-info
%endif

%if %{with doc}
%files doc
%defattr(644,root,root,755)
%doc docs/_build/html/*
%endif
