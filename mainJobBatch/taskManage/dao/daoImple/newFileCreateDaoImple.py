from mainJobBatch.taskManage.dao.newFileCreateDao import NewFileCreateDao

class NewFileCreateDaoImple(NewFileCreateDao):
    def jadgeJobNumStock(self, cur, user_id):
        select_user_job_num = ("""
        SELECT
          JOB_QUE_DATA.job_num
        FROM
          scrapingSystem_jobquedata AS JOB_QUE_DATA
        INNER JOIN scrapingSystem_processresultdata AS PROCESS_RESULT
          ON PROCESS_RESULT.result_file_num = JOB_QUE_DATA.result_file_num
        WHERE
          JOB_QUE_DATA.user_id = '""" + user_id + """'
          AND PROCESS_RESULT.file_create_status <> 'エラー'
        ORDER BY JOB_QUE_DATA.job_num ASC""")

        try:
            cur.execute(select_user_job_num)
            cur.fetchall()
            if cur.rowcount == 0:
                return True
            else:
                return False
        except:
            raise

    def getJobQueData(self, cur, user_id):
        select_user_job_id = ("""
        SELECT
          JOB_QUE_DATA.job_num,
          JOB_QUE_DATA.result_file_num
        FROM
          scrapingSystem_jobquedata AS JOB_QUE_DATA
        INNER JOIN scrapingSystem_processresultdata AS PROCESS_RESULT
          ON PROCESS_RESULT.result_file_num = JOB_QUE_DATA.result_file_num
        WHERE
          JOB_QUE_DATA.user_id = '""" + user_id + """'
          AND PROCESS_RESULT.file_create_status <> 'エラー'
        ORDER BY JOB_QUE_DATA.job_num ASC""")

        try:
            cur.execute(select_user_job_id)
            rows = cur.fetchall()

            job_num_list = []
            result_file_num_list = []
            for row in rows:
                job_num_list.append(row[0])
                result_file_num_list.append(row[1])

            result_list = {
                "job_num_list": job_num_list,
                "result_file_num_list": result_file_num_list,
            }
            return result_list
        except:
            raise