htpasswd -bc /etc/apache2/.htpasswd "$USERNAME" "$PASSWORD"
mkdir -p /data
chown www-data:www-data /data
echo "Make sure all files are owned by UID `id -u www-data`"
/usr/sbin/apache2ctl -DFOREGROUND
