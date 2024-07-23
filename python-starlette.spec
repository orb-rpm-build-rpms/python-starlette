Name:           python-starlette
Version:        0.37.2
Release:        %autorelease
Summary:        The little ASGI library that shines

License:        BSD-3-Clause
URL:            https://www.starlette.io/
Source:         https://github.com/encode/starlette/archive/%{version}/starlette-%{version}.tar.gz

# Fix 3.13.0b3/b4 compatibility:
#   Fix `routing.get_name()` not to assume all routines have `__name__`
#   https://github.com/encode/starlette/pull/2648
#
# This is a workaround for a change in Python 3.13.0b3:
#   https://github.com/python/cpython/commit/49e5740135670e04ae6da7e6f52dbe380655e0f1
#
# It is possible that this will be considered a Python bug/regression and fixed
# by 3.13.0 final. It was reported as a possible bug in:
#   3.13.0b3: undocumented change in inspect.isroutine() for functools.partial
#   https://github.com/python/cpython/issues/122087
# …and there should be a decision or resolution one way or the other by Python
# 3.13.0rc1. This should therefore be a temporary patch, and it should be
# either merged upstream or dropped as unnecessary after Python 3.13.0rc1 is
# released.
Patch:          https://github.com/encode/starlette/pull/2648.patch

BuildArch:      noarch

BuildRequires:  python3-devel
# The file requirements.txt pins exact versions and contains many unwanted
# dependencies, e.g. linters and typecheckers (see
# https://docs.fedoraproject.org/en-US/packaging-guidelines/Python/#_linters).
# It’s easier to maintain BuildRequires for testing manually than to heavily
# patch or process the requirements file.
BuildRequires:  %{py3_dist pytest}
BuildRequires:  %{py3_dist trio}
BuildRequires:  %{py3_dist typing_extensions}

Obsoletes:      python-starlette-doc < 0.16.0-10

%global common_description %{expand:
Starlette is a lightweight ASGI framework/toolkit, which is ideal for building
async web services in Python.

It is production-ready, and gives you the following:

  • A lightweight, low-complexity HTTP web framework.
  • WebSocket support.
  • In-process background tasks.
  • Startup and shutdown events.
  • Test client built on requests.
  • CORS, GZip, Static Files, Streaming responses.
  • Session and Cookie support.
  • 100%% test coverage.
  • 100%% type annotated codebase.
  • Few hard dependencies.
  • Compatible with asyncio and trio backends.
  • Great overall performance against independent benchmarks.}

%description %{common_description}


%package -n     python3-starlette
Summary:        %{summary}

%description -n python3-starlette %{common_description}


%pyproject_extras_subpkg -n python3-starlette full


%prep
%autosetup -n starlette-%{version} -p1


%generate_buildrequires
%pyproject_buildrequires -x full


%build
%pyproject_wheel


%install
%pyproject_install
%pyproject_save_files -l starlette


%check
# E       trio.TrioDeprecationWarning: The `cancellable=` keyword argument to
#         `trio.to_thread.run_sync` is deprecated since Trio 0.23.0; use
#         `abandon_on_cancel=` instead
#         (https://github.com/python-trio/trio/issues/2841)
warningsfilter="${warningsfilter-} -W ignore::trio.TrioDeprecationWarning"

# E       Failed: DID NOT WARN. No warnings of type (<class
#         'DeprecationWarning'>, <class 'PendingDeprecationWarning'>) were
#         emitted.
# E       The list of emitted warnings is: [].
k="${k-}${k+ and }not test_lifespan_with_on_events"

%if v"0%{?python3_version}" >= v"3.13"
# Python 3.13.0b2: KeyError: 'content-type' in test_debug_html[asyncio] and
# test_debug_html[trio]
# https://github.com/encode/starlette/issues/2614
k="${k-}${k+ and }not test_debug_html[asyncio]"
k="${k-}${k+ and }not test_debug_html[trio]"
# Python 3.13.0b2: test_gzip_ignored_for_responses_with_encoding_set[trio]
# fails with a ValueError: I/O operation on closed file
# https://github.com/encode/starlette/issues/2615
warningsfilter="${warningsfilter-} -W ignore::pytest.PytestUnraisableExceptionWarning"
%endif

%pytest ${warningsfilter-} -k "${k-}" -v


%files -n python3-starlette -f %{pyproject_files}
%doc README.md


%changelog
%autochangelog
