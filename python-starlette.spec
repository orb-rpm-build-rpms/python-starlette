# As of 2021-08-11, mkdocs and many of its dependencies are orphaned.
#
# We would also need to package mkautodoc to build these; that, in turn, should
# wait on https://github.com/tomchristie/mkautodoc/issues/30.
%bcond_with mkdocs

Name:           python-starlette
Version:        0.16.0
Release:        %autorelease
Summary:        The little ASGI library that shines

License:        BSD
URL:            https://www.starlette.io/
Source0:        https://github.com/encode/starlette/archive/%{version}/starlette-%{version}.tar.gz
Source1:        pytest.ini
BuildArch:      noarch

BuildRequires:  python3-devel

# These BR’s cannot be generated because they appear only in requirements.txt.
# We do not need the “Optionals”, which correspond to the “full” extra, nor
# those for “Packaging”, which are for uploading to PyPI, but we do need those
# for “Testing”, except linters, formatters, mypy:
#   - autoflake
#   - black==20.8b1
#   - coverage>=5.3
#   - flake8
#   - isort==5.*
#   - mypy
#   - types-requests
#   - types-contextvars
#   - types-PyYAML
#   - types-dataclasses
BuildRequires:  python3dist(databases[sqlite])
BuildRequires:  python3dist(flake8)
BuildRequires:  python3dist(pytest)
BuildRequires:  python3dist(trio)

%if %{with mkdocs}
# See “Documentation” in requirements.txt. These BR’s cannot be automatically
# generated.
BuildRequires:  python3dist(mkdocs)
BuildRequires:  python3dist(mkautodoc)
%endif


%global common_description %{expand:
Starlette is a lightweight ASGI framework/toolkit, which is ideal for building
high performance async services.

It is production-ready, and gives you the following:

  • Seriously impressive performance.
  • WebSocket support.
  • GraphQL support.
  • In-process background tasks.
  • Startup and shutdown events.
  • Test client built on requests.
  • CORS, GZip, Static Files, Streaming responses.
  • Session and Cookie support.
  • 100%% test coverage.
  • 100%% type annotated codebase.
  • Few hard dependencies.
  • Compatible with asyncio and trio backends.}

%description %{common_description}


%pyproject_extras_subpkg -n python3-starlette full


%package -n     python3-starlette
Summary:        %{summary}

%description -n python3-starlette %{common_description}


%package doc
Summary:        Documentation for %{name}

%description doc %{common_description}


%prep
%autosetup -n starlette-%{version}
# Remove bundled egg-info
rm -rf starlette.egg-info
# Remove Gitter chat app from documentation; it relies on pre-compiled/minified
# JavaScript, which is not acceptable in Fedora.
find docs/js -type f |
  while read -r fn
  do
    cat /dev/null > "${fn}"
  done
# Drop dependency on mkdocs-material. See
# https://bugzilla.redhat.com/show_bug.cgi?id=1960274#c3. The result doesn’t
# look as nice but is still usable.
sed -r -i 's/\bmaterial\b/mkdocs/' mkdocs.yml


%generate_buildrequires
%pyproject_buildrequires -x full


%build
%pyproject_wheel
%if %{with mkdocs}
mkdocs build
%endif


%install
%pyproject_install
%pyproject_save_files starlette
install -t '%{buildroot}%{_pkgdocdir}' -D -m 0644 -p README.md
%if %{with mkdocs}
cp -rp site '%{buildroot}%{_pkgdocdir}/'
%else
cp -rp docs '%{buildroot}%{_pkgdocdir}/markdown'
%endif


%check
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


%files -n python3-starlette -f %{pyproject_files}


%files doc
%license LICENSE.md
%{_pkgdocdir}


%changelog
%autochangelog
