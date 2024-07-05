#!/usr/bin/with-contenv bash
# shellcheck shell=bash

# Create config file
CONF_FILE="/config/config.xml"
touch ${CONF_FILE}
chown abc:users ${CONF_FILE}

# Start config file
echo "<Config>" > ${CONF_FILE}

# apikey config
[ -n "${RADARR_APIKEY}" ] && echo "  <ApiKey>${RADARR_APIKEY}</ApiKey>" >> ${CONF_FILE}

# authenticationMethod config
if [ -n "${RADARR_AUTHMETHOD}" ]; then
  echo "  <AuthenticationMethod>${RADARR_AUTHMETHOD}</AuthenticationMethod>" >> ${CONF_FILE}
else
  echo "  <AuthenticationMethod>Forms</AuthenticationMethod>" >> ${CONF_FILE}
fi

# postgresql config
if [ -n "${RADARR_DBUSER}" ] && [ -n "${RADARR_DBPASS}" ] && [ -n "${RADARR_DBPORT}" ] && [ -n "${RADARR_DBHOST}" ]; then
  echo "  <PostgresUser>${RADARR_DBUSER}</PostgresUser>" >> ${CONF_FILE}
  echo "  <PostgresPassword>${RADARR_DBPASS}</PostgresPassword>" >> ${CONF_FILE}
  echo "  <PostgresPort>${RADARR_DBPORT}</PostgresPort>" >> ${CONF_FILE}
  echo "  <PostgresHost>${RADARR_DBHOST}</PostgresHost>" >> ${CONF_FILE}
fi

# End config file
echo "</Config>" >> ${CONF_FILE}