#!/bin/bash
DB_NAME="csol3" # 可以导出全部数据库"--all-databases"
# 使用有密码的mysqldump，会出现安全警告 Using a password on the command line interface can be insecure
#DB_USER="root"
#DB_PASS="" # 注意密码里面包含!，若不使用双引号，则需要使用了转义符号\!
DB_USER="root"
DB_PASS="123456"  # backup账号只能用于myqldum备份使用，密码为空
ROOT_DIR="./"
BACK_DIR="all_backup"
BACK_FILE="${DB_NAME}_`date '+%Y.%m.%d-%H%M'`.sql"
BACK_LOG="backup.log"

cd ${ROOT_DIR}
echo "--------------------`date '+%Y-%m-%d %H:%M:%S'`--------------------" >> ${BACK_LOG}
date_start=`date +%s`
echo "work on:`pwd`" >> ${BACK_LOG}
echo "start all backup" >> ${BACK_LOG}
echo "create backup file: ${BACK_DIR}/${BACK_FILE}" >> ${BACK_LOG}
mysqldump --log-error=${BACK_LOG} -u${DB_USER} -p${DB_PASS} ${DB_NAME} > ${BACK_DIR}/${BACK_FILE} 
echo "finish all backup" >> ${BACK_LOG}

echo "cleanup follows expired files (for 7 days):" >> ${BACK_LOG}
find ${BACK_DIR} -mtime +7 -type f -name "*.sql" >> ${BACK_LOG}
yes | find ${BACK_DIR} -mtime +7 -type f -name "*.sql" | xargs rm -rf >> ${BACK_LOG} 2>&1
echo "finish cleanup expired files" >> ${BACK_LOG}
date_end=`date +%s`
echo "completed. cost $((date_end-date_start)) seconds" >> ${BACK_LOG}

echo -e "\n" >> ${BACK_LOG}
