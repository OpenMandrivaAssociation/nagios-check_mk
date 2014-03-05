Name:		nagios-check_mk
Version:	1.1.10
Release:	2
Summary:	A new general purpose Nagios-plugin for retrieving data
Group:		Networking/Other
License:	BSD
URL:		http://mathias-kettner.de/check_mk
Source:     http://mathias-kettner.de/download/check_mk-%{version}.tar.gz
BuildArch:  noarch

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
install -d -m 755 %{buildroot}%{_bindir}
cat > %{buildroot}%{_bindir}/check_mk <<'EOF'
#!/bin/sh
exec python %{_datadir}/check_mk/modules/check_mk.py "$@"
EOF
chmod +x %{buildroot}%{_bindir}/check_mk

install -d -m 755 %{buildroot}%{_sysconfdir}/check_mk
cat > %{buildroot}%{_sysconfdir}/check_mk/main.mk <<'EOF'
all_hosts = [ "localhost" ]
EOF

install -d -m 755 %{buildroot}%{_datadir}/check_mk
install -d -m 755 %{buildroot}%{_datadir}/check_mk/modules
tar xf modules.tar.gz -C %{buildroot}%{_datadir}/check_mk/modules
install -d -m 755 %{buildroot}%{_datadir}/check_mk/checks
tar xf checks.tar.gz -C %{buildroot}%{_datadir}/check_mk/checks
install -d -m 755 %{buildroot}%{_datadir}/check_mk/web
tar xf web.tar.gz -C %{buildroot}%{_datadir}/check_mk/web
install -d -m 755 %{buildroot}%{_datadir}/check_mk/pnp-templates
tar xf pnp-templates.tar.gz -C %{buildroot}%{_datadir}/check_mk/pnp-templates

cat > %{buildroot}%{_datadir}/check_mk/modules/defaults <<'EOF'
# created during package creation

check_mk_version            = '%{version}'
default_config_dir          = '%{_sysconfdir}/check_mk'
check_mk_configdir          = '%{_sysconfdir}/check_mk/conf.d'
checks_dir                  = '%{_datadir}/check_mk/checks'
check_manpages_dir          = '%{_datadir}/check_mk/doc/checks'
modules_dir                 = '%{_datadir}/check_mk/modules'
agents_dir                  = '%{_datadir}/check_mk/agents'
var_dir                     = '%{_localstatedir}/lib/check_mk'
lib_dir                     = ''
autochecksdir               = '%{_localstatedir}/lib/check_mk/autochecks'
precompiled_hostchecks_dir  = '%{_localstatedir}/lib/check_mk/precompiled'
counters_directory          = '%{_localstatedir}/lib/check_mk/counters'
tcp_cache_dir               = '%{_localstatedir}/lib/check_mk/cache'
logwatch_dir                = '%{_localstatedir}/lib/check_mk/logwatch'
nagios_objects_file         = '%{_sysconfdir}/nagios/objects/check_mk_objects.cfg'
rrd_path                    = '%{_localstatedir}/lib/check_mk/rrd'
nagios_command_pipe_path    = '/var/log/nagios/rw/nagios.cmd'
nagios_status_file          = '/var/log/nagios/status.dat'
nagios_conf_dir             = '/etc/nagios/objects'
nagios_user                 = 'nagios'
nagios_url                  = '/nagios'
nagios_cgi_url              = '/nagios/cgi-bin'
logwatch_notes_url          = '/check_mk/logwatch.py?host=%s&file=%s'
www_group                   = 'apache'
nagios_config_file          = '%{_sysconfdir}/nagios/nagios.cfg'
nagios_startscript          = '%{_initrddir}/nagios'
nagios_binary               = '%{_sbindir}/nagios'
apache_config_dir           = '%{_sysconfdir}/httpd/conf/webapps.d'
htpasswd_file               = '%{_sysconfdir}/check_mk/htpasswd.users'
nagios_auth_name            = 'Nagios Access'
web_dir                     = '%{_datadir}/check_mk/web'
checkmk_web_uri             = '/check_mk'
livestatus_unix_socket      = '/'
livebackendsdir             = ''
pnp_url                     = '/pnp4nagios/'
pnp_templates_dir           = '%{_datadir}/check_mk/pnp-templates'
doc_dir                     = '%{_datadir}/doc/check_mk'
EOF
cp %{buildroot}%{_datadir}/check_mk/modules/defaults \
    %{buildroot}%{_datadir}/check_mk/web/htdocs/defaults.py

install -d -m 755 %{buildroot}%{_localstatedir}/lib/check_mk
install -d -m 755 %{buildroot}%{_localstatedir}/lib/check_mk/autochecks
install -d -m 755 %{buildroot}%{_localstatedir}/lib/check_mk/cache
install -d -m 755 %{buildroot}%{_localstatedir}/lib/check_mk/counters
install -d -m 755 %{buildroot}%{_localstatedir}/lib/check_mk/precompiled
install -d -m 755 %{buildroot}%{_localstatedir}/lib/check_mk/logwatch
install -d -m 755 %{buildroot}%{_localstatedir}/lib/check_mk/rrd

install -d -m 755 %{buildroot}%{_docdir}/%{name}
tar xf doc.tar.gz -C %{buildroot}%{_docdir}/%{name} --exclude livestatus

install -d -m 755 %{buildroot}%{_sysconfdir}/xinetd.d
install -m 644 xinetd.conf %{buildroot}%{_sysconfdir}/xinetd.d/check_mk_agent

install -d -m 755 %{buildroot}%{_bindir}
install -m 755 check_mk_agent.linux %{buildroot}%{_bindir}/check_mk_agent

install -d -m 755 %{buildroot}%{_datadir}/check_mk_agent
install -d -m 755 %{buildroot}%{_datadir}/check_mk_agent/plugins
install -d -m 755 %{buildroot}%{_datadir}/check_mk_agent/local
install -m 644 plugins/mk_logwatch %{buildroot}%{_datadir}/check_mk_agent/plugins
install -m 644 plugins/j4p_performance %{buildroot}%{_datadir}/check_mk_agent/plugins
install -m 644 plugins/mk_oracle %{buildroot}%{_datadir}/check_mk_agent/plugins
install -m 644 plugins/sylo %{buildroot}%{_datadir}/check_mk_agent/plugins

install -d -m 755 %{buildroot}%{_sysconfdir}/check_mk_agent
install -m 644 logwatch.cfg %{buildroot}%{_sysconfdir}/check_mk_agent

perl -pi \
    -e 's|LIBDIR="/to/be/changed"|LIBDIR="%{_datadir}/check_mk_agent"|;' \
    -e 's|CONFDIR="/to/be/changed"|CONFDIR="%{_sysconfdir}/check_mk_agent"|;' \
    %{buildroot}%{_bindir}/check_mk_agent

%files
%doc %{_docdir}/%{name}
%{_bindir}/check_mk
%config(noreplace) %{_sysconfdir}/check_mk
%{_datadir}/check_mk
%{_localstatedir}/lib/check_mk

%files agent
%{_bindir}/check_mk_agent
%{_datadir}/check_mk_agent
%config(noreplace) %{_sysconfdir}/xinetd.d/check_mk_agent
%config(noreplace) %{_sysconfdir}/check_mk_agent
