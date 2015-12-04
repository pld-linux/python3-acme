#
# Conditional build:
%bcond_without	doc	# don't build doc
%bcond_without	tests	# do not perform "make test"
%bcond_without	python2 # CPython 2.x module
%bcond_without	python3 # CPython 3.x module

%define		module  acme
Summary:	Python library for the ACME protocol
Name:		python-%{module}
Version:	0.1.0
Release:	1
License:	Apache v2.0
Group:		Libraries/Python
Source0:	https://pypi.python.org/packages/source/a/%{module}/%{module}-%{version}.tar.gz
# Source0-md5:	7115ba77709b281ffaa59d853cd5337a
URL:		https://pypi.python.org/pypi/acme
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.713
%if %{with python2}
BuildRequires:	python-cryptography
BuildRequires:	python-devel
BuildRequires:	python-pyOpenSSL
BuildRequires:	python-pyrfc3339
BuildRequires:	python-requests
BuildRequires:	python-werkzeug
BuildRequires:	sphinx-pdg
%if %{with tests}
BuildRequires:	python-ndg_httpsclient
BuildRequires:	python-nose
BuildRequires:	python-tox
%endif
%endif
%if %{with python3}
BuildRequires:	python3-cryptography
BuildRequires:	python3-devel
BuildRequires:	python3-pyOpenSSL
BuildRequires:	python3-pyrfc3339
BuildRequires:	python3-requests
BuildRequires:	python3-werkzeug
%if %{with tests}
BuildRequires:	python3-ndg_httpsclient
BuildRequires:	python3-nose
BuildRequires:	python3-tox
%endif
%endif
%if %{with doc}
BuildRequires:	python-sphinxcontrib-programoutput
%endif
Requires:	python-cryptography
Requires:	python-ndg_httpsclient
Requires:	python-pyOpenSSL
Requires:	python-pyasn1
Requires:	python-pyrfc3339
Requires:	python-pytz
Requires:	python-requests
Requires:	python-six
Requires:	python-werkzeug
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
Requires:	python3-cryptography
Requires:	python3-ndg_httpsclient
Requires:	python3-pyOpenSSL
Requires:	python3-pyasn1
Requires:	python3-pyrfc3339
Requires:	python3-pytz
Requires:	python3-requests
Requires:	python3-six
Requires:	python3-werkzeug
Suggests:	python-acme-doc

%description -n python3-acme
Python 3 library for use of the Automatic Certificate Management
Environment protocol as defined by the IETF. It's used by the Let's
Encrypt project.

%package doc
Summary:	Documentation for python-acme libraries
Requires:	fontawesome-fonts
Requires:	fontawesome-fonts-web
Provides:	bundled(inconsolata-fonts)
Provides:	bundled(jquery)
Provides:	bundled(lato-fonts)
Provides:	bundled(robotoslab-fonts)
Provides:	bundled(underscore)

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
# build documentation
%{__python} setup.py install --user

# Clean up stuff we don't need for docs
rm -rf docs/_build/html/{.buildinfo,_sources}

# Unbundle fonts already on system
# Lato ttf is in texlive but that adds a lot of dependencies (30+MB) for just a font in documentation
# and lato is not in it's own -fonts package, only texlive
rm -f docs/_build/html/_static/fonts/fontawesome*
ln -sf %{_datadir}/fonts/fontawesome/fontawesome-webfont.eot docs/_build/html/_static/fonts/fontawesome-webfont.eot
ln -sf %{_datadir}/fonts/fontawesome/fontawesome-webfont.svg docs/_build/html/_static/fonts/fontawesome-webfont.svg
ln -sf %{_datadir}/fonts/fontawesome/fontawesome-webfont.ttf docs/_build/html/_static/fonts/fontawesome-webfont.ttf
ln -sf %{_datadir}/fonts/fontawesome/fontawesome-webfont.woff docs/_build/html/_static/fonts/fontawesome-webfont.woff
%endif

%install
rm -rf $RPM_BUILD_ROOT
# Do python3 first so bin ends up from py2
%if %{with python3}
%py3_install
%endif

%if %{with python2}
%py_install
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%files
%defattr(644,root,root,755)
%doc README.rst LICENSE.txt
%{py_sitescriptdir}/%{module}
%{py_sitescriptdir}/%{module}-%{version}*.egg-info
%attr(755,root,root) %{_bindir}/jws
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
