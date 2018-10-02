#!/usr/bin/python
#!-*-coding:utf8-*-

import sys
import os
import subprocess
import textwrap


class ExecutionError(Exception):
    pass


class Buffer:
    def __init__(self):
        self.markdown = ""

    def append(self, text):
        self.markdown = self.markdown + "\n" + text

    def __str__(self):
        return self.markdown


def execute(command, error=""):
    try:
        process = subprocess.Popen(command, shell=False,
                         stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE)
        out, err = process.communicate()
        if process.returncode != 0:
            print(str(err))
            raise ExecutionError("Aborted!!!")
        return out.decode("utf-8")
    except OSError:
        print("==============================")
        print("Error occur!!!")
        print("==============================")
        if error:
            print(error)
        else:
            print("Command not found ({})".format(command[0]))
        raise ExecutionError("Aborted!!!")


def platform():
    results = []
    uname = ['uname', '-a']
    results.append(execute(uname).replace('\n', ''))
    command = ['traceroute', 'google.com', '-m', '2']
    tracert = execute(command)
    provider_ip = tracert.split("\n")[2].split(' ')[3]
    command = execute(['whois', provider_ip])
    for line in command.split('\n'):
        if line.startswith('org-name'):
            results.append("Provider={}".format(line.replace('org-name:', '').strip()))
    return results


def main():
    buf = Buffer()
    ptf = platform()
    text = "## My Platform"
    buf.append(text)
    for el in ptf:
        buf.append("- {}".format(el))
    print(buf)
