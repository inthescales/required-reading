crontab -l > tmp
echo "0 */2 * * * sh /var/www/bots/required-reading/scripts/run" >> tmp
crontab tmp
