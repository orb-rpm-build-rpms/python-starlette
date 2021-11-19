Name:           python-starlette
Version:        0.17.1
Release:        %autorelease
Summary:        The little ASGI library that shines

License:        BSD
URL:            https://www.starlette.io/
Source0:        https://github.com/encode/starlette/archive/%{version}/starlette-%{version}.tar.gz
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
BuildRequires:  python3dist(pytest)
BuildRequires:  python3dist(trio)

Obsoletes:      python-starlette-doc < 0.16.0-10

%global common_description %{expand:
Starlette is a lightweight ASGI framework/toolkit, which is ideal for building
high performance async services.

It is production-ready, and gives you the following:

  • Seriously impressive performance.
  • WebSocket support.
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


%prep
%autosetup -n starlette-%{version}
# Remove Gitter chat app from documentation; it relies on pre-compiled/minified
# JavaScript, which is not acceptable in Fedora. Since we are not building
# documentation, we do this very bluntly:
rm -vrf docs/js


%generate_buildrequires
%pyproject_buildrequires -x full


%build
%pyproject_wheel


%install
%pyproject_install
%pyproject_save_files starlette


%check
%pytest


%files -n python3-starlette -f %{pyproject_files}
%doc README.md


%changelog
%autochangelog
