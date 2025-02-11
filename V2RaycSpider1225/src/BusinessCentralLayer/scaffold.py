__all__ = ['scaffold', 'command_set']

import csv
import time
from typing import List

import gevent
from gevent import monkey

from src.BusinessCentralLayer.setting import *

monkey.patch_all()

command_set = {

    # ---------------------------------------------
    # 部署接口
    # ---------------------------------------------
    'deploy': "部署项目（定时任务/Flask 开启与否取决于yaml配置文件）",
    # ---------------------------------------------
    # 调试接口
    # ---------------------------------------------
    "decouple": "立即唤醒一次subs_ddt链接解耦任务",
    "overdue": "立即执行一次过时链接清洗任务",
    "run": "[请使用spawn命令替代]立即执行一次采集任务（强制使用协程加速）",
    "force_run": "强制执行采集任务",
    "remain": "读取剩余订阅数量",
    "ping": "测试数据库连接",
    "entropy": "打印采集队列",
    "exile": "执行队列运维脚本（高饱和强阻塞任务）",
    "spawn": "并发执行所有在列的采集任务",
    "mining": "启动一次针对STAFF host的SEO全站挖掘任务",
    # ---------------------------------------------
    # Windows 功能接口
    # ---------------------------------------------
    "panel": "[for Windows] 打开桌面前端面板",
    "ash": "[for Windows] 一键清洗订阅池,并将所有类型订阅转换为Clash yaml配置文件,"
           "借由URL Scheme自动打开Clash并下载配置文件",
    # ---------------------------------------------
    # 调用示例
    # ---------------------------------------------
    "example": "python main.py ping"
}


class _ConfigQuarantine(object):
    def __init__(self):

        self.root = [
            SERVER_DIR_CLIENT_DEPORT, SERVER_PATH_DEPOT_VCS,
            SERVER_DIR_DATABASE_CACHE, SERVER_DIR_CACHE_BGPIC
        ]
        self.flag = False

    def set_up_file_tree(self, root):
        """
        --/qinse/V2RaycSpider{verNum}
            --BCL
            --BLL
            --BVL
            --Database
                --client_depot
                    --vcs.csv
                --logs
                    --*error.log
                    --*runtime.log
                --temp_cache
                    --*AnyTempCacheFile...
                --*CrawlFetchHistory.txt
                --fake_useragent_0.1.11.json
            --*tests
        """

        # 检查默认下载地址是否残缺 深度优先初始化系统文件
        for child_ in root:
            if not os.path.exists(child_):
                self.flag = True
                try:
                    # 初始化文件夹
                    if os.path.isdir(child_) or not os.path.splitext(child_)[-1]:
                        os.mkdir(child_)
                        logger.success(f"系统文件链接成功->{child_}")
                    # 初始化文件
                    else:
                        if child_ == SERVER_PATH_DEPOT_VCS:
                            try:
                                with open(child_, 'w', encoding='utf-8', newline='') as fpx:
                                    csv.writer(fpx).writerow(['version', 'title'])
                                logger.success(f"系统文件链接成功->{child_}")
                            except Exception as ep:
                                logger.exception(f"Exception{child_}{ep}")
                except Exception as ep:
                    logger.exception(ep)

    @staticmethod
    def check_config(call_driver: bool = False):
        chromedriver_not_found_error = f"<ScaffoldGuider> ForceRun || ChromedriverNotFound ||" \
                                       f"未查找到chromedriver驱动，请根据技术文档正确配置\n" \
                                       f">>> https://github.com/QIN2DIM/V2RayCloudSpider"

        if not all(SMTP_ACCOUNT.values()):
            logger.warning('您未正确配置<通信邮箱>信息(SMTP_ACCOUNT)')
        if not SERVER_CHAN_SCKEY:
            logger.warning("您未正确配置<Server酱>的SCKEY")
        if not all([REDIS_SLAVER_DDT.get("host"), REDIS_SLAVER_DDT.get("password")]):
            logger.warning('您未正确配置<Redis-Slave> 本项目的部分功能将毫无意义')
        if not all([REDIS_MASTER.get("host"), REDIS_MASTER.get("password")]):
            logger.error("您未正确配置<Redis-Master> 此配置为“云彩姬”的核心组件，请配置后重启项目！")
            exit()

        # 当需要调用的接口涉及到driver操作时抛出
        if call_driver:
            if not os.path.exists(CHROMEDRIVER_PATH):
                logger.error(chromedriver_not_found_error)
                exit()

    def run(self):
        try:
            if [cq for cq in reversed(self.root) if not os.path.exists(cq)]:
                logger.warning('系统文件残缺！')
                logger.debug("启动<工程重构>模块...")
                self.set_up_file_tree(self.root)
            self.check_config()

        finally:
            if self.flag:
                logger.success(">>> 运行环境链接完成，请重启项目")
                logger.warning(">>> 提醒您正确配置Chrome及对应版本的ChromeDriver")
                exec("if self.flag:\n\texit()")


_ConfigQuarantine().run()


class _ScaffoldGuider(object):
    # __slots__ = list(command_set.keys())

    def __init__(self):
        # 脚手架公开接口
        self.scaffold_ruler = [i for i in self.__dir__() if i.startswith('_scaffold_')]

    @logger.catch()
    def startup(self, driver_command_set: List[str]):
        """
        仅支持单进程使用
        @param driver_command_set: 在空指令时列表仅有1个元素，表示启动路径
        @return:
        """
        # logger.info(f">>> {' '.join(driver_command_set)}")

        # -------------------------------
        # TODO 优先级0：预处理指令集
        # -------------------------------
        # CommandId or List[CommandId]
        driver_command: List[str] = []

        # 未输入任何指令 列出脚手架简介
        if len(driver_command_set) == 1:
            print("\n".join([f">>> {menu[0].ljust(20, '-')}|| {menu[-1]}" for menu in command_set.items()]))
            return True
        # 输入立即指令 转译指令
        elif len(driver_command_set) == 2:
            driver_command = [driver_command_set[-1].lower(), ]
        # 输入指令集 转译指令集
        elif len(driver_command_set) > 2:
            driver_command = list(set([command.lower() for command in driver_command_set[1:]]))

        # 捕获意料之外的情况
        if not isinstance(driver_command, list):
            return True
        # -------------------------------
        # TODO 优先级1：解析运行参数
        # -------------------------------

        # TODO --help 帮助菜单（继续完善相关功能）
        # 使用该参数时系统不解析运行指令
        if '--help' in driver_command:
            logger.info(f">>>GuiderHelp || 帮助菜单")
            driver_command.remove("--help")
            for command_ in driver_command:
                introduction = command_set.get(command_)
                if introduction:
                    print(f"> {command_.ljust(20, '-')}|| {introduction}")
                else:
                    print(f"> {command_}指令不存在")
            return True

        # -------------------------------
        # TODO 优先级2：运行单线程指令
        # -------------------------------

        # 协程任务队列
        task_list = []

        # 测试数据库连接
        while driver_command.__len__() > 0:
            _pending_command = driver_command.pop()
            try:
                task_list.append(gevent.spawn(eval(f"self._scaffold_{_pending_command}")))
            except Exception as e:
                logger.warning(f'脚手架暂未授权指令<{_pending_command}> {e}')
        else:
            # 并发执行以上指令
            gevent.joinall(task_list)

        # -------------------------------
        # TODO 优先级3：自定义参数部署（阻塞线程）
        # -------------------------------

        if 'deploy' in driver_command:
            self._scaffold_deploy()

    @staticmethod
    def _scaffold_deploy():
        logger.info(f"<ScaffoldGuider> Deploy || MainProcess")
        from src.BusinessCentralLayer.middleware.interface_io import SystemInterface
        SystemInterface.run(deploy_=True)

    @staticmethod
    def _scaffold_decouple():
        logger.info(f"<ScaffoldGuider> Decouple || General startup")
        from src.BusinessLogicLayer.plugins.accelerator import SubscribesCleaner
        SubscribesCleaner(debug=True).interface(power=DEFAULT_POWER)

    @staticmethod
    def _scaffold_overdue():
        logger.info(f"<ScaffoldGuider> Overdue || Redis DDT")
        from src.BusinessCentralLayer.middleware.interface_io import SystemInterface
        SystemInterface.ddt()

    @staticmethod
    def _scaffold_spawn():
        _ConfigQuarantine.check_config(call_driver=True)
        logger.info(f"<ScaffoldGuider> Spawn || MainCollector")
        from src.BusinessLogicLayer.cluster.slavers import __entropy__
        from src.BusinessLogicLayer.plugins.accelerator import booster
        from src.BusinessCentralLayer.setting import DEFAULT_POWER
        booster(docker=__entropy__, silence=True, power=DEFAULT_POWER, assault=True)

    @staticmethod
    def _scaffold_run():
        _ConfigQuarantine.check_config(call_driver=True)
        logger.info(f"<ScaffoldGuider> Run || MainCollector")
        from src.BusinessCentralLayer.middleware.interface_io import SystemInterface
        SystemInterface.run(deploy_=False)

    @staticmethod
    def _scaffold_force_run():
        _ConfigQuarantine.check_config(call_driver=True)
        logger.info(f"<ScaffoldGuider> ForceRun || MainCollector")
        from src.BusinessCentralLayer.setting import CRAWLER_SEQUENCE
        from src.BusinessLogicLayer.plugins.accelerator import ForceRunRelease
        ForceRunRelease(task_docker=CRAWLER_SEQUENCE).interface()

    @staticmethod
    def _scaffold_remain():
        from src.BusinessCentralLayer.middleware.subscribe_io import select_subs_to_admin
        tracer = [f"{tag[0]}\n采集类型：{info_[0]}\n存活数量：{tag[-1]}" for info_ in
                  select_subs_to_admin(select_netloc=None, _debug=False)['info'].items() for tag in info_[-1].items()]
        for i, tag in enumerate(tracer):
            print(f">>> [{i + 1}/{tracer.__len__()}]{tag}")

    @staticmethod
    def _scaffold_ping():
        from src.BusinessCentralLayer.middleware.redis_io import RedisClient
        logger.info(f"<ScaffoldGuider> Ping || {RedisClient().test()}")

    @staticmethod
    def _scaffold_panel():
        from src.BusinessCentralLayer.middleware.interface_io import SystemInterface
        SystemInterface.system_panel()

    @staticmethod
    def _scaffold_entropy(_debug=False):
        from src.BusinessLogicLayer.cluster.slavers import __entropy__
        for i, host_ in enumerate(__entropy__):
            print(f">>> [{i + 1}/{__entropy__.__len__()}]{host_['name']}")
            print(f"注册链接: {host_['register_url']}")
            print(f"存活周期: {host_['life_cycle']}天")
            print(f"采集类型: {'&'.join([f'{j[0].lower()}' for j in host_['hyper_params'].items() if j[-1]])}\n")

    @staticmethod
    def _scaffold_exile(task_sequential=4):

        logger.debug(f"<ScaffoldGuider> Exile[0/{task_sequential}] || Running scaffold exile...")
        time.sleep(0.3)

        # task1: 检查队列任务
        logger.debug(f"<ScaffoldGuider> Exile[1/{task_sequential}] || Checking the task queue...")
        time.sleep(0.3)
        _ScaffoldGuider._scaffold_entropy(_debug=True)
        # logger.success(f">>> [Mission Completed] || entropy")

        # task2: decouple
        logger.debug(f"<ScaffoldGuider> Exile[2/{task_sequential}] || Cleaning the subscribe pool...")
        time.sleep(0.3)
        _ScaffoldGuider._scaffold_decouple()
        # logger.success(f">>> [Mission Completed] || decouple")

        # task3: overdue
        logger.debug(f"<ScaffoldGuider> Exile[3/{task_sequential}] || Cleaning timed out subscribes...")
        time.sleep(0.3)
        _ScaffoldGuider._scaffold_overdue()
        # logger.success(">>> [Mission Completed] || overdue")

        # finally: print task-queue， remaining subscribes
        logger.debug(f"<ScaffoldGuider> Exile[{task_sequential}/{task_sequential}] || Outputting debug data...")
        _ScaffoldGuider._scaffold_entropy()
        _ScaffoldGuider._scaffold_remain()
        logger.success("<ScaffoldGuider> Exile[Mission Completed] || exile")

    @staticmethod
    @logger.catch()
    def _scaffold_ash():
        """
        无尽套娃
        """
        from src.BusinessLogicLayer.apis import scaffold_api
        logger.info(f"<ScaffoldGuider> ash | Clash订阅堆一键生成脚本")

        # --------------------------------------------------
        # 参数清洗
        # --------------------------------------------------
        if 'win' not in platform:
            return

        # --------------------------------------------------
        # 运行脚本
        # --------------------------------------------------
        return scaffold_api.ash(debug=True, decouple=True)

    @staticmethod
    def _scaffold_mining():
        """
        “国外”服务器：直接运行
        大陆主机：开启代理后运行
        :return:
        """
        from src.BusinessLogicLayer.apis.staff_mining import staff_api
        use_collector = staff_api.is_first_run()
        classify_dir, staff_info = staff_api.go(
            debug=False,
            silence=True,
            power=os.cpu_count() * 2,
            identity_recaptcha=False,
            use_collector=use_collector,
            use_checker=True,
            use_generator=False,
        )
        staff_api.refresh_cache(mode='de-dup')
        print(f"\n\nSTAFF INFO\n{'_' * 32}")
        for element in staff_info.items():
            for i, tag in enumerate(element[-1]):
                print(f">>> [{i + 1}/{len(element[-1])}]{element[0]}: {tag}")
        print(f">>> 文件导出目录: {classify_dir}")


scaffold = _ScaffoldGuider()
