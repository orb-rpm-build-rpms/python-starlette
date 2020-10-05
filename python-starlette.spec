%global pypi_name starlette

Name:           python-%{pypi_name}
Version:        0.13.8
Release:        1%{?dist}
Summary:        The little ASGI library that shines

License:        BSD
URL:            https://github.com/encode/starlette
#uses github sources for having tests.
Source0:        %{pypi_source}
BuildArch:      noarch

BuildRequires:  python3-devel
BuildRequires:  python3dist(pytest)
BuildRequires:  python3dist(pytest-cov)
BuildRequires:  python3dist(pytest-asyncio)
BuildRequires:  python3dist(requests)
BuildRequires:  python3dist(itsdangerous)
BuildRequires:  python3dist(jinja2)
BuildRequires:  python3dist(pyyaml)
BuildRequires:  python3dist(setuptools)
BuildRequires:  python3dist(aiofiles)
BuildRequires:  python3dist(graphene)
BuildRequires:  python3dist(ujson)

%description
The little ASGI framework that shines

%package -n     python3-%{pypi_name}
Summary:        %{summary}
%{?python_provide:%python_provide python3-%{pypi_name}}

Requires:       python3dist(aiofiles)
Requires:       python3dist(graphene)
Requires:       python3dist(itsdangerous)
Requires:       python3dist(jinja2)
Requires:       python3dist(python-multipart)
Requires:       python3dist(pyyaml)
Requires:       python3dist(requests)
Requires:       python3dist(ujson)

%description -n python3-%{pypi_name}
The little ASGI framework that shines

%prep
%autosetup -n %{pypi_name}-%{version}
# Remove bundled egg-info
rm -rf %{pypi_name}.egg-info

%build
%py3_build

%install
%py3_install

%check
rm tests/test_database.py
rm tests/test_graphql.py
rm tests/test_formparsers.py
rm tests/test_requests.py
%pytest


%files -n python3-%{pypi_name}
%license LICENSE.md
%doc README.md
%{python3_sitelib}/%{pypi_name}
%{python3_sitelib}/%{pypi_name}-%{version}-py%{python3_version}.egg-info

%changelog
* Wed Sep 30 2020 Itamar Reis Peixoto <itamar@ispbrasil.com.br> - 0.13.8-1
- Initial package.
- Switch to github sources and enable some tests