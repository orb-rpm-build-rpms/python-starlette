%global srcname starlette

# Need to package mkautodoc to build these; that, in turn, should wait on
# https://github.com/tomchristie/mkautodoc/issues/30.
%bcond_with html_docs

Name:           python-%{srcname}
Version:        0.14.2
Release:        5%{?dist}
Summary:        The little ASGI library that shines

License:        BSD
URL:            https://www.starlette.io/
Source0:        %{pypi_source}
Source1:        pytest.ini
BuildArch:      noarch

BuildRequires:  python3-devel
BuildRequires:  pyproject-rpm-macros

# These BR’s cannot be generated because they appear only in requirements.txt.
# We do not need the “Optionals”, which correspond to the “full” extra, nor
# those for “Packaging”, which are for uploading to PyPI, but we do need those
# for “Testing”, except linters, formatters, mypy, pytest-cov:
#   - autoflake
#   - black==20.8b1
#   - flake8
#   - isort==5.*
#   - mypy
#   - pytest-cov
# Need to package this:
#BuildRequires:  python3dist(databases[sqlite])
BuildRequires:  python3dist(flake8)
BuildRequires:  python3dist(pytest)
BuildRequires:  python3dist(pytest-cov)
BuildRequires:  python3dist(pytest-asyncio)

%if %{with html_docs}
# See “Documentation” in requirements.txt. These BR’s cannot be automatically
# generated.
BuildRequires:  python3dist(mkdocs)
BuildRequires:  python3dist(mkdocs-material)
BuildRequires:  python3dist(mkautodoc)
%endif


%global common_description %{expand:
Starlette is a lightweight ASGI framework/toolkit, which is ideal for building
high performance asyncio services.

It is production-ready, and gives you the following:

  * Seriously impressive performance.
  * WebSocket support.
  * GraphQL support.
  * In-process background tasks.
  * Startup and shutdown events.
  * Test client built on requests.
  * CORS, GZip, Static Files, Streaming responses.
  * Session and Cookie support.
  * 100% test coverage.
  * 100% type annotated codebase.
  * Zero hard dependencies.}

%description %{common_description}


%generate_buildrequires
%pyproject_buildrequires -x full


%pyproject_extras_subpkg -n python3-%{srcname} full


%package -n     python3-%{srcname}
Summary:        %{summary}

%description -n python3-%{srcname} %{common_description}


%package doc
Summary:        Documentation for %{name}

%description doc %{common_description}


%prep
%autosetup -n %{srcname}-%{version}
# Remove bundled egg-info
rm -rf %{srcname}.egg-info
# Remove Gitter chat app from documentation; it relies on pre-compiled/minified
# JavaScript, which is not acceptable in Fedora.
find docs/js -type f |
  while read -r fn
  do
    cat /dev/null > "${fn}"
  done


%build
%pyproject_wheel
%if %{with html_docs}
mkdocs build
%endif


%install
%pyproject_install
%pyproject_save_files %{srcname}
install -t '%{buildroot}%{_pkgdocdir}' -D -m 0644 -p README.md
%if %{with html_docs}
cp -rp site '%{buildroot}%{_pkgdocdir}/'
%else
cp -rp docs '%{buildroot}%{_pkgdocdir}/markdown'
%endif


%check
# Need to package python3-databases first:
rm tests/test_database.py
# Built-in GraphQL support is being deprecated
# (https://github.com/encode/starlette/issues/619), and the tests do not work
# because they use a legacy graphql-core API that is no longer present:
#       from graphql.execution.executors.asyncio import AsyncioExecutor
#   E   ModuleNotFoundError: No module named 'graphql.execution.executors'
rm tests/test_graphql.py

# Sanity check: we do not want to overwrite an existing pytest.ini:
! [ -e pytest.ini ]
# See the file itself for comments on why this is needed.
cp -p '%{SOURCE1}' .

%pytest


%files -n python3-%{srcname} -f %{pyproject_files}
%license LICENSE.md


%files doc
%license LICENSE.md
%{_pkgdocdir}


%changelog
* Tue Mar 16 2021 Benjamin A. Beasley <code@musicinmybrain.net> - 0.14.2-5
- Drop python3dist(setuptools) BR, redundant with %%pyproject_buildrequires

* Mon Mar 01 2021 Benjamin A. Beasley <code@musicinmybrain.net> - 0.14.2-4
- Move documentation BR’s to base package

* Fri Feb 26 2021 Benjamin A. Beasley <code@musicinmybrain.net> - 0.14.2-3
- Drop mypy BR

* Thu Feb 25 2021 Benjamin A. Beasley <code@musicinmybrain.net> - 0.14.2-2
- Use srcname macro instead of pypi_name
- Drop obsolete python_provide macro
- Implement the “full” extra metapackage, dropping the corresponding
  dependencies from the main package
- Use pyproject-rpm-macros, including generated BR’s
- Improved description from upstream

* Wed Feb 03 2021 Filipe Rosset <rosset.filipe@gmail.com> - 0.14.2-1
- Update to 0.14.2 fixes FTBFS rhbz#1908274

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.13.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Sep 30 2020 Itamar Reis Peixoto <itamar@ispbrasil.com.br> - 0.13.8-1
- Initial package.
- Switch to github sources and enable some tests
