import _thread
import hashlib
import io
import json
import os
import subprocess
import tarfile
import time
import uuid

import requests
import urllib3

from django.shortcuts import render

# Create your views here.
from django.utils import timezone

from network_recon import settings
from recon import models, date_util, hash_util
from recon.common import port_protocols, unfinished, ztag_command

urllib3.disable_warnings()

try:
    models.ScanTask.objects.filter(execute_status=1).update(execute_status=0)
    models.BannerTask.objects.filter(execute_status=1).update(execute_status=0)
except BaseException as e:
    print(e)


def index(request):
    return render(request, "index.html")


def zmap_start(delay):
    while True:
        task = models.ScanTask.objects.filter(execute_status=0).order_by('priority').first()
        if task is not None:
            models.ScanTask.objects.filter(id=task.id).update(execute_status=1)
            scan_start(task)
        time.sleep(delay)


def file_hash(file_path):
    m = hashlib.md5()
    _file = io.FileIO(file_path, 'r')
    _bytes = _file.read(1024)
    while _bytes != b'':
        m.update(_bytes)
        _bytes = _file.read(1024)
    _file.close()
    md5value = m.hexdigest()
    return md5value


def scan_start(task_info):
    command = task_info.command
    print("zmap running: ", command)

    try:
        subprocess.call(command, shell=True)
        count = 0
        with open(task_info.port_result_path, "r") as file:
            for _ in file.readlines():
                count += 1

        port = task_info.port
        protocol_str = task_info.protocol
        if len(protocol_str) > 0:
            protocols = protocol_str.split(",")
        else:
            protocols = port_protocols.get(port)
        task_number = 0
        for protocol in protocols:
            if protocol in unfinished:
                continue
            banner_command = ["zgrab2", "-f", task_info.port_result_path, protocol, "-p", str(port), "-t 5s"]
            _id = hash_util.get_md5(" ".join(banner_command))
            zgrab_result_path = settings.banner_save_path + protocol + "_" + str(port) + "_" + _id + ".json"
            ztag_result_path = None
            ztag_status = -1
            if protocol in ztag_command.keys():
                ztag_result_path = settings.ztag_save_path + protocol + "_" + str(port) + "_" + _id + ".json"
                ztag_status = 0
            banner_command.append('--output-file='+zgrab_result_path)
            models.BannerTask.objects.create(id=_id, command=" ".join(banner_command), port=port, protocol=protocol,
                                             ip_count=count, scan_task_id=task_info.id, banner_result_path=zgrab_result_path,
                                             ztag_result_path=ztag_result_path, ztag_status=ztag_status,
                                             priority=task_info.priority, create_time=timezone.now())
            task_number += 1

        models.ScanTask.objects.filter(id=task_info.id).update(execute_status=2, open_port_count=count, banner_task_count=task_number)
        models.ReconRecordLog.objects.create(id=uuid.uuid1(), ip_count=task_info.ip_count, command=command, success_count=count,
                                             task_type="online", create_time=timezone.now())
    except BaseException as e1:
        print("zmap scan error", e1, command)
        models.ScanTask.objects.filter(id=task_info.id).update(execute_status=-1)


def exec_banner_job(delay):
    while True:
        print("exec_banner_job is running")
        task_info = models.BannerTask.objects.filter(execute_status=0).order_by('priority').first()
        if task_info is not None:
            models.BannerTask.objects.filter(id=task_info.id).update(execute_status=1)
            banner_start(task_info)
        time.sleep(delay)


def banner_start(task_info):
    command = task_info.command
    print("banner running: ", command)
    try:
        subprocess.call(command, shell=True)
        count = 0
        with open(task_info.banner_result_path, "r") as file:
            for line in file.readlines():
                if line.find('"error":"') == -1:
                    count += 1

        records_handled = 0
        ztag_status = -1
        if task_info.ztag_status == 0:
            ztag_status = 0
            shell_command = 'cat ' + task_info.banner_result_path + ' | ztag -p ' + str(task_info.port) + ' ' \
                            + ztag_command.get(task_info.protocol) + ' > ' + task_info.ztag_result_path
            output = subprocess.getoutput(shell_command)
            print("ztag result", output)
            try:
                result = output.split("\n")
                if len(result) > 0:
                    _info = result[len(result)-1]
                    rh = json.loads(_info).get('records_handled')
                    if rh is not None:
                        records_handled = int(rh)
                ztag_status = 1
            except BaseException as e3:
                print(e3, "error ZTag info", shell_command)

        models.BannerTask.objects.filter(id=task_info.id).update(execute_status=2, banner_success_count=count, ztag_handle_count=records_handled,
                                                                 ztag_status=ztag_status, finish_time=timezone.now())
        scantask = models.ScanTask.objects.filter(id=task_info.scan_task_id).first()
        number = scantask.banner_task_count - 1
        if number == 0:
            models.ScanTask.objects.filter(id=task_info.scan_task_id).update(banner_task_count=number, finish_time=timezone.now())
        else:
            models.ScanTask.objects.filter(id=task_info.scan_task_id).update(banner_task_count=number)
        models.ReconRecordLog.objects.create(id=uuid.uuid1(), ip_count=task_info.ip_count, command=command, success_count=count,
                                             task_type="banner", create_time=timezone.now())
    except BaseException as e1:
        print("zgrab scan error", e1, command)
        models.BannerTask.objects.filter(id=task_info.id).update(execute_status=-1)


def exec_finish_job(delay):
    while True:
        print("exec_finish_job is running")
        all_list = models.ScanTask.objects.filter(execute_status=2).filter(banner_task_count=0)\
                                          .filter(upload_status=-1).all()
        if len(all_list) > 0:
            report_path = settings.report_save_path + date_util.get_now_day_str() + '/'
            if os.path.exists(report_path) is False:
                os.makedirs(report_path)
            for task in all_list:
                try:
                    banner_path = dict()
                    ztag_path = dict()
                    banner_list = models.BannerTask.objects.filter(scan_task_id=task.id, execute_status=2).all()
                    for info in banner_list:
                        if info.banner_result_path is not None:
                            banner_path[info.banner_result_path] = "banner_"+info.protocol+".json"
                        if info.ztag_result_path is not None:
                            ztag_path[info.ztag_result_path] = "ztag_"+info.protocol+".json"

                    filename = str(task.id) + '_' + str(task.port) + '.tar.gz'
                    file_path = report_path + filename
                    with tarfile.open(file_path, 'w:gz') as tar:
                        tar.add(task.port_result_path, arcname='zmap.csv')
                        for msg in banner_path.keys():
                            tar.add(msg, arcname=banner_path.get(msg))
                        for msg in ztag_path.keys():
                            tar.add(msg, arcname=ztag_path.get(msg))
                    file_md5 = file_hash(file_path)
                    models.ScanTask.objects.filter(id=task.id).update(report_result_path=file_path, report_file_md5=file_md5, upload_status=0)
                    # os.remove(task.port_result_path)
                    # for msg in banner_path.keys():
                    #     os.remove(msg)
                    # for msg in ztag_path.keys():
                    #     os.remove(msg)
                except BaseException as e2:
                    print("gen report error", e2, task)
        time.sleep(delay)


def get_mac():
    address = hex(uuid.getnode())[2:]
    address = address.upper()
    return '-'.join(address[i:i + 2] for i in range(0, len(address), 2))


def upload_center(delay):
    while True:
        scan_finish_list = models.ScanTask.objects.filter(upload_status=0).all()
        if len(scan_finish_list) > 0:
            for up in scan_finish_list:
                try:
                    data = {
                        'port': up.port,
                        'count': up.ip_count,
                        'ip_range': up.ip_range,
                        'client_ip': get_mac(),
                        'time': up.finish_time.time()
                    }

                    report_file = open(up.report_result_path, "rb")

                    files = {
                        'file': report_file
                    }

                    response = requests.post('https://182.148.53.139:18081/dataExchange/upload4scan', data=data, files=files, verify=False)
                    print(response.text)
                    if response.json()['msg'] == 'success':
                        models.ScanTask.objects.filter(id=up.id).update(upload_status=1)
                        os.remove(up.report_result_path)
                except BaseException as e:
                    print("upload center error", up, e)

        time.sleep(delay)


_thread.start_new_thread(upload_center, (2,))

_thread.start_new_thread(zmap_start, (2,))
_thread.start_new_thread(exec_banner_job, (2,))
_thread.start_new_thread(exec_finish_job, (2,))


# print(timezone.now())
