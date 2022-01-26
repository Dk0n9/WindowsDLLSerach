# coding:utf8
import glob
import json
import platform

import win32api


def getFileVersionInfo(fileName):
    try:
        lang, codepage = win32api.GetFileVersionInfo(fileName, '\\VarFileInfo\\Translation')[0]
        strInfo = {}
        for propName in ["CompanyName", "LegalCopyright", "FileVersion", "FileDescription"]:
            strInfoPath = u'\\StringFileInfo\\%04X%04X\\%s' % (lang, codepage, propName)
            strInfo[propName] = win32api.GetFileVersionInfo(fileName, strInfoPath)

        return strInfo
    except Exception as err:
        print(fileName, err)
        return {}


def enumDLL():
    storageName = platform.version()
    storageContent = {}
    wp = open(storageName + ".json", "w+")
    fileList = glob.glob(r"C:\Windows\System32\*.dll")
    for fname in fileList:
        dllName = fname.split("\\")[-1]
        tmpContent = getFileVersionInfo(fname)
        if not tmpContent:
            continue
        storageContent[dllName] = tmpContent
    wp.write(json.dumps(storageContent, indent=1))
    wp.close()


if __name__ == '__main__':
    enumDLL()
