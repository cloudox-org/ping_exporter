%global debug_package %{nil}

Name: ping_exporter
Version: 1.2.1
Release: 1%{?dist}
Summary: Ping exporter
License: ASL 2.0
URL:        https://github.com/czerwonk/ping_exporter
Source0:    https://github.com/czerwonk/ping_exporter/releases/download/v%{version}/ping_exporter_%{version}_linux_amd64.tar.gz
Source1: %{name}.service
Source2: %{name}.default

%{?systemd_requires}
Requires(pre): shadow-utils

%description
The ping exporter allows ping probing of endpoints via ICMP.

%prep
%setup -q -c -n %{name}-%{version}_linux_amd64

%build
/bin/true

%install
mkdir -vp %{buildroot}%{_sharedstatedir}/prometheus
install -D -m 755 %{name} %{buildroot}%{_bindir}/%{name}
install -D -m 644 %{SOURCE1} %{buildroot}%{_unitdir}/%{name}.service
install -D -m 644 %{SOURCE2} %{buildroot}%{_sysconfdir}/default/%{name}

%pre
getent group prometheus >/dev/null || groupadd -r prometheus
getent passwd prometheus >/dev/null || \
useradd -r -g prometheus -d %{_sharedstatedir}/prometheus -s /sbin/nologin -c "Prometheus services" prometheus
exit 0

%post
%systemd_post %{name}.service

%preun
%systemd_preun %{name}.service

%postun
%systemd_postun %{name}.service

%files
%defattr(-,root,root,-)
%caps(cap_net_raw=ep) %{_bindir}/%{name}
%{_unitdir}/%{name}.service
%config(noreplace) %{_sysconfdir}/default/%{name}
%dir %attr(755, prometheus, prometheus)%{_sharedstatedir}/prometheus

%changelog
* Thu Aug 06 2026 Ivan Garcia <igarcia@cloudox.org> - 1.2.1
- Initial packaging for the 1.2.1 branch, switch to https://github.com/czerwonk/ping_exporter
* Thu Apr 23 2026 Ivan Garcia <igarcia@cloudox.org> - 1.2.0
- Initial packaging for the 1.2.0 branch, switch to https://github.com/czerwonk/ping_exporter
