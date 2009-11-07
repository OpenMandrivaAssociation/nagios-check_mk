%define name	nagios-check_mk
%define version	1.0.39
%define release	%mkrel 1
%define _requires_exceptions pear(default.php)

Name:		%{name}
Version:	%{version}
Release:	%{release}
Summary:	A new general purpose Nagios-plugin for retrieving data
Group:		Networking/Other
License:	BSD
URL:		http://mathias-kettner.de/check_mk
Source:     http://mathias-kettner.de/download/check_mk-%{version}.tar.gz
BuildArch:  noarch
BuildRoot:  %{_tmppath}/%{name}-%{version}

%description
check_mk is a general purpose Nagios-plugin for retrieving data. It adopts a
new approach for collecting data from operating systems and network components.
It obsoletes NRPE, check_by_ssh, NSClient, and check_snmp and it has many
benefits, the most important of which are significant reduction of CPU usage on
the Nagios host and automatic inventory of items to be checked on hosts. The
larger your Nagios installation is, the more helpful these improvements.

%package agent
Summary:    Agent for check_mk
Requires:   xinetd
Group:      Networking/Other

%description agent
This package contains the agent for check_mk. Install this on
all Linux machines you want to monitor via check_mk.

%prep
%setup -q -n check_mk-%{version}
tar xf agents.tar.gz

%build

%install
rm -rf %{buildroot}

install -d -m 755 %{buildroot}%{_datadir}/nagios/plugins
cat > %{buildroot}%{_datadir}/nagios/plugins/check_mk <<'EOF'
#!/bin/sh
exec python %{_datadir}/check_mk/modules/check_mk.py "$@"
EOF

install -d -m 755 %{buildroot}%{_datadir}/check_mk
install -d -m 755 %{buildroot}%{_datadir}/check_mk/modules
tar xf modules.tar.gz -C %{buildroot}%{_datadir}/check_mk/modules
install -d -m 755 %{buildroot}%{_datadir}/check_mk/checks
tar xf checks.tar.gz -C %{buildroot}%{_datadir}/check_mk/checks
install -d -m 755 %{buildroot}%{_datadir}/check_mk/htdocs
tar xf htdocs.tar.gz -C %{buildroot}%{_datadir}/check_mk/htdocs
install -d -m 755 %{buildroot}%{_datadir}/check_mk/pnp-templates
tar xf pnp-templates.tar.gz -C %{buildroot}%{_datadir}/check_mk/pnp-templates

install -d -m 755 %{buildroot}%{_localstatedir}/lib/check_mk
install -d -m 755 %{buildroot}%{_localstatedir}/lib/check_mk/autochecks
install -d -m 755 %{buildroot}%{_localstatedir}/lib/check_mk/cache
install -d -m 755 %{buildroot}%{_localstatedir}/lib/check_mk/counters
install -d -m 755 %{buildroot}%{_localstatedir}/lib/check_mk/precompiled
install -d -m 755 %{buildroot}%{_localstatedir}/lib/check_mk/logwatch
install -d -m 755 %{buildroot}%{_localstatedir}/lib/check_mk/rrd

install -d -m 755 %{buildroot}%{_docdir}/%{name}
tar xf doc.tar.gz -C %{buildroot}%{_docdir}/%{name}

install -d -m 755 %{buildroot}%{_sysconfdir}/xinetd.d
install -m 644 xinetd.conf %{buildroot}%{_sysconfdir}/xinetd.d/check_mk_agent

install -d -m 755 %{buildroot}%{_bindir}
install -m 755 check_mk_agent.linux %{buildroot}%{_bindir}/check_mk_agent

install -d -m 755 %{buildroot}%{_datadir}/check_mk_agent
install -d -m 755 %{buildroot}%{_datadir}/check_mk_agent/plugins
install -d -m 755 %{buildroot}%{_datadir}/check_mk_agent/local
install -m 644 mk_logwatch %{buildroot}%{_datadir}/check_mk_agent/plugins

install -d -m 755 %{buildroot}%{_sysconfdir}/check_mk_agent
install -m 644 logwatch.cfg %{buildroot}%{_sysconfdir}/check_mk_agent

perl -pi \
    -e 's|LIBDIR="/to/be/changed"|LIBDIR="%{_datadir}/check_mk_agent"|;' \
    -e 's|CONFDIR="/to/be/changed"|CONFDIR="%{_sysconfdir}/check_mk_agent"|;' \
    %{buildroot}%{_bindir}/check_mk_agent

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc %{_docdir}/%{name}
%{_datadir}/nagios/plugins/check_mk
%{_datadir}/check_mk
%{_localstatedir}/lib/check_mk

%files agent
%defattr(-,root,root)
%{_bindir}/check_mk_agent
%{_datadir}/check_mk_agent
%config(noreplace) %{_sysconfdir}/xinetd.d/check_mk_agent
%config(noreplace) %{_sysconfdir}/check_mk_agent

