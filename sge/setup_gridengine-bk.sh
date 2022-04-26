#!/bin/bash

#hostname > /var/lib/gridengine/default/common/act_qmaster
/etc/init.d/gridengine-master start
/etc/init.d/gridengine-exec start

cat << EOS  > /tmp/qconf-ae.txt
hostname              $(hostname)
load_scaling          NONE
complex_values        NONE
user_lists            NONE
xuser_lists           NONE
projects              NONE
xprojects             NONE
usage_scaling         NONE
report_variables      NONE
EOS

qconf -Ae /tmp/qconf-ae.txt


# Add submit host
qconf -as `hostname`

# shell bash
cat << EOS > /tmp/qconf-aq.txt
qname                 testq
hostlist              $(hostname)
seq_no                0
load_thresholds       np_load_avg=1.75
suspend_thresholds    NONE
nsuspend              1
suspend_interval      00:05:00
priority              0
min_cpu_interval      00:05:00
processors            UNDEFINED
qtype                 BATCH INTERACTIVE
ckpt_list             NONE
pe_list               make
rerun                 FALSE
slots                 1
tmpdir                /tmp
shell                 /bin/bash
prolog                NONE
epilog                NONE
shell_start_mode      posix_compliant
starter_method        NONE
suspend_method        NONE
resume_method         NONE
terminate_method      NONE
notify                00:00:60
owner_list            NONE
user_lists            NONE
xuser_lists           NONE
subordinate_list      NONE
complex_values        NONE
projects              NONE
xprojects             NONE
calendar              NONE
initial_state         default
s_rt                  INFINITY
h_rt                  INFINITY
s_cpu                 INFINITY
h_cpu                 INFINITY
s_fsize               INFINITY
h_fsize               INFINITY
s_data                INFINITY
h_data                INFINITY
s_stack               INFINITY
h_stack               INFINITY
s_core                INFINITY
h_core                INFINITY
s_rss                 INFINITY
h_rss                 INFINITY
s_vmem                INFINITY
h_vmem                INFINITY
EOS

cat /etc/gridengine/configuration >> qconf -aconf sgemaster
# shell bash
cat "
#global:
hostname              	     $(hostname)
execd_spool_dir              /var/spool/gridengine/execd
mailer                       /usr/bin/mail
xterm                        /usr/bin/xterm
load_sensor                  none
prolog                       none
epilog                       none
shell_start_mode             posix_compliant
login_shells                 bash,sh,ksh,csh,tcsh
min_uid                      33
min_gid                      33
user_lists                   none
xuser_lists                  none
projects                     none
xprojects                    none
enforce_project              false
enforce_user                 auto
load_report_time             00:00:40
max_unheard                  00:05:00
reschedule_unknown           00:00:00
loglevel                     log_warning
administrator_mail           root
set_token_cmd                none
pag_cmd                      none
token_extend_time            none
shepherd_cmd                 none
qmaster_params               none
execd_params                 none
reporting_params             accounting=true reporting=false \
                             flush_time=00:00:15 joblog=false sharelog=00:00:00
finished_jobs                100
gid_range                    65400-65500
qlogin_command               builtin
qlogin_daemon                builtin
rlogin_command               builtin
rlogin_daemon                builtin
rsh_command                  builtin
rsh_daemon                   builtin
max_aj_instances             2000
max_aj_tasks                 75000
max_u_jobs                   0
max_jobs                     0
auto_user_oticket            0
auto_user_fshare             0
auto_user_default_project    none
auto_user_delete_time        86400
delegated_file_staging       false
reprioritize                 0
jsv_url                      none
jsv_allowed_mod              ac,h,i,e,o,j,M,N,p,w
"



# avoid 'stdin: is not a tty'
#sed -i -e 's/^mesg n//' /root/.profile

echo "hostname ; date" | qsub


#
for HOST in $@
do
  qconf -as $HOST
  #qconf -as mail.domain.es
done
