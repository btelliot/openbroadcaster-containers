# Allow the kill signal to kill the right process
_term() { 
  echo "Quitting" 
  kill -TERM "$child" 2>/dev/null
}

trap _term SIGTERM

####### Begin Startup ...

echo "[OK] Begin startup"

echo "[INFO] Testing NGINX configuration"
nginx -t

echo "[INFO] Starting php8.3-fpm"
service php8.3-fpm start

echo "[INFO] Running OB updates"
#php /var/www/html/updates/index.php force-update
tools/cli/ob updates run all

echo "[INFO] Updating password"
#php /var/www/html/tools/password_change.php "admin" "password"
tools/cli/ob passwd admin << EOF
password
password
EOF

nginx -g 'daemon off;' &

echo "[OK] NGINX is running..."

####### Application Running ...

# Wait for SIGTERM (kill signal)
child=$!
wait "$child"