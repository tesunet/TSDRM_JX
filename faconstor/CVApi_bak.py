import time
import base64
import requests
from lxml import etree
import copy
import threading
import operator
from concurrent.futures import ThreadPoolExecutor
import json


class CVRestApiToken(object):
    """
    CV 登陆接口
    """

    def __init__(self):
        self.is_login = False
        self.credit = {"web_addr": "", "port": "", "username": "", "pass_wd": "", "token": "", "last_login": 0}
        self.msg = ""
        self.service = 'http://<<server>>:<<port>>/SearchSvc/CVWebService.svc/'

    def login(self, credit):
        # 重置登录口令，清除上次登录记录
        if self.is_login is False:
            self.credit["token"] = None
            self.credit["last_login"] = 0

        # 初始化登录信息
        try:
            self.credit["web_addr"] = credit["web_addr"]
            self.credit["port"] = credit["port"]
            self.credit["username"] = credit["username"]
            self.credit["pass_wd"] = credit["pass_wd"]
            self.credit["token"] = credit["token"]
            self.credit["last_login"] = credit["last_login"]
        except Exception as e:
            self.msg = "登录信息有误！"
            print(self.msg, e)
            return None

        # 设置延用上次口令时长，避免重复登录
        if self.credit["token"] and self.credit["token"].count("QSDK") == 1:
            diff = time.time() - self.credit["last_login"]
            if diff <= 550:
                return self.credit["token"]
        self.is_login = self._login()
        return self.credit["token"]

    def _login(self):
        # 请求url
        self.service = self.service.replace("<<server>>", self.credit["web_addr"]).replace("<<port>>",
                                                                                           self.credit["port"])
        # 密码64位编码格式
        password = base64.b64encode(self.credit["pass_wd"].encode(encoding="utf-8"))

        # 请求体
        login_req = """<DM2ContentIndexing_CheckCredentialReq mode="Webconsole" username="{username}" password="{password}" />""".format(
            **{
                "username": self.credit["username"],
                "password": password.decode(),
            })
        # 发起请求
        try:
            ret = requests.post(self.service + "Login", data=login_req)
        except Exception as e:
            self.msg = "连接失败：web_addr {0} port {1}".format(self.credit["web_addr"], self.credit["port"])
            print(self.msg, e)
            return False
        if ret.status_code == 200:
            try:
                root = etree.XML(ret.content)
            except Exception as e:
                self.mag = "返回字符未格式化！"
                print(self.msg, e)
                return False

            if "token" in root.keys():
                self.credit["token"] = root.attrib["token"]
                if self.credit["token"].count("QSDK") == 1:
                    self.is_login = True
                    self.credit["last_login"] = time.time()
                    self.msg = "登陆成功"

                    return True
                else:
                    self.msg = "登陆失败：username {0} password {1}".format(self.credit["username"], self.credit["pass_wd"])
        else:
            self.msg = "连接失败：web_addr {0} port {1}".format(self.credit["web_addr"], self.credit["port"])

        return False

    def check_login(self):
        return self.login(self.credit)

    def get_token_string(self):
        return self.credit["token"]


class CVRestApiCmd(object):
    """
    CV 提供的请求接口
    """

    def __init__(self, token):
        self.msg = ""
        self.web_addr = token.credit["web_addr"]
        self.port = token.credit["port"]
        self.service = 'http://{server}:{port}/SearchSvc/CVWebService.svc/'.format(
            **{"server": token.credit["web_addr"], "port": token.credit["port"]})
        self.token = token
        self.receive_text = ""

    def _rest_cmd(self, rest_cmd, command, update_cmd=""):
        token = self.token.check_login()
        if token is None:
            self.msg = "没有获取到token值"
            print(self.msg)
            return None

        client_props_req = self.service + command
        print("request:", client_props_req)
        try:
            update = update_cmd.encode(encoding="utf-8")
        except:
            update = update_cmd
        headers = {
            'Cookie2': token,
        }

        if rest_cmd == "GET":
            try:
                r = requests.get(client_props_req, data=update, headers=headers)
            except:
                self.msg = "Connect Failed: web_addr " + self.web_addr + " port " + self.port
                print(self.msg)
                return None

        elif rest_cmd == "POST":
            try:
                r = requests.post(client_props_req, data=update, headers=headers)
            except:
                self.msg = "Connect Failed: web_addr " + self.web_addr + " port " + self.port
                return None

        elif rest_cmd == "PUT":
            try:
                r = requests.put(client_props_req, data=update, headers=headers)
            except:
                self.msg = "Connect Failed: web_addr " + self.web_addr + " port " + self.port
                return None

        elif rest_cmd == "DEL":
            try:
                r = requests.delete(client_props_req, data=update, headers=headers)
            except:
                self.msg = "Connect Failed: web_addr " + self.web_addr + " port " + self.port
                return None

        elif rest_cmd == "QCMD":
            try:
                r = requests.post(client_props_req, data=update, headers=headers)
            except:
                self.msg = "Connect Failed: web_addr " + self.web_addr + " port " + self.port
                return None
        else:
            print("未匹配到正确的请求方法")
            r = None

        if r:
            if r.status_code == 200 or r.status_code == 201:
                self.receive_text = r.content
            else:
                self.receive_text = r.status_code
                self.msg = 'Failure: web_addr ' + self.web_addr + " port " + self.port + " retcode: %d" % r.status_code
        else:
            self.receive_text = None
            self.msg = "Endpoint not found"

        return self.receive_text

    def get_cmd(self, command, update_cmd="", write_down=False):
        """
        GET请求
        """
        ret = self._rest_cmd("GET", command, update_cmd)
        if write_down and ret:
            with open(r"C:\Users\Administrator\Desktop\lookup.xml", "w") as f:
                f.write(ret.decode("utf-8") or "")
        try:
            return etree.XML(ret)
        except Exception as e:
            self.msg = "接收信息并非XML格式数据"
            print(self.msg, e, ret)
            return None

    def post_cmd(self, command, update_cmd=""):
        """
        POST请求
        """
        ret = self._rest_cmd("POST", command, update_cmd)
        try:
            resp_root = etree.XML(ret)
            resp_ele = resp_root.findall(".//response")
            error_code = ""
            for node in resp_ele:
                error_code = node.attrib["errorCode"]
            if error_code == "0":
                self.msg = "Set successfully"
                return ret
            else:
                try:
                    err_string = node.attrib["errorString"]
                    self.msg = "PostCmd:" + command + "ErrCode: " + error_code + "ErrString:" + err_string
                except:
                    self.msg = "post command:" + command + " Error Code: " + error_code + " receive text is " + self.receive_text
                    pass
            return None
        except:
            self.msg = "receive string is not XML format:" + self.receive_text
            return None

    def del_cmd(self, command, update_cmd=""):
        # DELETE <webservice>/Backupset/{backupsetId}
        ret = self._rest_cmd("DELETE", command, update_cmd)
        try:
            resp_root = etree.XML(ret)
            resp_ele = resp_root.findall(".//response")
            error_code = ""
            for node in resp_ele:
                error_code = node.attrib["errorCode"]
            if error_code == "0":
                self.msg = "Set successfully"
                return True
            self.msg = "del command:" + command + " xml format:" + update_cmd + " Error Code: " + error_code + " receive text is " + self.receive_text
            return False
        except:
            self.msg = "receive string is not XML format:" + self.receive_text
            return False

    def put_cmd(self, command, update_cmd=""):
        # PUT <webservice>/Backupset/{backupsetId}
        ret = self._rest_cmd("PUT", command, update_cmd)
        try:
            resp_root = etree.XML(ret)
            resp_ele = resp_root.findall(".//response")
            error_code = ""
            for node in resp_ele:
                error_code = node.attrib["errorCode"]
            if error_code == "0":
                self.msg = "Set successfully"
                return ret
            self.msg = "del command:" + command + " xml format:" + update_cmd + " Error Code: " + error_code + " receive text is " + self.receive_text
            return None
        except:
            self.msg = "receive string is not XML format:" + self.receive_text
            return None

    def q_cmd(self, command, update_cmd=""):
        """
        Constructor
        get command function
        """
        ret = self._rest_cmd("QCMD", command, update_cmd)
        try:
            resp_root = etree.XML(ret)
            resp_job = resp_root.findall(".//jobIds")
            for node in resp_job:
                return True
            resp_ele = resp_root.findall(".//response")
            error_code = ""
            for node in resp_ele:
                error_code = node.attrib["errorCode"]
            if error_code == "0":
                self.msg = "Set successfully"
                return True
            else:
                try:
                    err_string = node.attrib["errorString"]
                    self.msg = "qcmd command:" + command + " Error Code: " + error_code + " ErrString: " + err_string
                except:
                    self.msg = "qcmd command:" + command + " Error Code: " + error_code + " receive text is " + self.receive_text
                    pass
            return False
        except:
            # traceback.print_exc()
            return ret


class CVApiOperate(CVRestApiCmd):
    """
    CV 操作接口
        设置
        查询
        删除
    """

    def __init__(self, token):
        super().__init__(token)
        self.sp_list = []
        self.client_list = []
        self.job_list = []
        self.platform = {"platform": None, "ProcessorType": 0, "hostName": None}
        self.client_info = {"clientName": None, "clientId": None, "platform": self.platform, "backupsetList": [],
                            "agentList": []}
        self.sub_client_list = []
        self.agent_list = []
        self.instance_list = []
        self.is_new_client = True
        self._sub_client_list = []
        self.lock = threading.Lock()

        # 线程池
        self.pool = ThreadPoolExecutor(max_workers=10)

    def get_console_alert_list(self):
        """
        控制台告警列表
        :return:
        """
        alert_list = []
        alert_rule = self.get_cmd("Alert?pageNo=1&pageCount=200")
        if alert_rule is None:
            return None

        active_physical_node = alert_rule.xpath("//feedsList")
        for feeds_list in active_physical_node:
            alert_info = feeds_list.attrib
            alert_time = feeds_list.xpath("./detectedTime")[0].attrib
            alert_client = feeds_list.xpath("./client")[0].attrib
            alert_list.append(dict(alert_info.items() + alert_time.items() + alert_client.items()))
        return alert_list

    def get_sp_list(self):
        """
        获取所有存储策略
        :return:
        """
        sp_list = []
        storage_policy = self.get_cmd("StoragePolicy")
        if storage_policy is None:
            return None
        active_physical_node = storage_policy.findall(".//policies")
        for node in active_physical_node:
            if node.attrib["storagePolicyId"] <= "2":
                continue
            if "System Create" in node.attrib["storagePolicyName"]:
                continue
            sp_list.append(node.attrib)
        return sp_list

    def get_sp_from_sub_client(self, sub_client_id):
        """
        获取子客户端关联存储策略
        :param sub_client_id:
        :return:
        """
        if sub_client_id is None:
            return None
        command = "Subclient/{0}".format(sub_client_id)
        resp = self.get_cmd(command)
        storage_policys = resp.xpath("//dataBackupStoragePolicy")
        storage_policy_list = []
        for storage_policy in storage_policys:
            storage_policy_list.append(storage_policy.attrib)
        return storage_policy_list

    def get_sp_info(self, sp_id):
        if sp_id is None:
            return None
        sp_info_list = []
        command = "StoragePolicy/{0}?propertyLevel=10".format(sp_id)
        resp = self.get_cmd(command)
        if resp is None:
            return None
        active_physical_node = resp.findall(".//StoragePolicyCopy")
        for node in active_physical_node:
            sp_info_list.append(node.attrib)
        return sp_info_list

    def get_copy_from_sp(self, sp_id, copy_id):
        command = "V2/StoragePolicy/{0}/Copy/{1}".format(sp_id, copy_id)
        resp = self.get_cmd(command)
        # if resp is None:
        #     return None

    def get_schedule_policy_list(self):
        """
        获取所有计划策略
        :return:
        """
        schedule_policy_list = []
        schedule_policy = self.get_cmd('SchedulePolicy')
        if schedule_policy is None:
            return None
        schedule_tasks = schedule_policy.xpath("//taskDetail/task")

        if schedule_tasks:
            for schedule_task in schedule_tasks:
                taskIds = schedule_task.xpath("./@taskId")
                if taskIds:
                    taskId = taskIds[0]
                else:
                    taskId = ""
                taskNames = schedule_task.xpath("./@taskName")
                if taskNames:
                    taskName = taskNames[0]
                else:
                    taskName = ""
                schedule_policy_list.append({
                    "taskId": taskId,
                    "taskName": taskName,
                })

        return schedule_policy_list

    def get_schedule_list(self, client_id):
        schduleList = []
        cmd = "Schedules?clientId={0}".format(client_id)
        schedules = self.get_cmd(cmd)

        taskDetails = schedules.xpath("//taskDetail")
        if taskDetails:
            taskDetail = taskDetails[0]
            # 策略名称
            taskIds = taskDetail.xpath("./task/@taskId")
            if taskIds:
                taskId = taskIds[0]
            else:
                taskId = ""
            taskNames = taskDetail.xpath("./task/@taskName")
            if taskNames:
                taskName = taskNames[0]
            else:
                taskName = ""
            # backset_name/app_name
            backupsetNames = taskDetail.xpath("./associations/@backupsetName")
            appNames = taskDetail.xpath("./associations/@appName")
            subclientNames = taskDetail.xpath("./associations/@subclientName")
            instanceNames = taskDetail.xpath("./associations/@instanceName")
            if backupsetNames:
                backupsetName = backupsetNames[0]
            else:
                backupsetName = ""
            if appNames:
                appName = appNames[0]
            else:
                appName = ""
            if subclientNames:
                subclientName = subclientNames[0]
            else:
                subclientName = ""
            if instanceNames:
                instanceName = instanceNames[0]
            else:
                instanceName = ""
            subTasks = taskDetail.xpath("./subTasks")
            for subTask in subTasks:
                # backupOpts(备份模式),pattern(计划模式)
                backupOpts = subTask.xpath("./options/backupOpts")
                for backupOpt in backupOpts:
                    backupLevels = backupOpt.xpath("./@backupLevel")
                    if backupLevels:
                        backupLevel = backupLevels[0]
                    else:
                        backupLevel = ""

                    incLevels = backupOpt.xpath("./@incLevel")
                    if incLevels:
                        incLevel = incLevels[0]
                    else:
                        incLevel = ""
                patterns = subTask.xpath("./pattern")
                for pattern in patterns:
                    descriptions = pattern.xpath("./@description")
                    if descriptions:
                        description = descriptions[0]
                    else:
                        description = ""

                schduleList.append({
                    "taskId": taskId,
                    "taskName": taskName,
                    "backupLevel": backupLevel,
                    "incLevels": incLevel,
                    "description": description,
                    "backupsetName": backupsetName,
                    "appName": appName,
                    "subclientName": subclientName,
                    "instanceName": instanceName,
                })
        return schduleList

    def get_schedule_policy_info(self, task_id):
        get_schedule_policy_info_list = []
        cmd = "SchedulePolicy/{0}".format(task_id)
        schedule_info = self.get_cmd(cmd)
        # taskInfo/associations  taskInfo/subTasks/options/backupOpts taskInfo/subTasks/pattern
        taskInfo = schedule_info.xpath("//taskInfo")
        if taskInfo:
            taskInfo = taskInfo[0]
            # backset_name/app_name
            clientNames = taskInfo.xpath("./associations/@clientName")
            backupsetNames = taskInfo.xpath("./associations/@backupsetName")
            appNames = taskInfo.xpath("./associations/@appName")
            subclientNames = taskInfo.xpath("./associations/@subclientName")
            taskNames = taskInfo.xpath("./task/@taskName")
            instanceNames = taskInfo.xpath("./associations/@instanceName")
            if clientNames:
                clientName = clientNames[0]
            else:
                clientName = ""
            if backupsetNames:
                backupsetName = backupsetNames[0]
            else:
                backupsetName = ""
            if appNames:
                appName = appNames[0]
            else:
                appName = ""
            if subclientNames:
                subclientName = subclientNames[0]
            else:
                subclientName = ""
            if taskNames:
                taskName = taskNames[0]
            else:
                taskName = ""
            if instanceNames:
                instanceName = instanceNames[0]
            else:
                instanceName = ""
            subTasks = taskInfo.xpath("./subTasks")
            for num, subTask in enumerate(subTasks):
                if num == 0:
                    first_schedule = 1
                else:
                    first_schedule = 0
                # backupOpts(备份模式),pattern(计划模式)
                backupOpts = subTask.xpath("./options/backupOpts")
                for backupOpt in backupOpts:
                    backupLevels = backupOpt.xpath("./@backupLevel")
                    if backupLevels:
                        backupLevel = backupLevels[0]
                    else:
                        backupLevel = ""

                    incLevels = backupOpt.xpath("./@incLevel")
                    if incLevels:
                        incLevel = incLevels[0]
                    else:
                        incLevel = ""
                patterns = subTask.xpath("./pattern")
                for pattern in patterns:
                    descriptions = pattern.xpath("./@description")
                    if descriptions:
                        description = descriptions[0]
                    else:
                        description = ""
                if subclientName:
                    get_schedule_policy_info_list.append({
                        "first_schedule": first_schedule,
                        "schedule_count": len(subTasks),
                        "backupLevel": backupLevel,
                        "incLevels": incLevel,
                        "description": description,
                        "backupsetName": backupsetName if appName in ["File System", "Virtual Server"] else instanceName,
                        "appName": appName,
                        "subclientName": subclientName,
                        "clientName": clientName,
                        "taskName": taskName,
                    })

        return get_schedule_policy_info_list

    def get_client_list(self):
        """
        获取客户端列表
        :return:
        """
        client_list = []
        client_rec = {"clientName": None, "clientId": -1}
        client = self.get_cmd('Client')
        if client is None:
            return None
        active_physical_node = client.findall(".//clientEntity")
        for node in active_physical_node:
            rec = copy.deepcopy(client_rec)
            rec["clientName"] = node.attrib["clientName"]
            try:
                rec["clientId"] = int(node.attrib["clientId"])
            except Exception as e:
                print("get_client_list", e)
            client_list.append(rec)
        return client_list

    def get_job_list(self, client_id, job_type="", app_type_name=None, backup_set_name=None, sub_client_name=None, time_sorted=False, period=604800):
        """
        Running
        Waiting
        Pending
        Suspend
        Kill Pending
        Interrupt Pending
        Interrupted
        QueuedCompleted
        Completed w/ one or more errors
        Completed w/ one or more warnings
        Committed
        Failed
        Failed to Start
        Killed
        """
        job_list = []
        status_list = {"Running": "运行", "Waiting": "等待", "Pending": "阻塞", "Suspend": "终止", "Completed": "正常",
                       "Failed": "失败", "Failed to Start": "启动失败", "Killed": "杀掉",
                       "Completed w/ one or more errors": "已完成，但有一个或多个错误",
                       "Completed w/ one or more warnings": "已完成，但有一个或多个警告"}
        cmd = """Job?clientId={client_id}&limit={limit}&offset={offset}&completedJobLookupTime={completedJobLookupTime}&jobFilter={job_type}""".format(
            **{
                "client_id": client_id,
                "limit": 100,
                "offset": 0,
                "completedJobLookupTime": period,  # 最近1周作业(s)
                "job_type": job_type,
            })
        # cmd = "/Job?clientId=3&completedJobLookupTime=604800&jobFilter="
        resp = self.get_cmd(cmd)

        if resp is None:
            return None
        active_physical_node = resp.findall(".//jobs/jobSummary")
        for node in active_physical_node:
            if app_type_name:
                if app_type_name not in node.attrib["appTypeName"]:
                    continue
            if backup_set_name:
                if backup_set_name not in node.attrib["backupSetName"]:
                    continue
            if sub_client_name:
                if sub_client_name not in node.attrib["subclientName"]:
                    continue

            status = node.attrib["status"]
            try:
                node.attrib["status"] = status_list[status]
            except KeyError as e:
                print("get_job_list", e)
                node.attrib["status"] = status
            job_list.append({
                "jobId": node.attrib["jobId"],
                "client": node.attrib["destClientName"],
                "status": node.attrib["status"],
                "agentType": node.attrib["appTypeName"],
                "backupSetName": node.attrib["backupSetName"],
                "jobType": node.attrib["jobType"],
                "Level": node.attrib["backupLevel"],
                "appSize": node.attrib["sizeOfApplication"],
                "diskSize": node.attrib["sizeOfMediaOnDisk"],
                "StartTime": node.attrib["jobStartTime"],
                "LastTime": node.attrib["lastUpdateTime"],
            })
        if time_sorted:
            job_list = sorted(job_list, key=operator.itemgetter("StartTime"))
        return job_list

    def get_job_info(self, job_id):
        if job_id is None:
            return None
        job_info_list = []
        command = "/Job/{0}".format(job_id)
        resp = self.get_cmd(command)
        if resp is None:
            return None
        active_physical_node = resp.findall(".//jobs/jobSummary")
        for node in active_physical_node:
            job_info_list.append(node.attrib)
        return job_info_list

    def get_client(self, client):
        """
        判断客户端是否存在
        :param client:
        :return:
        """
        client_info = self.client_info
        if isinstance(client, int):
            command = "Client/{0}".format(str(client))
            resp = self.get_cmd(command)
            if resp is None:
                return False
            client_entity = resp.findall(".//clientEntity")
            if not client_entity:
                return False
            # versionInfo,GalaxyRelease
            version_info = resp.findall(".//versionInfo")
            galaxy_release = resp.findall(".//GalaxyRelease")

            client_info["clientId"] = client_entity[0].attrib["clientId"]
            client_info["clientName"] = client_entity[0].attrib["clientName"]
            client_info["versionInfo"] = version_info[0].attrib["version"]
            client_info["GalaxyRelease"] = galaxy_release[0].attrib["ReleaseString"]
        else:
            command = "GetId?clientName={0}".format(client)
            resp = self.get_cmd(command)
            if resp is None:
                return False

            client_info["clientId"] = resp.attrib["clientId"]
            if int(client_info["clientId"]) <= 0:
                return False
            client_info["clientName"] = resp.attrib["clientName"]
        return True

    def get_sub_client_list(self, client_id):
        """
        获取子客户端列表
        :param client_id:
        :return:
        """
        if client_id is None:
            return None
        sub_client_list = []
        cmd = 'Subclient?clientId={0}'.format(client_id)
        sub_client = self.get_cmd(cmd)
        if sub_client is None:
            return None
        active_physical_node = sub_client.findall(".//subClientEntity")
        for node in active_physical_node:
            sub_client_list.append(node.attrib)
        return sub_client_list

    def get_simple_sub_client_info(self, sub_client_id):
        try:
            sub_client_id = int(sub_client_id)
        except Exception as e:
            print(e)
            return None
        else:
            sub_client_info = {}
            command = "Subclient/{0}".format(sub_client_id)
            resp = self.get_cmd(command)
            subClientEntity = resp.findall(".//subClientEntity")
            if subClientEntity:
                # 子客户端名称
                sub_client_info["subclientName"] = subClientEntity[0].get("subclientName", "")
                sub_client_info["subclientId"] = subClientEntity[0].get("subclientId", "")
                sub_client_info["backupsetId"] = subClientEntity[0].get("backupsetId", "")
                sub_client_info["backupsetName"] = subClientEntity[0].get("backupsetName", "")
                sub_client_info["instanceId"] = subClientEntity[0].get("instanceId", "")
                sub_client_info["instanceName"] = subClientEntity[0].get("instanceName", "")
                sub_client_info["applicationId"] = subClientEntity[0].get("applicationId", "")
                sub_client_info["appName"] = subClientEntity[0].get("appName", "")
                sub_client_info["clientId"] = subClientEntity[0].get("clientId", "")
                sub_client_info["clientName"] = subClientEntity[0].get("clientName", "")

            # dataBackupStoragePolicy
            dataBackupStoragePolicy = resp.findall(".//dataBackupStoragePolicy")
            if dataBackupStoragePolicy:
                sub_client_info["storagePolicyId"] = dataBackupStoragePolicy[0].get("storagePolicyId", "")
                sub_client_info["storagePolicyName"] = dataBackupStoragePolicy[0].get("storagePolicyName", "")
            return sub_client_info

    def get_backup_content(self, sub_client_id):
        bacukup_content = {}
        my_content = []

        if sub_client_id is None:
            return None
        command = "Subclient/{0}".format(sub_client_id)
        resp = self.get_cmd(command)

        subClientEntity = resp.findall(".//subClientEntity")
        # 子客户端名称
        bacukup_content["subclientName"] = subClientEntity[0].get("subclientName", "")

        # 应用名
        bacukup_content["appName"] = subClientEntity[0].get("appName", "")
        # 备份集
        bacukup_content["backupsetName"] = subClientEntity[0].get("backupsetName", "")
        if bacukup_content["appName"] == "File System":
            # content
            contentlist = resp.findall(".//content")
            for content in contentlist:
                my_content.append(content.get("path", ""))
            bacukup_content["content"] = my_content
        # 数据库实例信息
        if bacukup_content["appName"] == "SQL Server":
            command = "/instance?clientId={0}".format(subClientEntity[0].get("clientId", ""))
            resp = self.get_cmd(command)
            instancenodes = resp.findall(".//instanceProperties")
            for instancenode in instancenodes:
                instance = instancenode.findall(".//instance")
                if instance[0].get("instanceId", "") == subClientEntity[0].get("instanceId", ""):
                    bacukup_content["instanceName"] = instance[0].get("instanceName", "")
                    bacukup_content["content"] = [instance[0].get("instanceName", "")]
                    break
        if bacukup_content["appName"] == "Oracle":
            command = "instance?clientId={0}".format(subClientEntity[0].get("clientId", ""))
            resp = self.get_cmd(command)
            instancenodes = resp.findall(".//instanceProperties")
            for instancenode in instancenodes:
                instance = instancenode.findall(".//instance")
                if instance[0].get("instanceId", "") == subClientEntity[0].get("instanceId", ""):
                    bacukup_content["instanceName"] = instance[0].get("instanceName", "")
                    bacukup_content["content"] = [instance[0].get("instanceName", "")]
                    break
        if bacukup_content["appName"] == "Virtual Server":
            children = resp.findall(".//vmContent/children")
            for child in children:
                my_content.append(child.get("displayName", ""))
            bacukup_content["content"] = my_content
            bacukup_content["backupsetName"] = subClientEntity[0].get("backupsetName", "")
        if bacukup_content["appName"] == "MySQL":
            contents = resp.xpath("//content/mySQLContent")
            db_list = []
            if contents:
                for content in contents:
                    db_names = content.xpath("./@databaseName")
                    if db_names:
                        db_list.append(db_names[0])
            bacukup_content["content"] = db_list

        return bacukup_content

    def get_sub_client_info(self, sub_client_id):
        """
        获取子客户端信息
        :param sub_client_id:
        :return:
        """
        backup_info = {}
        my_content = []
        if sub_client_id is None:
            return None
        command = "Subclient/{0}".format(sub_client_id)
        resp = self.get_cmd(command)
        try:
            subClientEntity = resp.findall(".//subClientEntity")
            # 子客户端名称
            backup_info["sub_client_name"] = subClientEntity[0].get("subclientName", "")

            # 应用名
            backup_info["appName"] = subClientEntity[0].get("appName", "")
            # 存储策略
            dataBackupStoragePolicy = resp.findall(".//dataBackupStoragePolicy")

            # 存储策略具体内容
            storagePolicyId = dataBackupStoragePolicy[0].get("storagePolicyId", "")
            storage_policy_cmd = "/StoragePolicy/{0}?propertyLevel=10".format(storagePolicyId)
            storage_policy_xml = self.get_cmd(storage_policy_cmd)
            storage_policy_copy = storage_policy_xml.findall(
                ".//StoragePolicyCopy") if storage_policy_xml is not None else []
            storage_library = storage_policy_xml.findall(".//library") if storage_policy_xml is not None else []
            storage_drive_pool = storage_policy_xml.findall(".//drivePool") if storage_policy_xml is not None else []
            storage_retention_rules = storage_policy_xml.findall(
                ".//retentionRules") if storage_policy_xml is not None else []

            backup_info["storage_info"] = {
                "storage_id": dataBackupStoragePolicy[0].get("storagePolicyId", ""),
                "storage_name": dataBackupStoragePolicy[0].get("storagePolicyName", ""),
                "storage_policy_copy": dict(storage_policy_copy[0].items()) if storage_policy_copy else "",
                "storage_library": dict(storage_library[0].items()) if storage_library else "",
                "storage_drive_pool": dict(storage_drive_pool[0].items()) if storage_drive_pool else "",
                "storage_retention_rules": dict(storage_retention_rules[0].items()) if storage_retention_rules else "",
            }
            # 计划策略
            schduleList = []
            cmd = "Schedules?subclientId={0}".format(sub_client_id)
            client = self.get_cmd(cmd)
            try:
                activePhysicalNode = client.findall(".//task")
                for node in activePhysicalNode:
                    schduleList.append(node.attrib)
            except Exception as e:
                self.msg = "未获取到任务"
                print(self.msg, e)
            schedule_policy_list = []
            for schedule in schduleList:
                task_id = schedule["taskId"] if schduleList else ""

                # 计划策略具体内容
                cmd_get_schedule_name = "SchedulePolicy/{0}".format(task_id)
                content = self.get_cmd(cmd_get_schedule_name)
                schedule_info = content.findall(".//pattern") if content is not None else []
                if schedule_info:
                    schedule_info = schedule_info[0]
                    schedule_policy_dict = dict(schedule_info.items())
                    schedule_policy_dict["schdule_name"] = schduleList[0]["taskName"] if schduleList else ""

                    schedule_policy_list.append(schedule_policy_dict)
            backup_info["schedule_info"] = schedule_policy_list

            # 客户端备份内容
            # 文件备份集信息
            if backup_info["appName"] == "File System":
                # content
                contentlist = resp.findall(".//content")
                for content in contentlist:
                    my_content.append(content.get("path", ""))
                backup_info["content"] = my_content
                # backupSystemState
                fsSubClientProp = resp.findall(".//fsSubClientProp")
                backup_info["backupSystemState"] = fsSubClientProp[0].get("backupSystemState", "")
                if backup_info["backupSystemState"] == "0" or backup_info["backupSystemState"] == "false":
                    backup_info["backupSystemState"] = "FALSE"
                if backup_info["backupSystemState"] == "1" or backup_info["backupSystemState"] == "true":
                    backup_info["backupSystemState"] = "TRUE"
            # 数据库实例信息
            if backup_info["appName"] == "SQL Server":
                command = "/instance?clientId={0}".format(subClientEntity[0].get("clientId", ""))
                resp = self.get_cmd(command)
                instancenodes = resp.findall(".//instanceProperties")
                for instancenode in instancenodes:
                    instance = instancenode.findall(".//instance")

                    if instance[0].get("instanceId", "") == subClientEntity[0].get("instanceId", ""):
                        backup_info["instanceName"] = instance[0].get("instanceName", "")
                        mssqlInstance = instancenode.findall(".//mssqlInstance")
                        backup_info["vss"] = mssqlInstance[0].get("useVss", "")
                        if backup_info["vss"] == "0" or backup_info["vss"] == "false":
                            backup_info["vss"] = "FALSE"
                        if backup_info["vss"] == "1" or backup_info["vss"] == "true":
                            backup_info["vss"] = "TRUE"

                        # iscover
                        iscover = instancenode.findall(".//mssqlInstance/overrideHigherLevelSettings")
                        if iscover:
                            iscover = iscover[0]
                            backup_info["iscover"] = iscover.get("overrideGlobalAuthentication", "")
                        else:
                            backup_info["iscover"] = ""

                        if backup_info["iscover"] == "0" or backup_info["iscover"] == "false":
                            backup_info["iscover"] = "FALSE"
                        if backup_info["iscover"] == "1" or backup_info["iscover"] == "true":
                            backup_info["iscover"] = "TRUE"
                        # user:<userAccount/>
                        userAccount = instancenode.findall(".//mssqlInstance/overrideHigherLevelSettings/userAccount")
                        if userAccount:
                            backup_info["userName"] = userAccount[0].get("userName", "")
                        else:
                            backup_info["userName"] = ""
                        break
            if backup_info["appName"] == "Oracle":
                command = "/instance?clientId={0}".format(subClientEntity[0].get("clientId", ""))
                resp = self.get_cmd(command)
                instancenodes = resp.findall(".//instanceProperties")
                for instancenode in instancenodes:
                    instance = instancenode.findall(".//instance")
                    if instance[0].get("instanceId", "") == subClientEntity[0].get("instanceId", ""):
                        backup_info["instanceName"] = instance[0].get("instanceName", "")
                        oracleInstance = instancenode.findall(".//oracleInstance")
                        backup_info["oracleHome"] = oracleInstance[0].get("oracleHome", "")
                        oracleUser = instancenode.findall(".//oracleInstance/oracleUser")
                        backup_info["oracleUser"] = oracleUser[0].get("userName", "")
                        # connect
                        sqlConnect = instancenode.findall(".//oracleInstance/sqlConnect")
                        backup_info["conn1"] = sqlConnect[0].get("userName", "")
                        backup_info["conn2"] = ""  # sys密码，没有
                        backup_info["conn3"] = sqlConnect[0].get("domainName", "")
                        break
            if backup_info["appName"] == "Virtual Server":
                children = resp.findall(".//vmContent/children")
                for child in children:
                    my_content.append(child.get("displayName", ""))
                backup_info["content"] = my_content
                backup_info["backupsetName"] = subClientEntity[0].get("backupsetName", "")
        except Exception as e:
            self.msg = "获取客户端实例失败"
            print(self.msg, e)
        return backup_info

    def get_vm_backup_content(self, sub_client_id):
        my_content = []
        if sub_client_id is None:
            return None
        command = "Subclient/{0}".format(sub_client_id)
        resp = self.get_cmd(command)
        children = resp.findall(".//vmContent/children")
        for child in children:
            my_content.append(child.get("displayName", ""))
        return my_content

    def get_backup_set_list(self, client_id):
        """
        备份集列表
        :param client_id:
        :return:
        """
        # {'backupsetName': 'defaultBackupSet', 'appName': 'Windows File System', 'instanceId': '1',
        # 'instanceName': 'DefaultInstanceName', '_type_': '6', 'clientId': '3', 'backupsetId': '5',
        # 'clientName': 'win-2qls3b7jx3v.hzx', 'applicationId': '33'}
        if client_id is None:
            return None
        backup_set_list = []
        cmd = 'Backupset?clientId={0}'.format(client_id)
        sub_client = self.get_cmd(cmd)
        if sub_client is None:
            return None
        active_physical_node = sub_client.findall(".//backupSetEntity")
        for node in active_physical_node:
            backup_set_list.append(node.attrib)
        return backup_set_list

    def get_backup_set_info(self, backup_set_id):
        """
        备份集具体信息
        :param backup_set_id:
        :return:
        """
        pass
        # try:
        #     backup_set_id = int(backup_set_id)
        # except Exception as e:
        #     print(e)
        #     return None
        # else:
        #     backup_set_info = {}
        #     cmd = 'Backupset/{0}'.format(backup_set_id)
        #     backup_set = self.get_cmd(cmd)
        #     return backup_set

    def get_client_os_info(self, client_id):
        """
        获取客户端操作系统
        :param client_id:
        :return:
        """
        if client_id is None:
            return None
        command = "Client/{0}".format(client_id)
        resp = self.get_cmd(command)

        try:
            os_info = resp.findall(".//OsDisplayInfo")
            self.platform["platform"] = os_info[0].attrib["OSName"]
            self.platform["ProcessorType"] = os_info[0].attrib["ProcessorType"]

            host_names = resp.findall(".//clientEntity")
            self.platform["hostName"] = host_names[0].attrib["hostName"]
        except Exception as e:
            self.msg = "获取客户端平台失败"
            print(self.msg, e)

    def get_client_instance(self, client_id):
        """
        获取数据库/虚机实例
        :param client_id:
        :return:
        """
        # instance = {}
        # my_proxy_list = []
        if client_id is None:
            return None
        command = "/instance?clientId={0}".format(client_id)
        instance = self.get_cmd(command)

        # try:
        #     vc_info = resp.findall(".//vmwareVendor/virtualCenter")
        #     instance["HOST"] = vc_info[0].attrib["domainName"]
        #     instance["USER"] = vc_info[0].attrib["userName"]
        #
        #     proxy_list = resp.findall(".//memberServers/client")
        #     for proxy in proxy_list:
        #         my_proxy_list.append({"clientId": proxy.attrib["clientId"], "clientName": proxy.attrib["clientName"]})
        #     instance["PROXYLIST"] = my_proxy_list
        # except Exception as e:
        #     self.msg = "获取客户端实例失败"
        #     print(self.msg, e)
        if instance is None:
            return None
        active_physical_node = instance.findall(".//instance")
        for node in active_physical_node:
            self.instance_list.append(node.attrib)
        return self.instance_list

    def get_client_agent_list(self, client_id):
        """
        获取客户端模块
        :param client_id:
        :return:
        """
        agent_list = []
        agent = {}
        if client_id is None:
            return None
        command = "Agent?clientId={0}".format(client_id)
        resp = self.get_cmd(command)
        try:
            active_physical_node = resp.findall(".//idaEntity")
            for node in active_physical_node:
                agent["clientName"] = node.attrib["clientName"]
                agent["agentType"] = node.attrib["appName"]
                agent["appId"] = node.attrib["applicationId"]
                agent_list.append(copy.deepcopy(agent))
        except Exception as e:
            self.msg = "error get agent type"
            print(self.msg, e)
        # self.agent_list = agent_list
        return agent_list

    def get_client_info(self, client):
        """
        获取客户端信息
        :param client:
        :return:
        """
        self.is_new_client = True

        if self.token is None or client is None:
            return None
        # get client
        if self.get_client(client) is False:
            return None
        client_info = self.client_info
        # 客户端安装时间
        self.is_new_client = False
        # get backupsetList
        client_info["backupsetList"] = self.get_backup_set_list(client_info["clientId"])
        # get platform
        self.get_client_os_info(client_info["clientId"])
        # get agent list
        client_info["agentList"] = self.get_client_agent_list(client_info["clientId"])
        if (client_info["platform"]["platform"]).upper() == "ANY":
            client_info["instance"] = self.get_client_instance(client_info["clientId"])
        return client_info

    def get_client_info_by_id(self, client_id):
        client_info = {}
        if isinstance(client_id, int):
            command = "Client/{0}".format(str(client_id))
            resp = self.get_cmd(command)
            if resp is None:
                return None
            client_entity = resp.findall(".//clientEntity")
            if not client_entity:
                return None
            # versionInfo,GalaxyRelease
            version_info = resp.findall(".//versionInfo")
            galaxy_release = resp.findall(".//GalaxyRelease")
            os_info = resp.findall(".//OsDisplayInfo")
            try:
                client_info["os_info"] = os_info[0].attrib["OSName"]
                client_info["clientId"] = client_entity[0].attrib["clientId"]
                client_info["clientName"] = client_entity[0].attrib["clientName"]
                client_info["commCellName"] = client_entity[0].attrib["commCellName"]
                client_info["versionInfo"] = version_info[0].attrib["version"]
                client_info["GalaxyRelease"] = galaxy_release[0].attrib["ReleaseString"]
            except:
                return None
            return client_info
        else:
            return None

    def get_client_info_by_name(self, client_name):
        if isinstance(client_name, str):
            command = "GetId?clientName={0}".format(client_name)
            resp = self.get_cmd(command)
            if resp is None:
                return None

            client_id = resp.attrib["clientId"]
            try:
                client_id = int(client_id)
            except:
                return False
            if client_id <= 0:
                return False
            client_info = self.get_client_info_by_id(client_id)
            return client_info
        else:
            return None

    def get_is_new_client(self):
        return self.is_new_client

    def custom_backup_tree_by_client(self, client):
        """
        根据client_id获取所有备份信息：
        :return: backup_info_by_client
        """
        # 多线程
        t1 = threading.Thread(target=self.get_client_agent_list, args=(client,))
        t2 = threading.Thread(target=self.get_backup_set_list, args=(client,))
        t3 = threading.Thread(target=self.get_sub_client_list, args=(client,))
        t4 = threading.Thread(target=self.get_client_instance, args=(client,))

        t1.start()
        t2.start()
        t3.start()
        t4.start()

        t1.join()
        t2.join()
        t3.join()
        t4.join()

        c_agent_list = self.agent_list
        c_backup_set_list = self.backup_set_list
        c_sub_client_list = self.sub_client_list
        c_instance_list = self.instance_list

        backup_tree = {}
        agent_list = []

        for agent in c_agent_list:
            agent_info = {}
            agent_type = agent["agentType"]
            backup_set_list = []
            instance_list = []
            # 文件系统备份集
            if agent_type == "File System":
                for backup_set in c_backup_set_list:
                    # 两个接口获取的appName样式略有不同：SQL Server >> Oracle Database，Oracle >> Oracle Database
                    if agent_type in backup_set["appName"]:
                        backup_set_info = dict()
                        backup_set_info["back_up_set_id"] = backup_set["backupsetId"]
                        backup_set_info["back_up_set_name"] = backup_set["backupsetName"]

                        c_ts_backup = []
                        for num, sub_client in enumerate(c_sub_client_list):
                            # backup_set_id相同
                            temp_lock = threading.Lock()
                            if backup_set_info["back_up_set_id"] == sub_client["backupsetId"]:
                                # 多线程
                                c_t = threading.Thread(target=self._get_sub_client_list, args=(sub_client, temp_lock))
                                c_t.start()
                                c_ts_backup.append(c_t)

                        for i in c_ts_backup:
                            i.join()

                        cp_list = copy.deepcopy(self._sub_client_list)
                        backup_set_info["sub_client_list"] = cp_list
                        backup_set_list.append(backup_set_info)
                        self._sub_client_list.clear()
            # 虚机>实例>备份集>子客户端
            elif agent_type == "Virtual Server":
                for instance in c_instance_list:
                    if agent_type in instance["appName"]:
                        virtual_backup_set_list = list()
                        instance_info = dict()
                        instance_info["instance_id"] = instance["instanceId"]
                        instance_info["instance_name"] = instance["instanceName"]
                        for backup_set in c_backup_set_list:
                            # 两个接口获取的appName样式略有不同：SQL Server >> Oracle Database，Oracle >> Oracle Database
                            if agent_type in backup_set["appName"]:
                                backup_set_info = dict()
                                backup_set_info["back_up_set_id"] = backup_set["backupsetId"]
                                backup_set_info["back_up_set_name"] = backup_set["backupsetName"]
                                c_ts_virtual = []
                                for num, sub_client in enumerate(c_sub_client_list):
                                    # backup_set_id相同
                                    temp_lock = threading.Lock()
                                    if backup_set_info["back_up_set_id"] == sub_client["backupsetId"] and instance_info[
                                        "instance_id"] == sub_client["instanceId"]:
                                        # 多线程
                                        c_t = threading.Thread(target=self._get_sub_client_list,
                                                               args=(sub_client, temp_lock))
                                        c_t.start()
                                        c_ts_virtual.append(c_t)

                                for i in c_ts_virtual:
                                    i.join()

                                cp_list = copy.deepcopy(self._sub_client_list)
                                backup_set_info["sub_client_list"] = cp_list
                                virtual_backup_set_list.append(backup_set_info)
                                self._sub_client_list.clear()
                        instance_info["backup_set_list"] = virtual_backup_set_list
                        instance_list.append(instance_info)
            # 数据库实例
            else:
                for instance in c_instance_list:
                    # print(agent_type, instance["appName"])
                    if agent_type in instance["appName"]:
                        instance_info = dict()
                        instance_info["instance_id"] = instance["instanceId"]
                        instance_info["instance_name"] = instance["instanceName"]

                        c_ts_instance = []
                        for num, sub_client in enumerate(c_sub_client_list):
                            # instance_id相同
                            temp_lock = threading.Lock()
                            if instance_info["instance_id"] == sub_client["instanceId"]:
                                # 多线程
                                c_t = threading.Thread(target=self._get_sub_client_list, args=(sub_client, temp_lock))
                                c_t.start()
                                c_ts_instance.append(c_t)

                        for i in c_ts_instance:
                            i.join()
                        cp_list = copy.deepcopy(self._sub_client_list)
                        instance_info["sub_client_list"] = cp_list
                        instance_list.append(instance_info)
                        self._sub_client_list.clear()

            agent_info["agent_type"] = agent_type
            if backup_set_list:
                agent_info["backup_set_list"] = backup_set_list
            if instance_list:
                agent_info["instance_list"] = instance_list
            agent_list.append(agent_info)
        backup_tree["agent_list"] = agent_list
        return backup_tree

    def _get_sub_client_list(self, sub_client, temp_lock):
        """
        获取子客户端信息线程任务
        :param sub_client:
        :param temp_lock:
        :return:
        """
        with temp_lock:
            sub_client_id = sub_client["subclientId"]
            c_sub_client_info = self.get_sub_client_info(sub_client_id)
            self._sub_client_list.append(c_sub_client_info)

    def get_library_list(self):
        """
        获取库列表
        :return:
        """
        library_list = []
        library = self.get_cmd('Library')
        if library is None:
            return None
        active_physical_node = library.findall(".//entityInfo")
        for node in active_physical_node:
            library_dict = dict()

            library_dict["library_name"] = node.attrib["name"]
            try:
                library_dict["library_id"] = int(node.attrib["id"])
            except TypeError as e:
                print("get_library_list", e)
            library_list.append(library_dict)
        return library_list

    def get_library_info(self, library_id):
        """
        获取库详细信息
        :param library_id:
        :return:
        """
        if library_id is None:
            return None
        command = "Library/{0}".format(library_id)
        resp = self.get_cmd(command)
        library_info = dict()
        # 容量/状态
        mag_lib_summary = resp.findall(".//magLibSummary")
        if mag_lib_summary:
            mag_lib_summary = mag_lib_summary[0]
            library_info["total_capacity"] = mag_lib_summary.attrib["totalCapacity"].strip()
            library_info["total_available_capacity"] = mag_lib_summary.attrib["totalAvailableSpace"].strip()
            library_info["is_online"] = mag_lib_summary.attrib["isOnline"]
        else:
            return None
            # raise Exception("该库不存在")
            # library_info["total_capacity"] = ""
            # library_info["total_available_capacity"] = ""
            # library_info["is_online"] = ""
        # 状态
        library_type = resp.findall(".//libraryInfo")
        # Library type.
        # 1 - 磁带
        # 3 - 磁盘/云
        # 4 - 独立库
        library_type_dict = {
            "1": "磁带",
            "3": "磁盘/云",
            "4": "独立库"
        }

        if library_type:
            library_type = library_type[0]
            library_type_string = library_type.attrib["libraryType"]
            try:
                library_type_string = library_type_dict[library_type_string]
                library_info["library_type"] = library_type_string
            except KeyError:
                library_info["library_type"] = ""
        else:
            library_info["library_type"] = ""
        return library_info

    def get_storage_pool_list(self):
        """
        获取存储池列表
        :return:
        """
        storage_pool_list = []
        storage_pool = self.get_cmd('StoragePool')
        if storage_pool is None:
            return None
        # active_physical_node = storage_pool.findall(".//entityInfo")
        # for node in active_physical_node:
        #     storage_pool = dict()
        #
        #     storage_pool["library_name"] = node.attrib["name"]
        #     try:
        #         storage_pool["library_id"] = int(node.attrib["id"])
        #     except TypeError as e:
        #         print("get_library_list", e)
        #     storage_pool_list.append(storage_pool)
        return storage_pool_list

    def get_CS(self):
        cs_info = self.get_cmd('CommServ')
        commcell_info = cs_info.findall(".//commcell")
        commcell_info_dict = {}
        if commcell_info is not None:
            commcell_info = commcell_info[0]
            commcell_info_dict["commCellName"] = commcell_info.attrib["commCellName"]
            commcell_info_dict["commCellId"] = commcell_info.attrib["commCellId"]
            commcell_info_dict["csGUID"] = commcell_info.attrib["csGUID"]

        return commcell_info_dict

    def test(self):
        temp_list = []
        event = self.get_cmd('/Events')
        if event is None:
            return None

    def get_agent_list(self, client_id):
        try:
            client_id = int(client_id)
        except Exception as e:
            print(e)
            return None
        else:
            agent_list = []
            cmd = 'Agent?clientId={0}'.format(client_id)
            resp = self.get_cmd(cmd)
            try:
                activePhysicalNode = resp.findall(".//idaEntity")
                for node in activePhysicalNode:
                    agent = dict()
                    agent["clientName"] = node.attrib["clientName"]
                    agent["agentType"] = node.attrib["appName"]
                    agent["appId"] = node.attrib["applicationId"]
                    agent_list.append(agent)
            except:
                self.msg = "error get agent type"
        return agent_list

    def custom_schedule_policy_index(self):
        # whole_list = []
        # client_list = self.get_client_list()
        # for client in client_list:
        #
        #     # {'clientId': 2, 'clientName': 'cv-server'}
        #     sub_client_list = self.get_sub_client_list(client["clientId"])
        #
        #     # [{'clientId': '24', 'subclientId': '140', 'backupsetId': '75', 'instanceId': '43', 'appName': 'Virtual Server', 'backupsetName': 'defaultBackupSet',
        #     #   'subclientName': 'default', 'instanceName': 'VMware', 'clientName': '192.168.100.60', '_type_': '7', 'applicationId': '106'}]
        #
        #     # app_count = 1
        #     # backupset_count = 1
        #     # appName = None
        #     # backupsetName = None
        #     #
        #     # # app_count/backupset_count
        #     # for sub_client in sub_client_list:
        #     #     if appName == sub_client["appName"]:
        #     #         app_count += 1
        #     #     if appName == sub_client["appName"] and backupsetName == sub_client["backupsetName"]:
        #     #         backupset_count += 1
        #
        #     for sub_client in sub_client_list:
        #
        #         subclientId = sub_client["subclientId"]
        #         appName = sub_client["appName"]
        #         backupsetName = sub_client["backupsetName"]
        #         subclientName = sub_client["subclientName"]
        #         instanceName = sub_client["instanceName"]
        #
        #         # schedules
        #         schedules = self.get_schedule_list(subclientId)
        #         # [{'taskId': '10', 'incLevels': 'BEFORE_SYNTH', 'description': '', 'appName': 'Windows File System', 'subclientName': 'DDBBackup', 'backupsetName': 'defaultBackupSet',
        #         # 'backupLevel': 'FULL', 'taskName': 'System Created for DDB subclients'}]
        #         # print(schedules)
        #
        #         for schedule in schedules:
        #
        #
        #             whole_list.append({
        #                 # client
        #                 "client_area": app_count,
        #
        #                 # app
        #                 "app_area": app_count,
        #
        #                 # backupset/instance
        #
        #
        #                 # subclient
        #
        #                 # schedule
        #             })

        return None

    def discover_VM(self, clientId):
        vm_list = []
        cmd = 'VMBrowse?PseudoClientId={0}&inventoryPath=%5CNONE%3AVMs'.format(clientId)
        resp = self.get_cmd(cmd)
        if resp == None:
            return False
        else:
            return resp
        # activePhysicalNode = resp.findall(".//inventoryInfo")
        #
        # for node in activePhysicalNode:
        #     attrib = node.attrib
        #     if attrib["type"] == '4':
        #         self.discoverVM(clientId, attrib["name"])
        #     if attrib["type"] == '9':
        #         self.vmList.append(attrib)

if __name__ == "__main__":
    a = time.time()
    # credit_info = {"web_addr": "192.168.1.121", "port": "81", "username": "admin", "pass_wd": "admin", "token": "",
    #                "last_login": 0}
    credit_info = {"web_addr": "192.168.100.149", "port": "81", "username": "admin", "pass_wd": "Admin@2017",
                   "token": "",
                   "last_login": 0}
    cv_token = CVRestApiToken()
    cv_token.login(credit_info)
    print("-----成功登陆")
    c = time.time()
    cv_api = CVApiOperate(cv_token)
    # sp = cv_api.get_backup_content(118)
    # sp = cv_api.custom_schedule_policy_index()
    # sp = cv_api.get_CS()
    # get_cs
    # print(sp)
    # sp = cv_api.get_client_list()  # 2357 11 12 13 14 22 24 2 3 5 7
    # sp = cv_api.get_client_info_by_name("cv-server")  # 2357 11 12 13 14 22 24
    # sp = cv_api.get_client_info_by_id(12)
    # sp = cv_api.custom_backup_tree_by_client(3)
    # sp = cv_api.get_sub_client_info(22)
    # sp = cv_api.discover_VM(5)
    # sp = cv_api.get_simple_sub_client_info(22)
    # sp = cv_api.get_schedule_list(5)
    # sp = cv_api.get_schedule_policy_info(30)
    # sp = cv_api.get_schedule_policy_list()

    # sp = cv_api.get_backup_set_list(3)
    # sp = cv_api.get_backup_set_info(5)
    # sp = cv_api.get_client_instance(3)
    # sp = cv_api.get_client_list()
    # sp = cv_api.get_library_list()
    # sp = cv_api.get_library_info(13)
    # sp = cv_api.get_job_info("4440437")
    # sp = cv_api.get_job_list("2",app_type_name="File System")
    # sp = cv_api.get_job_list("1")
    # sp = cv_api.get_sp_list()  # 26, 27, 28
    # sp = cv_api.get_sp_info("26")  # 25, 30
    # sp = cv_api.get_agent_list(7)
    # 通过数据库过滤辅助拷贝状态destcopyid

    # sp = cv_api.get_copy_from_sp("26", "25")
    # sp = cv_api.get_client_agent_list("3")
    # sp = cv_api.get_console_alert_list()
    # sp = cv_api.get_storage_pool_list()
    # sp = cv_api.test()
    sp = cv_api.get_sub_client_list(5)  # mysql 89  filesystem 4 oracle 118 sqlserver34 virtual22
    # sp = cv_api.get_vm_backup_content(61)
    # if sp is not None:
    #     print(len(sp), sp)
    # else:
    #     print("没有数据")
    # with open(r"C:\Users\Administrator\Desktop\lookup.json", "w") as f:
    #     f.write(str(sp))
    print(sp)
    b = time.time()
    print("登陆时间:", round(c - a, 3), "查询时间:", round(b - c, 3))
    # import pymssql
    # conn = pymssql.connect(host='192.168.100.149\COMMVAULT', user='sa_cloud', password='1qaz@WSX', database='CommServ')
    # cur = conn.cursor()
    # sql = """SELECT jobstatus, storagepolicy FROM [commserv].[dbo].[CommCellAuxCopyInfo] WHERE destcopyid=30 and storagepolicy LIKE 'SP-7DAY2'"""
    # print("-----", sql)
    # cur.execute(sql)
    # aux_copy_info = cur.fetchall()
    # print(aux_copy_info)
